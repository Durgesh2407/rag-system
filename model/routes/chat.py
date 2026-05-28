from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from services.embedding import generate_embeddings
from services.vectordb import search_similar_chunks

class QueryRequest(BaseModel):
    question : str

router = APIRouter()

@router.post("/chat")
def chat(query_req : QueryRequest):
    try:
        ques_embedding = generate_embeddings([query_req.question])[0]
        print(ques_embedding)
        chunks = search_similar_chunks(ques_embedding)
        print(chunks)
        return {"results": [dict(row._mapping) for row in chunks]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))