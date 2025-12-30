from openai import AsyncOpenAI
from app.config import settings


class Embedder:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = settings.embedding_model
        self.dimensions = settings.embedding_dimensions

    async def generate_embedding(self, text: str) -> list[float]:
        response = await self.client.embeddings.create(
            input=text, model=self.model, dimensions=self.dimensions
        )
        return response.data[0].embedding

    async def generate_embeddings_batch(self, texts: list[str]) -> list[list[float]]:
        response = await self.client.embeddings.create(
            input=texts, model=self.model, dimensions=self.dimensions
        )
        return [item.embedding for item in response.data]


embedding_service = Embedder()
