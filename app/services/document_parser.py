from docling.document_converter import DocumentConverter
from docling.chunking import HybridChunker
from app.utils.tokenizer import OpenAITokenizer
from app.schemas.document import ProcessedChunk, ChunkMetadata


class DocumentParser:
    def __init__(self, max_tokens: int = 8191):
        self.converter = DocumentConverter()
        tokenizer = OpenAITokenizer()
        self.chunker = HybridChunker(
            tokenizer=tokenizer, max_tokens=max_tokens, merge_peers=True
        )

    def process_document(self, pdf_path: str) -> list[ProcessedChunk]:
        result = self.converter.convert(pdf_path)
        chunks = list(self.chunker.chunk(result.document))

        processed_chunks = []
        for idx, chunk in enumerate(chunks):
            processed_chunks.append(
                ProcessedChunk(
                    content=chunk.text,
                    metadata=ChunkMetadata(
                        chunk_id=idx,
                        path=chunk.meta.doc_items[0].self_ref
                        if chunk.meta.doc_items
                        else None,
                    ),
                )
            )

        return processed_chunks


parser = DocumentParser()
