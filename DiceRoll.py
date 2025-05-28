import random
import re


class DiceRoller:
    def __init__(self):
        pass

    def roll(self, roll_string: str) -> str:
        # Remove whitespace
        roll_string = roll_string.replace(" ", "")

        # Pattern to match formats like: 2*d6+4, 3d10-2, d20+1
        pattern = r'(?:(\d+)\*?d)?(\d+)([+-]\d+)?$'
        match = re.fullmatch(pattern, roll_string)

        if not match:
            return "Invalid roll format. Use like `2*d6+3`, `1d20-1`, or `3d10`."

        num_rolls = int(match.group(1)) if match.group(1) else 1
        sides = int(match.group(2))
        modifier = int(match.group(3)) if match.group(3) else 0

        try:
            rolls = [random.randint(1, sides) for _ in range(num_rolls)]
            total = sum(rolls)
            final_total = total + modifier

            rolls_str = ', '.join(str(r) for r in rolls)
            if modifier:
                return f"{rolls_str} [sum: {total} {match.group(3)} = {final_total}]"
            else:
                return f"{rolls_str} [sum: {total}]"
        except Exception as e:
            return f"Error rolling dice: {e}"
