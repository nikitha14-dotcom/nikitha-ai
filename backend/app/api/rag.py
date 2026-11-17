"""RAG related API endpoints."""
"""RAG related API endpoints.

Provides:
- POST /rag/upload    -> upload a PDF/text file
- GET  /rag/documents -> list user's documents
- DELETE /rag/{doc_id} -> delete a document (and its chunks)
- POST /rag/query      -> ask a question over the user's knowledge base

All routes are protected by JWT authentication via `get_current_user`.
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List
import os
import uuid
import shutil
import json

from backend.app.database import get_db
from backend.app.core.security import get_current_user
from backend.app.models.user import User
from backend.app.models.document import Document, DocumentChunk
from backend.app.ai.provider import ai_service

# Optional heavy imports – loaded gracefully so server can run without crash
try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

try:
    import numpy as np
except ImportError:
    np = None

router = APIRouter()

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MiB
ALLOWED_TYPES = {"application/pdf", "text/plain"}
CHUNK_SIZE = 500  # characters per chunk
CHUNK_OVERLAP = 100

def validate_upload(file: UploadFile):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    # size check – FastAPI streams, so we read a bit to estimate size
    if file.spool_max_size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large")

def save_temp_file(upload: UploadFile) -> str:
    # store in a safe temporary folder under storage
    storage_root = os.path.join(os.path.dirname(__file__), "..", "..", "storage", "uploads")
    os.makedirs(storage_root, exist_ok=True)
    unique_name = f"{uuid.uuid4().hex}_{upload.filename}"
    dest_path = os.path.join(storage_root, unique_name)
    with open(dest_path, "wb") as out:
        shutil.copyfileobj(upload.file, out)
    return dest_path

def extract_text(path: str, filetype: str) -> List[dict]:
    """Extract text from a file, returning a list of dicts.
    Each dict contains:
        "page": int (1‑based) for PDFs, None for plain‑text files
        "text": extracted string for that page.
    """
    results: List[dict] = []
    if filetype == "application/pdf":
        if PyPDF2 is None:
            raise HTTPException(status_code=501, detail="PyPDF2 is required for PDF processing. Install via 'pip install PyPDF2'.")
        with open(path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for i, page in enumerate(reader.pages):
                txt = page.extract_text() or ""
                results.append({"page": i + 1, "text": txt})
    elif filetype == "text/plain":
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            txt = f.read()
        results.append({"page": None, "text": txt})
    else:
        raise ValueError("Unsupported file type for extraction")
    return results

def chunk_text(text: str) -> List[dict]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + CHUNK_SIZE
        chunk = text[start:end]
        chunks.append({"text": chunk, "start": start, "end": end})
        start = max(start + CHUNK_SIZE - CHUNK_OVERLAP, 0)
    return chunks

async def embed_texts(texts: List[str]) -> List[List[float]]:
    """Generate Gemini embeddings for a list of text strings.
    Returns a list of embedding vectors (list of floats).
    Raises HTTPException on any failure – callers must handle it.
    """
    if not ai_service.gemini_key:
        raise HTTPException(status_code=500, detail="Gemini API key not configured")
    try:
        from google import genai
        client = genai.Client(api_key=ai_service.gemini_key)
        embeddings: List[List[float]] = []
        for txt in texts:
            if hasattr(client, "models") and hasattr(client.models, "embed_content"):
                resp = client.models.embed_content(
                    model="gemini-embedding-001",
                    contents=txt,
                )
            elif hasattr(client, "embed_content"):
                resp = client.embed_content(
                    model="gemini-embedding-001",
                    content=txt,
                )
            else:
                raise ValueError("google-genai Client does not have embed_content method")

            if hasattr(resp, "embedding") and hasattr(resp.embedding, "values"):
                emb = list(resp.embedding.values)
            elif hasattr(resp, "embeddings") and resp.embeddings and hasattr(resp.embeddings[0], "values"):
                emb = list(resp.embeddings[0].values)
            elif isinstance(resp, dict) and "embedding" in resp:
                emb = resp["embedding"]
            elif hasattr(resp, "embedding"):
                emb = resp.embedding
            else:
                raise ValueError("Invalid embedding response structure from Gemini")

            if not isinstance(emb, list) or not emb:
                raise ValueError("Invalid or empty embedding vector from Gemini")
            embeddings.append(emb)

        # Validate all vectors have the same dimension
        if embeddings:
            dim = len(embeddings[0])
            for e in embeddings:
                if len(e) != dim:
                    raise ValueError("Embedding dimension mismatch")
        return embeddings
    except Exception as e:
        # Propagate as a 502 Bad Gateway – upstream can decide retry logic
        raise HTTPException(status_code=502, detail=f"Embedding generation failed: {str(e)}")

def cosine_similarity(a: List[float], b: List[float]) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0
    if np is not None:
        a_arr = np.array(a, dtype=float)
        b_arr = np.array(b, dtype=float)
        norm_a = np.linalg.norm(a_arr)
        norm_b = np.linalg.norm(b_arr)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(np.dot(a_arr, b_arr) / (norm_a * norm_b))
    else:
        import math
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(y * y for y in b))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(dot / (norm_a * norm_b))

# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    validate_upload(file)
    temp_path = save_temp_file(file)
    try:
        pages = extract_text(temp_path, file.content_type)
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise HTTPException(status_code=400, detail="Failed to extract text: " + str(e))

    # Create Document entry (we need doc.id for chunks)
    doc = Document(
        user_id=user.id,
        filename=file.filename,
        filepath=temp_path,
        processed=False,
        metadata={"size": os.path.getsize(temp_path), "type": file.content_type},
    )
    db.add(doc)
    await db.commit()
    await db.refresh(doc)

    # Process each page: chunk and embed
    all_chunks = []
    for page in pages:
        page_num = page["page"]  # None for plain text
        page_chunks = chunk_text(page["text"])
        for idx, chunk in enumerate(page_chunks):
            all_chunks.append({
                "page_number": page_num,
                "chunk_index": idx,
                "text": chunk["text"],
            })
    # Prepare texts for embedding
    texts = [c["text"] for c in all_chunks]
    embeddings = await embed_texts(texts)
    # Save chunks with embeddings
    for idx, (c, emb) in enumerate(zip(all_chunks, embeddings)):
        chunk_obj = DocumentChunk(
            document_id=doc.id,
            page_number=c["page_number"],
            chunk_index=idx,
            text=c["text"],
            embedding=emb,
        )
        db.add(chunk_obj)
    doc.processed = True
    await db.commit()

    return {"document_id": doc.id, "filename": doc.filename, "chunks": len(all_chunks)}

@router.get("/documents")
async def list_documents(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    result = await db.execute(select(Document).where(Document.user_id == user.id))
    docs = result.scalars().all()
    return [
        {
            "id": d.id,
            "filename": d.filename,
            "uploaded_at": d.uploaded_at,
            "processed": d.processed,
            "metadata": d.metadata,
        }
        for d in docs
    ]

@router.delete("/{doc_id}")
async def delete_document(
    doc_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    # Ensure ownership
    result = await db.execute(select(Document).where(Document.id == doc_id, Document.user_id == user.id))
    doc = result.scalars().first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    # Delete file from disk
    if os.path.exists(doc.filepath):
        os.remove(doc.filepath)
    # Delete DB rows (chunks cascade)
    await db.delete(doc)
    await db.commit()
    return {"detail": "Document deleted"}

from pydantic import BaseModel

class QueryPayload(BaseModel):
    question: str
    top_k: int = 5

@router.post("/query")
async def query_knowledge(
    payload: QueryPayload,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    # Retrieve all chunks for the user
    result = await db.execute(
        select(DocumentChunk).join(Document).where(Document.user_id == user.id)
    )
    chunks: List[DocumentChunk] = result.scalars().all()
    if not chunks:
        raise HTTPException(status_code=400, detail="No knowledge base available for this user.")

    # Embed the question
    question_embeds = await embed_texts([payload.question])
    q_vec = question_embeds[0]

    # Compute similarity
    scored = []
    for chunk in chunks:
        sim = cosine_similarity(q_vec, chunk.embedding or [])
        scored.append((sim, chunk))
    scored.sort(key=lambda x: x[0], reverse=True)
    top_chunks = [c.text for _, c in scored[: payload.top_k] if _ > 0]

    # Build context for LLM
    context = "\n---\n".join(top_chunks)
    messages = [
        {"role": "user", "content": f"Answer the following question using only the provided context.\nContext:\n{context}\n\nQuestion: {payload.question}"}
    ]
    answer, model_name, provider_name = await ai_service.generate_response(messages, provider="gemini")

    # Build citations – we include document filename and chunk index
    citations = []
    for _, chunk in scored[: payload.top_k]:
        citations.append({"document_id": chunk.document_id, "chunk_index": chunk.chunk_index})

    return JSONResponse(
        content={
            "answer": answer,
            "model": model_name,
            "provider": provider_name,
            "citations": citations,
        }
    )
