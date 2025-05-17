# responses.py
from yt_search import join_and_play
import random
import weather
import myjokes


# Rolls a die with maxVal sides
def diceRoll(maxVal):
    return str(random.randint(1, maxVal))


async def handle_response(message) -> str | None:
    p_message = message.content.lower().strip()

    if p_message.startswith('!help'):
        return (
            "Hey mate, I'm Maberse (Bot). I can roll dice, tell jokes, and tell you the weather.\n"
            "Try typing `!roll 2*d10` to roll two 10-sided dice, `joke` to hear a joke.\n"
            "If you want to know the weather, just ask me!\n"
            "You can also `!play <YouTube search>` to play music in your voice channel."
        )

    if p_message.startswith('!roll'):
        try:
            _, roll_string = p_message.split(' ', 1)
        except ValueError:
            roll_string = ''

        if '*' in roll_string:
            num_rolls, dice_type = roll_string.split('*')
            num_rolls = int(num_rolls.strip())
        else:
            num_rolls = 1
            dice_type = roll_string.strip() if roll_string.strip() else 'd6'

        sides = 6
        if 'd10' in dice_type:
            sides = 10
        elif 'd20' in dice_type:
            sides = 20

        rolls = [diceRoll(sides) for _ in range(num_rolls)]
        return ', '.join(rolls)

    if 'how are you' in p_message:
        return "I'm good, thanks for asking!"

    if 'thanks mark' in p_message:
        return "That's okay, always happy to help out a mate!"

    if 'joke' in p_message:
        joke = await myjokes.tell_joke()
        return f"Yeah, I know a joke actually:\n{joke}"

    if 'legal advice' in p_message:
        return "Sorry, I'm not programmed to give legal advice. Please consult Maberse(Real)."

    if 'weather' in p_message:
        temperature = await weather.getweather()
        place = weather.getLocation()
        return f"It's currently {temperature} degrees in {place}, mate."

    if p_message.startswith("!play "):
        query = p_message[6:].strip()
        await join_and_play(message, query)
        return None  # Audio action, no text reply

    if p_message.startswith("!leave") or p_message.startswith("!stop"):
        voice_client = message.guild.voice_client
        if voice_client and voice_client.is_connected():
            await voice_client.disconnect()
            return "I'm off, you lads have a good night."
    else:
        return "I'm not connected to any voice channel."

    return "Not sure about that one, sorry."
