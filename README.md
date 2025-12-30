# AI Chatbot Backend

RAG-based chatbot using FastAPI, PostgreSQL (pgvector), OpenAI, and Docling.

## Setup

1. **Install dependencies:**
```bash
uv sync
```

2. **Configure environment variables:**
```bash
cp .env.example .env
# Edit .env with your credentials
```

3. **Start the database:**
```bash
docker compose up -d
```

4. **Run the ingestion script:**
```bash
uv run python scripts/ingest.py
```

5. **Start the API server:**
```bash
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### POST /api/chat
Query the chatbot with a question.

**Request:**
```json
{
  "query": "What products are available?"
}
```

**Response:**
```json
{
  "response": "Based on the catalog, the following products are available..."
}
```

### GET /health
Check API health and database status.

**Response:**
```json
{
  "status": "healthy",
  "embeddings_count": 150
}
```

## Testing

### Using curl:
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "What products do you have?"}'
```