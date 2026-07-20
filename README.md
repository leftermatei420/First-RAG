# Valeria — AI Dungeon Master

An AI agent that runs D&D adventures in the kingdom of Valeria.
Features: tool calling (dice, characters), RAG knowledge retrieval,
session save/load, token & cost tracking. CLI and web interface.

## Installation

pip install -r requirements.txt

Create a `.env` file with:
API_KEY=your_azure_api_key

Requires Ollama running locally with the embedding model:
ollama pull nomic-embed-text

Generate embeddings once:
python embedding_generator.py

## Running

CLI:  python main.py
Web:  python web.py  (then open http://localhost:5000)

## Usage examples

You ➤ I want to be a wizard
🎲 Garcea: Excellent — a Wizard...
    
You ➤ roll for initiative
[TOOL] rolling 1d20