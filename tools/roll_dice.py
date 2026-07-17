from .tool import Tool
import random

def dice(num_dice, sides, modifier=0):

    print(f"[TOOL] rolling {num_dice}d{sides}+{modifier}")

    rolls = [random.randint(1,sides) for _ in range(num_dice)]
    total = sum(rolls) + modifier
    sign = f"+{modifier}" if modifier > 0 else (str(modifier) if modifier < 0 else "")
    return f"Rolled {num_dice}d{sides}{sign}: {rolls} -> total {total}"
    


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
            },

            "modifier": {
                "type": "integer",
                "description": "Flat bonus or penalty added to the total, e.g. 5 for 1d20+5. Default 0."
            }
        },
        "required": ["num_dice", "sides"]
    },
    callback=dice
)