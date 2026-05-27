from pydantic import BaseModel
from fastapi import APIRouter
from services.embedding import generate_embeddings

class QueryRequest(BaseModel):
    question : str
    document_id : str = None

router = APIRouter()

@router.post("/chat")
def chat(query_req : QueryRequest):
    ques_embedding = generate_embeddings([query_req.question])[0]
    print(ques_embedding)