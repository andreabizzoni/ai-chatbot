from app.database.connection import Database
from app.schemas.embedding import EmbeddingRecord


class VectorStore:
    @classmethod
    async def insert_embedding(
        cls, content: str, embedding: list[float], metadata: dict
    ) -> int:
        result = await Database.fetchrow(
            """
            INSERT INTO embeddings (content, embedding, metadata)
            VALUES ($1, $2::vector, $3::jsonb)
            RETURNING id
            """,
            content,
            str(embedding),
            metadata,
        )
        return result["id"]

    @classmethod
    async def insert_embeddings_batch(
        cls, contents: list[str], embeddings: list[list[float]], metadatas: list[dict]
    ) -> list[int]:
        ids = []
        for content, embedding, metadata in zip(contents, embeddings, metadatas):
            result = await Database.fetchrow(
                """
                INSERT INTO embeddings (content, embedding, metadata)
                VALUES ($1, $2::vector, $3::jsonb)
                RETURNING id
                """,
                content,
                str(embedding),
                metadata,
            )
            ids.append(result["id"])
        return ids

    @classmethod
    async def similarity_search(
        cls, query_embedding: list[float], top_k: int = 5, threshold: float = 0.0
    ) -> list[EmbeddingRecord]:
        results = await Database.fetch(
            """
            SELECT id, content, embedding, metadata, created_at,
                   1 - (embedding <=> $1::vector) as similarity
            FROM embeddings
            WHERE 1 - (embedding <=> $1::vector) > $2
            ORDER BY embedding <=> $1::vector
            LIMIT $3
            """,
            str(query_embedding),
            threshold,
            top_k,
        )

        return [
            EmbeddingRecord(
                id=row["id"],
                content=row["content"],
                embedding=list(row["embedding"]),
                metadata=row["metadata"],
                created_at=row["created_at"],
            )
            for row in results
        ]

    @classmethod
    async def count(cls) -> int:
        result = await Database.fetchrow("SELECT COUNT(*) as total FROM embeddings")
        return result["total"]

    @classmethod
    async def delete_all(cls) -> None:
        await Database.execute("DELETE FROM embeddings")
