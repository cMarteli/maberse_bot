import random
import re


class DiceRoller:
    MAX_ROLLS = 100
    MAX_SIDES = 100

    def __init__(self):
        pass

    def roll(self, roll_string: str) -> str:
        roll_string = roll_string.replace(" ", "")

        # Pattern: [optional number][optional *]d[sides][optional +|-modifier]
        pattern = r'(\d*)\*?d(\d+)([+-]\d+)?$'
        match = re.fullmatch(pattern, roll_string)

        if not match:
            return "Invalid roll format. Use formats like `2*d6+3`, `d20-1`, or `3d10`."

        num_rolls = int(match.group(1)) if match.group(1) else 1
        sides = int(match.group(2))
        modifier = int(match.group(3)) if match.group(3) else 0

        if num_rolls > self.MAX_ROLLS:
            return f"Too many dice rolls requested: {num_rolls}. Maximum allowed is {self.MAX_ROLLS}."

        if sides > self.MAX_SIDES:
            return f"Dice size too large: d{sides}. Maximum allowed is d{self.MAX_SIDES}."

        try:
            rolls = [random.randint(1, sides) for _ in range(num_rolls)]
            total = sum(rolls)
            final_total = total + modifier

            rolls_str = '+'.join(str(r) for r in rolls)
            if modifier:
                return f"{rolls_str}\n[{total} {match.group(3)} = {final_total}]"
            else:
                return f"{rolls_str}\n[{total}]"
        except Exception as e:
            return f"Error rolling dice: {e}"
