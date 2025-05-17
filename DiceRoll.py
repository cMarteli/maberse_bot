import random


class DiceRoller:
    def __init__(self):
        pass

    def roll(self, roll_string: str) -> str:
        # Default values
        num_rolls = 1
        sides = 6

        if '*' in roll_string:
            try:
                num_rolls_str, dice_type = roll_string.split('*')
                num_rolls = int(num_rolls_str.strip())
            except ValueError:
                return "Invalid roll format. Use format like `2*d10` or `d20`."
        else:
            dice_type = roll_string.strip()

        # Detect sides from dice type
        if 'd10' in dice_type:
            sides = 10
        elif 'd20' in dice_type:
            sides = 20
        elif 'd6' in dice_type or dice_type.startswith('d'):
            sides = 6

        try:
            rolls = [str(random.randint(1, sides)) for _ in range(num_rolls)]
            return ', '.join(rolls)
        except Exception as e:
            return f"Error rolling dice: {e}"
