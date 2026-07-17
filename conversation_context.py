"""
Conversation memory management.

This module is responsible for storing and retrieving
messages exchanged between the user and the AI assistant.
"""
import os
import json
from config import INPUT_TOKEN_PRICE_PER_MILLION
from config import OUTPUT_TOKEN_PRICE_PER_MILLION
from config import MAX_CONTEXT_TOKENS
from utils import count_tokens



def load_file(path):
    try:
        with open(path, 'r', encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Warning: file not found: {path}")
        return ""

    
def load_registry(folder):
    path = os.path.join("knowledge", folder, "registry.json")
    with open(path, 'r', encoding="utf-8") as f:
        return json.load(f)
    
def load_always_load_docs(folder):
    sections = []
    docs = load_registry(folder)
    for doc in docs:
        if doc["always_load"]:
            path = os.path.join("knowledge", folder, doc["id"] + ".md")
            content = load_file(path)
            sections.append(f"# {doc['name']}\n{content}")
    return sections


class ConversationContext:

    def __init__(self):
        self.messages = [
            self.assemble_system_prompt()
        ]
        self.input_tokens = 0
        self.output_tokens = 0

    def get_cost(self):
        input_cost = self.input_tokens / 1_000_000 * INPUT_TOKEN_PRICE_PER_MILLION
        output_cost = self.output_tokens / 1_000_000 * OUTPUT_TOKEN_PRICE_PER_MILLION
        total = input_cost + output_cost
        return total

    def count_context_tokens(self):
        total = 0
        for msg in self.messages:
            total += count_tokens(str(msg.get("content", "")))
        return total

    def compress(self):
        while self.count_context_tokens() > MAX_CONTEXT_TOKENS:
            self.messages.pop(1)
        
    def assemble_system_prompt(self):
        sections = []
        for filename in os.listdir(os.path.join("knowledge", "prompts")):
            content = load_file(os.path.join("knowledge", "prompts", filename))
            sections.append(content)

        sections += load_always_load_docs("facts")
        sections += load_always_load_docs("procedures")

        full_prompt = "\n\n".join(sections)
        return {"role": "system", "content": full_prompt}


    def add_message(self, message):
        self.messages.append(message)

    def get_history(self):
        return self.messages
    
    def save(self, path="session.json"):
        data = {
            "messages": self.messages,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load(self, path="session.json"):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.messages = data["messages"]
            self.input_tokens = data["input_tokens"]
            self.output_tokens = data["output_tokens"]
            return True
        except FileNotFoundError:
            return False


    
