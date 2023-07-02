# responses.py
import random
import weather
import myjokes


# Rolls a die with maxVal sides
def diceRoll(maxVal):
  return str(random.randint(1, maxVal))


async def handle_response(message) -> str:
  p_message = message.lower()

  if p_message.startswith('!help'):
    return "Hey mate, I'm Maberse (Bot). I can roll dice, tell jokes, and tell you the weather. Try typing !roll 2d10 to roll two 10-sided dice, type \'joke\' to hear a joke. If you want to know the weather, just ask me!"

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

    # Check which dice to roll
    if 'd10' in dice_type:
      rolls = [diceRoll(10) for _ in range(num_rolls)]
      return ', '.join(str(r) for r in rolls)
    elif 'd20' in dice_type:
      rolls = [diceRoll(20) for _ in range(num_rolls)]
      return ', '.join(str(r) for r in rolls)
    else:
      rolls = [diceRoll(6) for _ in range(num_rolls)]
      return ', '.join(str(r) for r in rolls)

  if 'how are you' in p_message:
    return "I'm good, thanks for asking!"

  if 'thanks mark' in p_message:
    return "That's okay, always happy to help out a mate!"

  if 'joke' in p_message:
    joke = await myjokes.tell_joke()
    return "Sure mate, here's a good one:\n" + joke

  if 'legal advice' in p_message:
    return "Sorry, I'm not programmed to give legal advice. Please consult Maberse(Real)."

  if 'weather' in p_message:
    temperature = await weather.getweather()
    place = weather.getLocation()
    return "It's currently " + str(
      temperature) + " degrees in " + place + ", mate."
