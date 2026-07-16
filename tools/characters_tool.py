from .tool import Tool

CHARACTERS = [
    {"name": "wizard", "details": "Master of arcane magic, low HP, high damage, range combat"},
    {"name": "warrior", "details": "Master of power, high HP, medium damage, close combat"},
    {"name": "assasin", "details": "Master shadows, very low HP, fatal damage, close combat"},  
]

def characters(role):

    for c in CHARACTERS:
        if c["name"] == role:
            return c

    return f"Role '{role}' not found. Available: wizard, warrior, assasin"


characters_tool = Tool(
    name = "characters",
    description = (
        "Lets the player choose their character class at the start of an "
        "adventure. Returns the attributes and combat style of the chosen "
        "class. Use it when the player wants to start a game or pick a role."
    ),
    parameters = {
        "type": "object",
        "properties": {
            "role": {
                "type": "string",
                "description": (
                    "The character class chosen by the player. "
                    "One of: wizard, warrior, assasin"
                )
            }
        },
        "required": ["role"]
    },
    callback=characters
)