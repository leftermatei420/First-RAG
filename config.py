"""
Application configuration.

This module contains all configurable settings used by the AI agent.

Future exercises may extend this file with:
- Model configuration
- API credentials
- Prompt templates
- Embedding settings
- Logging configuration
"""


import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
MODEL_NAME = "qwen3:8b"
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
