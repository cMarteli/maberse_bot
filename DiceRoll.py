import random
import re


class DiceRoller:
    MAX_ROLLS = 100
    MAX_SIDES = 100

    def __init__(self):
        pass

    def roll(self, roll_string: str, assist: bool = False) -> str:
        roll_string = roll_string.replace(" ", "")
        pattern = r'(\d*)\*?d(\d+)([+-]\d+)?$'
        match = re.fullmatch(pattern, roll_string)

        if not match:
            return "Invalid roll format. Try `2d6`, `3*d10+1`, or `d20-2`."

        num_rolls = int(match.group(1)) if match.group(1) else 1
        sides = int(match.group(2))
        modifier = int(match.group(3)) if match.group(3) else 0

        if num_rolls > self.MAX_ROLLS:
            return f"Too many dice rolls requested: {num_rolls}. Max is {self.MAX_ROLLS}."

        if sides > self.MAX_SIDES:
            return f"Dice size too large: d{sides}. Max is d{self.MAX_SIDES}."

        try:
            rolls = [random.randint(1, sides) for _ in range(num_rolls)]
            rolls_str = '+'.join(str(r) for r in rolls)

            if assist:
                points = [(2 if r <= 5 else 0) for r in rolls]
                total = sum(points)
                breakdown = ' + '.join(str(p) for p in points)
                return f"Assist Roll: {rolls_str}\nScored: {breakdown} = {total}"
            else:
                total = sum(rolls)
                final_total = total + modifier
                if modifier:
                    return f"{rolls_str}\n[{total} {match.group(3)} = {final_total}]"
                else:
                    return f"{rolls_str}\n[{total}]"

        except Exception as e:
            return f"Error rolling dice: {e}"
