# player.py
import asyncio
import discord
from yt_dlp import YoutubeDL

YDL_OPTIONS = {
    'format': 'bestaudio[abr<=96]/bestaudio/best',
    'noplaylist': 'True',
    'quiet': True,
    'default_search': 'ytsearch',
    'extract_flat': False
}

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

song_queues = {}
main_loop = None


def get_queue(guild_id):
    return song_queues.setdefault(guild_id, [])


async def join_and_play(message, query):
    guild_id = message.guild.id
    voice_channel = message.author.voice.channel
    vc: discord.VoiceClient = message.guild.voice_client

    if vc and vc.channel != voice_channel:
        await vc.move_to(voice_channel)
    elif not vc:
        try:
            vc = await voice_channel.connect()
        except discord.ClientException:
            await message.channel.send("Failed to connect to the voice channel.")
            return

    with YoutubeDL(YDL_OPTIONS) as ydl:
        try:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)[
                'entries'][0]
            audio_url = info['url']
            title = info['title']
        except Exception:
            await message.channel.send("Error retrieving video.")
            return

    queue = get_queue(guild_id)
    is_playing = vc.is_playing()
    queue.append((title, audio_url))

    if is_playing:
        await message.channel.send(f"Queued: **{title}**")
    else:
        await play_next(message.guild, message.channel)


async def play_next(guild, text_channel):
    global main_loop
    if main_loop is None:
        main_loop = asyncio.get_running_loop()

    queue = get_queue(guild.id)
    vc: discord.VoiceClient = guild.voice_client

    if not vc:
        return

    if not queue:
        await asyncio.sleep(2)  # Grace period before disconnecting
        if not get_queue(guild.id) and not vc.is_playing():
            await vc.disconnect()
        return

    title, audio_url = queue.pop(0)
    await text_channel.send(f"Now playing: **{title}**")

    def after_playing(err):
        if err:
            print(f"Playback error: {err}")
        try:
            future = asyncio.run_coroutine_threadsafe(
                play_next(guild, text_channel), main_loop
            )
            future.result()
        except Exception as e:
            print(f"Error in after_playing: {e}")

    vc.play(discord.FFmpegPCMAudio(audio_url, **
            FFMPEG_OPTIONS), after=after_playing)


def clear_queue(guild_id):
    song_queues.pop(guild_id, None)


async def skip_song(guild):
    vc: discord.VoiceClient = guild.voice_client
    if vc and vc.is_playing():
        vc.stop()  # Triggers after_playing, which handles disconnection
        return True
    elif vc and not vc.is_playing() and not get_queue(guild.id):
        await vc.disconnect()
    return False
