#responses.py
import random
import myjokes


#rolls a die maxVal is the number of sides
def diceRoll(maxVal):
  return str(random.randint(1, maxVal))


def handle_response(message) -> str:
  p_message = message.lower()

  if p_message.startswith('!roll'):
    _, roll_string = p_message.split(' ', 1)
    if '*' in roll_string:
      # Split the roll string by the * symbol to get the number of rolls and the type of dice
      num_rolls, dice_type = roll_string.split('*')
      num_rolls = int(num_rolls.strip())
    else:
      # If no dice type is specified, assume d6
      num_rolls = 1
      if len(roll_string.strip()) == 0:
        dice_type = 'd6'
      else:
        dice_type = roll_string.strip()

    # check which dice to roll
    if 'd10' in dice_type:
      rolls = [diceRoll(10) for i in range(num_rolls)]
      return ', '.join(str(r) for r in rolls)
    elif 'd20' in dice_type:
      rolls = [diceRoll(20) for i in range(num_rolls)]
      return ', '.join(str(r) for r in rolls)
    else:
      rolls = [diceRoll(6) for i in range(num_rolls)]
      return ', '.join(str(r) for r in rolls)

  if 'how are you' in p_message:
    return "I'm good thanks for asking!"

  if 'joke' in p_message:
    joke = myjokes.tell_joke()
    return str("Sure mate, here's a good one:\n" + joke)

  if 'legal advice' in p_message:
    return str(
      "Sorry, I'm not programmed to give legal advice, mate. Please check with Maberse (real)"
    )
