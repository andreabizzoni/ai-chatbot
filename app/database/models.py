from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class Document(BaseModel):
    id: int = Field(..., description="Unique document identifier")
    content: str = Field(..., description="Document text content")
    embedding: list[float] = Field(..., description="Vector embedding")
    metadata: Optional[dict] = Field(default=None, description="Additional metadata")
    created_at: datetime = Field(..., description="Creation timestamp")
