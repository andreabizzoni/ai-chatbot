from openai import AsyncOpenAI
from app.config.settings import settings
from app.database.vector_store import VectorStore
from langfuse import observe, Langfuse


class Agent:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.chat_model = settings.chat_model
        self.dimensions = settings.embedding_dimensions
        self.embedding_model = settings.embedding_model
        self.langfuse = Langfuse(
            public_key=settings.langfuse_public_key,
            secret_key=settings.langfuse_secret_key,
            host=settings.langfuse_base_url,
        )

    async def generate_embedding(self, text: str) -> list[float]:
        response = await self.client.embeddings.create(
            input=text, model=self.embedding_model, dimensions=self.dimensions
        )
        return response.data[0].embedding

    async def generate_embeddings_batch(self, texts: list[str]) -> list[list[float]]:
        response = await self.client.embeddings.create(
            input=texts, model=self.embedding_model, dimensions=self.dimensions
        )
        return [item.embedding for item in response.data]

    @observe(capture_input=False, capture_output=False, as_type="generation")
    async def answer_query_with_rag(self, user_query: str) -> str:
        query_embedding = await self.generate_embedding(user_query)
        relevant_docs = await VectorStore.similarity_search(
            query_embedding=query_embedding
        )

        context = "\n".join([doc.content for doc in relevant_docs])

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
            model=self.chat_model,
            messages=messages,
        )

        self.langfuse.update_current_generation(
            model=self.chat_model,
            input=messages,
            output=response.choices[0].message.content,
            usage_details={
                "input": response.usage.prompt_tokens,
                "output": response.usage.completion_tokens,
            },
        )

        return response.choices[0].message.content


_agent_instance: Agent | None = None


def initialize_agent() -> None:
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = Agent()


async def cleanup_agent() -> None:
    global _agent_instance
    if _agent_instance is not None:
        await _agent_instance.client.close()
        _agent_instance.langfuse.flush()
        _agent_instance = None


def get_agent() -> Agent:
    if _agent_instance is None:
        raise RuntimeError("Agent not initialized. Call initialize_agent() first.")
    return _agent_instance
