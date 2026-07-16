from .tool import Tool
import random

def dice(num_dice, sides):

    rolls = []

    for x in range(num_dice):
        roll = random.randint(1, sides)
        rolls.append(roll)

    total = sum(rolls)
    return f"Rolled {num_dice}d{sides}: {rolls} -> total {total}"


roll_dice = Tool(
    name="roll_dice",
    description=(
        "Rolls dice for D&D gameplay. Use it whenever a dice roll is needed: "
        "ability checks, attacks, damage, initiative. Returns individual "
        "rolls and the total."
    ),
    parameters={
        "type": "object",
        "properties": {
            "num_dice": {
                "type": "integer",
                "description": "How many dice to roll, e.g. 2 for 2d6"
                
            },
            "sides": {
                "type": "integer",
                "description": "Number of sides per die, e.g. 6 for d6, 20 for d20"
            }
        },
        "required": ["num_dice", "sides"]
    },
    callback=dice
)