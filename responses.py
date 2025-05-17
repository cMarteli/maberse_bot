# responses.py
from player import join_and_play, skip_song, clear_queue
import random
import weather
import myjokes


def dice_roll(sides: int) -> str:
    return str(random.randint(1, sides))


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

        rolls = [dice_roll(sides) for _ in range(num_rolls)]
        return ', '.join(rolls)

    if 'how are you' in p_message and not p_message.startswith('!'):
        return "I'm good, thanks for asking!"

    if 'thanks mark' in p_message and not p_message.startswith('!'):
        return "That's okay, always happy to help out a mate!"

    if 'joke' in p_message and not p_message.startswith('!'):
        joke = await myjokes.tell_joke()
        return f"Yeah, I know a joke actually:\n{joke}"

    if 'legal advice' in p_message and not p_message.startswith('!'):
        return "Sorry, I'm not programmed to give legal advice. Please consult Maberse(Real)."

    if 'weather' in p_message:
        temperature = await weather.getweather()
        place = weather.getLocation()
        return f"It's currently {temperature} degrees in {place}, mate."

    if p_message.startswith("!play "):
        query = message.content.strip()[6:].strip()
        await join_and_play(message, query)
        return None  # Audio action, no text reply

    if p_message.startswith("!leave") or p_message.startswith("!stop"):
        voice_client = message.guild.voice_client
        if voice_client and voice_client.is_connected():
            clear_queue(message.guild.id)
            await voice_client.disconnect()
            return "I'm off, you lads have a good night."

    if p_message.startswith("!skip"):
        voice_client = message.guild.voice_client
        if await skip_song(message.guild):
            return "Sorry mate, let me skip that one."
        elif voice_client and voice_client.is_connected():
            clear_queue(message.guild.id)
            await voice_client.disconnect()
            return "There's nothing playing to skip. I'm off."
        else:
            return "I'm not even in a voice channel, mate."

    return "Not sure about that one, sorry."
