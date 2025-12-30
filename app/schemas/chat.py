from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1, description="User's question or query")


class ChatResponse(BaseModel):
    response: str = Field(..., description="AI-generated response")
