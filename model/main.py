from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.ingest import router as ingest_router
from routes.chat import router as chat_router

app = FastAPI()

origin = [
    "http://localhost:5173"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins= origin,
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingest_router, prefix="/api")

app.include_router(chat_router, prefix="/api")

@app.get("/health")
def health():
    return {"messgage": "healthy"}