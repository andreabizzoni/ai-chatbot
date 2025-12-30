from typing import Optional
from pydantic import BaseModel, Field


class ChunkMetadata(BaseModel):
    chunk_id: int = Field(..., description="Sequential chunk identifier")
    path: Optional[str] = Field(None, description="Document structure path reference")


class ProcessedChunk(BaseModel):
    content: str = Field(..., description="Chunk text content")
    metadata: ChunkMetadata = Field(..., description="Chunk metadata")
