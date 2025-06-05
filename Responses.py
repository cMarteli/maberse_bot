# Responses.py
from Player import join_and_play, skip_song, clear_queue
from DiceRoll import DiceRoller
import Weather
import MyJokes

roller = DiceRoller()


async def handle_response(message) -> str | None:
    content = message.content
    p_message = content.lower().strip()

    # Fast command routing
    if p_message.startswith('!'):
        command = p_message.split(' ', 1)[0]

        if command == '!help':
            return (
                "Hey mate, I'm Maberse (Bot). I can roll dice, tell jokes, and tell you the weather.\n"
                "Try typing `!roll 2*d10` to roll two 10-sided dice, `joke` to hear a joke.\n"
                "If you want to know the weather, just ask me!\n"
                "You can also `!play <YouTube search>` to play music in your voice channel."
            )

        elif command in ('!roll', '!r', '!ra'):
            roll_string = p_message[len(command):].strip() or 'd6'
            is_assist = (command == '!ra')
            return roller.roll(roll_string, assist=is_assist)

        elif command in ('!play', '!p'):
            query = content[6:].strip()  # Use original for casing
            await join_and_play(message, query)
            return None

        elif command in ('!leave', '!l'):
            vc = message.guild.voice_client
            if vc and vc.is_connected():
                clear_queue(message.guild.id)
                await vc.disconnect()
                return "I'm off, you lads have a good night."

        elif command in ('!skip', '!s'):
            vc = message.guild.voice_client
            if await skip_song(message.guild):
                return "Sorry mate, let me skip that one."
            elif vc and vc.is_connected():
                clear_queue(message.guild.id)
                await vc.disconnect()
                return "There's nothing playing to skip. I'm off."
            else:
                return "I'm not even in a voice channel, mate."

        return "Not sure about that one, sorry."

    # Non-command keyword responses
    if 'joke' in p_message:
        joke = await MyJokes.tell_joke()
        return f"Yeah, I know a joke actually:\n{joke}"

    if 'weather' in p_message:
        temperature = await Weather.getweather()
        place = Weather.getLocation()
        return f"It's currently {temperature} degrees in {place}, mate."

    if 'how are you' in p_message:
        return "I'm good, thanks for asking!"

    if 'thanks mark' in p_message:
        return "That's okay, always happy to help out a mate!"

    if 'legal advice' in p_message:
        return "Sorry, I'm not programmed to give legal advice. Please consult Maberse(Real)."

    return "Not sure about that one, sorry."
