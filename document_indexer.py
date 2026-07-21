"""
Runtime document indexing.

Adds user-uploaded documents to the existing embeddings index,
without regenerating the whole knowledge base.
"""
import os
import json
import logging

from config import CHUNK_SIZE, EMBEDDINGS_FILE
from document_chunker import split_text
from embeddings_client import EmbeddingsClient

logger = logging.getLogger(__name__)


def load_index():
    """Returns all indexed chunks, or an empty list if nothing is indexed yet."""
    if not os.path.exists(EMBEDDINGS_FILE):
        return []
    with open(EMBEDDINGS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_index(chunks):
    with open(EMBEDDINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(chunks, f)


def index_document(document_id, text):
    """
    Chunks, embeds and appends a document to the index.
    Re-uploading the same document replaces its old chunks.
    Returns the number of chunks added.
    """
    client = EmbeddingsClient()
    chunks = split_text(text, CHUNK_SIZE)

    index = load_index()
    index = [c for c in index if c.get("document_id") != document_id]

    for i, chunk in enumerate(chunks):
        index.append({
            "document_id": document_id,
            "chunk_index": i,
            "content": chunk,
            "source": "upload",
            "embedding": client.get_embedding(chunk)
        })

    save_index(index)
    logger.info(f"Indexed document '{document_id}': {len(chunks)} chunks")
    return len(chunks)


def list_documents():
    """Returns the ids of uploaded documents currently in the index."""
    ids = {c["document_id"] for c in load_index() if c.get("source") == "upload"}
    return sorted(ids)