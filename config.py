"""
Application configuration.

Contains model settings, API endpoints, pricing,
and RAG parameters (chunking, retrieval threshold).
"""


import os
from dotenv import load_dotenv
import logging

load_dotenv()
API_KEY = os.getenv("API_KEY")
CHUNK_SIZE = 500
EMBEDDINGS_MODEL = "nomic-embed-text"
EMBEDDINGS_ENDPOINT = "http://localhost:11434/api/embed"
EMBEDDINGS_FILE = "embeddings.json"
AZURE_ENDPOINT = "https://ai-academy-foundry.services.ai.azure.com/openai/v1"
MODEL_NAME = "gpt-5-mini"

INPUT_TOKEN_PRICE_PER_MILLION = 2.0
OUTPUT_TOKEN_PRICE_PER_MILLION = 10.0
MAX_CONTEXT_TOKENS = 4000
SIMILARITY_THRESHOLD = 0.5

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    encoding="utf-8"
)
