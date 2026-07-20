"""Core agent orchestration.
The agent coordinates communication between
the conversation context and the language model."""
import json
from utils import count_tokens
from embeddings_client import EmbeddingsClient
from config import SIMILARITY_THRESHOLD
import logging

logger = logging.getLogger(__name__)

class Agent:
    def __init__(self, llm_client, context, tools=None):
        self.llm_client = llm_client
        self.context = context
        self.tools = {tool.name: tool for tool in tools} if tools else {}
        self.embeddings_client = EmbeddingsClient()

    def _count_input(self):
        for msg in self.context.get_history():
            self.context.input_tokens += count_tokens(str(msg.get("content", "")))


    def _handle_tool_calls(self, tool_calls):
        results = []
        for tc in tool_calls:
            tool_name = tc["function"]["name"]
            arguments = json.loads(tc["function"]["arguments"])
            tool_id = tc["id"]
            logger.info(f"Tool call: {tool_name}({arguments})")

            tool = self.tools.get(tool_name)
            if tool:
                result = tool.callback(**arguments)
            else:
                result = f"Tool '{tool_name}' not found"

            results.append({
                "role": "tool",
                "tool_call_id": tool_id,
                "content": str(result)
            })
        return results

    def process_message(self, user_message):
        logger.info(f"User: {user_message}")
        self.context.add_message({
            "role": "user",
            "content": user_message
        })
        results = self.embeddings_client.semantic_search(user_message)
        results = [chunk for chunk in results if chunk["similarity"] > SIMILARITY_THRESHOLD]

        self.context.messages = [
            msg for msg in self.context.messages
            if not (msg["role"] == "system" and str(msg["content"]).startswith("Relevant knowledge"))
        ]

        if results:
            knowledge = "\n\n".join(chunk["content"] for chunk in results)
            self.context.add_message({
                "role": "system",
                "content": f"Relevant knowledge for this question:\n{knowledge}"
            })
        else:
            self.context.add_message({
                "role": "system",
                "content": (
                    "Relevant knowledge: none found in the knowledge base for this question. "
                    "Answer from your general instructions and world lore. If the question is about "
                    "specific rules or facts you don't have, say you don't know instead of inventing them."
                )
            })

        self.context.compress()
        self._count_input()
        response = self.llm_client.generate_response(
            self.context.get_history(),
            tools=list(self.tools.values())
        )

        message = response["message"]   
        self.context.output_tokens += count_tokens(str(message.get("content", "")))
        tool_calls = message.get("tool_calls", [])

        while tool_calls:
            self.context.add_message(message)

            tool_results = self._handle_tool_calls(tool_calls)
            for result in tool_results:
                self.context.add_message(result)

            self._count_input()

            response = self.llm_client.generate_response(
                self.context.get_history(),
                tools=list(self.tools.values())
            )
            message = response["message"]
            self.context.output_tokens += count_tokens(str(message.get("content", "")))
            tool_calls = message.get("tool_calls", [])

        self.context.add_message(message)

        print(f"Input tokens: {self.context.input_tokens}")
        print(f"Output tokens: {self.context.output_tokens}")
        print(f"Estimated cost: ${self.context.get_cost():.6f}")

        logger.info(f"Assistant: {message.get('content', '')}")
        return message.get("content", "")
