from flask import Flask, request, jsonify, render_template
from agent import Agent
from llm_client import LLMClient
from conversation_context import ConversationContext
from tools.tools import tools
from document_indexer import index_document, list_documents
import os
import requests

app = Flask(__name__)

context = ConversationContext()
agent = Agent(LLMClient(), context, tools=tools)

@app.route("/")
def home():
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True)
    if not data or "message" not in data:
        return jsonify({"error": "Request must be JSON with a 'message' field"}), 400

    user_message = data["message"]
    if not isinstance(user_message, str) or not user_message.strip():
        return jsonify({"error": "'message' must be a non-empty string"}), 400

    reply = agent.process_message(user_message)
    context.save()
    return jsonify({
        "reply": reply,
        "input_tokens": context.input_tokens,
        "output_tokens": context.output_tokens,
        "cost": context.get_cost()
    })
    

@app.route("/new", methods=["POST"])
def new_game(): 
    context.messages = [context.assemble_system_prompt()]
    context.input_tokens = 0
    context.output_tokens = 0
    return jsonify({"status": "new adventure started"})

@app.route("/load", methods=["POST"])
def load_game(): 
    if context.load():
        return jsonify({"status": "adventure loaded"})
    else:
        return jsonify({"status": "no save found"})
    
@app.route("/stats", methods=["GET"])
def stats():
    return jsonify({
        "input_tokens": context.input_tokens,
        "output_tokens": context.output_tokens,
        "cost": context.get_cost()
    })

ALLOWED_EXTENSIONS = (".txt", ".md")
MAX_UPLOAD_CHARS = 50_000


@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file was sent"}), 400

    file = request.files["file"]
    filename = file.filename or ""

    if not filename.lower().endswith(ALLOWED_EXTENSIONS):
        return jsonify({"error": "Only .txt and .md files are accepted"}), 400

    try:
        text = file.read().decode("utf-8")
    except UnicodeDecodeError:
        return jsonify({"error": "The file is not readable as UTF-8 text"}), 400

    if not text.strip():
        return jsonify({"error": "The file is empty"}), 400

    text = text[:MAX_UPLOAD_CHARS]
    document_id = os.path.splitext(os.path.basename(filename))[0]

    try:
        chunks = index_document(document_id, text)
    except requests.exceptions.RequestException:
        return jsonify({"error": "The embeddings service is unavailable"}), 503

    return jsonify({"document": document_id, "chunks": chunks})


@app.route("/documents", methods=["GET"])
def documents():
    return jsonify({"documents": list_documents()})

print("Server running on http://localhost:5000")
app.run(port=5000)