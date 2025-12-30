from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routes import router
from app.database import Database, VectorStore


@asynccontextmanager
async def lifespan(app: FastAPI):
    await Database.connect()

    count = await VectorStore.count()
    print(f"Connected to database. Total embeddings: {count}")

    if count == 0:
        print("Warning: No embeddings found in database. Run ingestion script first.")

    yield

    await Database.disconnect()
    print("Database connection closed")


app = FastAPI(
    title="AI Chatbot API",
    description="RAG-based chatbot using FastAPI, PostgreSQL, and OpenAI",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "AI Chatbot API is running"}


@app.get("/health")
async def health():
    try:
        count = await VectorStore.count()
        return {"status": "healthy", "embeddings_count": count}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
