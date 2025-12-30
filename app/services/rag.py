from openai import AsyncOpenAI
from app.database.vector_store import VectorStore
from app.services.embeddings import embedding_service
from app.config.settings import settings


class RAGService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = settings.chat_model

    async def query(self, user_query: str, top_k: int = 5) -> str:
        query_embedding = await embedding_service.generate_embedding(user_query)

        relevant_docs = await VectorStore.similarity_search(
            query_embedding, top_k=top_k
        )

        if not relevant_docs:
            return "I don't have enough information to answer that question."

        context = "\n\n".join([doc.content for doc in relevant_docs])

        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant. Answer the user's question based on the provided context. If the context doesn't contain relevant information, say so.",
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {user_query}",
            },
        ]

        response = await self.client.chat.completions.create(
            model=self.model, messages=messages, temperature=0.7
        )

        return response.choices[0].message.content


rag_service = RAGService()
