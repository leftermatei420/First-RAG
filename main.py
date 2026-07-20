"""
Application entry point.

This module provides a simple command-line
interface for interacting with the agent.
"""

from agent import Agent
from llm_client import LLMClient
from conversation_context import ConversationContext
from tools.tools import tools
from rich.console import Console
from rich.panel import Panel

console = Console()

def show_menu():
    console.print()
    console.print("[bold #d4a017]1)[/] New adventure")
    console.print("[bold #d4a017]2)[/] Continue")
    console.print("[bold #d4a017]3)[/] Exit")

    while True:
        choice = console.input("[bold #e07b39]Choose ➤ [/]")
        if choice in ("1", "2", "3"):
            return choice
        console.print("[dim]The barkeep squints. Pick 1, 2, or 3.[/]")

def main():
    context = ConversationContext()

    choice = show_menu()

    if choice == "3":
        return
    if choice == "2":
        if context.load():
            console.print("[#d4a017]The barkeep nods as you enter. \"Back again, adventurer? Your tale awaits.\"[/]")   
        else:
            console.print("[dim #8b7355]No saved adventure found. A blank page awaits — starting fresh.[/]")   

    llm_client = LLMClient()

    agent = Agent(llm_client, context, tools=tools)

    console.print(Panel.fit(
        "[bold #d4a017]⚔  VALERIA  ⚔[/]\n"
        "[#8b7355]The Gilded Flagon awaits, adventurer.[/]\n"
        "[dim]Type 'exit' to leave the tavern.[/]",
        border_style="#d4a017"
    ))

    try:
        while True:
            console.print()
            user_input = console.input("[bold #e07b39]You ➤ [/]")

            if user_input.lower() == "exit":
                console.print("[dim #8b7355]The tavern door closes behind you...[/]")
                context.save()
                break
            if user_input.lower().startswith("export "):
                filename = user_input.split(" ", 1)[1].strip()
                context.save(filename)
                console.print(f"[#d4a017]Adventure exported to {filename}[/]")
                continue

            if user_input.lower().startswith("import "):
                filename = user_input.split(" ", 1)[1].strip()
                if context.load(filename):
                    console.print(f"[#d4a017]Adventure imported from {filename}[/]")
                else:
                    console.print(f"[dim #8b7355]Could not load {filename} — file missing or corrupted.[/]")
                continue
            with console.status("[#9b59b6]Garcea consults the fates...[/]", spinner="dots12"):
                response = agent.process_message(user_input)

            console.print()
            console.print("[bold #9b59b6]🎲 Garcea:[/]", response)
    except KeyboardInterrupt:
        console.print("\n[dim #8b7355]The tavern door slams shut...[/]")
        context.save()


if __name__ == "__main__":
    main()
