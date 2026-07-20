from flask import Flask, request, jsonify, render_template
from agent import Agent
from llm_client import LLMClient
from conversation_context import ConversationContext
from tools.tools import tools

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
    return jsonify({"reply": reply})
    

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

print("Server running on http://localhost:5000")
app.run(port=5000)