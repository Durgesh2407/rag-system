from fastapi import APIRouter, UploadFile, File, HTTPException, Form
import tempfile, os
from services.pdfloader import extract_text
from services.chunker import chunk_text
from services.embedding import generate_embeddings
from services.vectordb import store_embeddings

router = APIRouter()


@router.post("/ingest")
async def ingest(file: UploadFile = File(...), document_id: str = Form(...)):
    contents = await file.read()
    # print(contents)

    # saving  temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(contents)
        tmp_path = tmp.name

    # assigning path
    pdf_path = tmp_path

    try:
        #Extracting chunks from PDF
        full_text = extract_text(pdf_path)
        print("Text Extracted")

        #Generating chunks with overlap
        chunks = chunk_text(full_text)
        print("Chunks are created")

        #Generating embeddings
        embeddings = generate_embeddings(chunks)
        print("Embeddings created")

        #store embeddings in db
        store_embeddings(
            document_id,
            chunks,
            embeddings
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
    finally:
        # removing the file
        os.remove(pdf_path)

    return {"docid": document_id, "message": "Successfull"}