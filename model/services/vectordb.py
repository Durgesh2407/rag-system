import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


engine = create_engine(DATABASE_URL)


def store_embeddings(document_id, chunks, embeddings):

    with engine.connect() as conn:

        for i, (chunk, embedding) in enumerate(
            zip(chunks, embeddings)
        ):

            embedding_list = embedding.tolist()

            query = text("""
                INSERT INTO document_chunks
                (
                    document_id,
                    chunk_index,
                    content,
                    embedding
                )
                VALUES
                (
                    :document_id,
                    :chunk_index,
                    :content,
                    :embedding
                )
            """)

            conn.execute(
                query,
                {
                    "document_id": document_id,
                    "chunk_index": i,
                    "content": chunk,
                    "embedding": embedding_list
                }
            )

        conn.commit()



def search_similar_chunks(ques_embeeding):
    with engine.connect() as conn:
        query = text("""
            SELECT * FROM document_chunks
            ORDER BY embedding <=> CAST(:ques_embeeding AS vector)
            LIMIT :5
        """)

        res = conn.execute(query, {...}).fetchall()
        
    return res
