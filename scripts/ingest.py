import asyncio
import json
from app.services.document_parser import DocumentParser
from app.services.embeddings import embedding_service
from app.database.connection import db
from app.config import settings


async def ingest_document(pdf_path: str):
    print(f"Starting document ingestion for: {pdf_path}")

    await db.connect()

    try:
        parser = DocumentParser(max_tokens=settings.embedding_dimensions)
        chunks = parser.process_document(pdf_path)
        print(f"Parsed {len(chunks)} chunks from document")

        batch_size = 100
        total_batches = (len(chunks) + batch_size - 1) // batch_size

        for i in range(0, len(chunks), batch_size):
            batch = chunks[i : i + batch_size]
            texts = [chunk.content for chunk in batch]

            batch_num = i // batch_size + 1
            print(f"Generating embeddings for batch {batch_num}/{total_batches}")
            embeddings = await embedding_service.generate_embeddings_batch(texts)

            print("Storing batch in database...")
            for chunk, embedding in zip(batch, embeddings):
                await db.execute(
                    """
                    INSERT INTO embeddings (content, embedding, metadata)
                    VALUES ($1, $2::vector, $3::jsonb)
                    """,
                    chunk.content,
                    str(embedding),
                    json.dumps(chunk.metadata.model_dump()),
                )

            print(f"Batch {batch_num} completed")

        count = await db.fetchrow("SELECT COUNT(*) as total FROM embeddings")
        print(f"\nIngestion complete! Total documents in database: {count['total']}")

    finally:
        await db.disconnect()


if __name__ == "__main__":
    pdf_path = "data/fertil_catalog.pdf"
    asyncio.run(ingest_document(pdf_path))
