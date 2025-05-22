# player.py
import os
import asyncio
import discord
from yt_dlp import YoutubeDL

DOWNLOAD_DIR = 'downloads'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

YDL_OPTIONS = {
    'format': 'bestaudio[abr<=96]/bestaudio/best',
    'noplaylist': True,
    'quiet': True,
    'default_search': 'ytsearch',
    'extract_flat': False,
    'outtmpl': f'{DOWNLOAD_DIR}/%(id)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '96',
    }],
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

    try:
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
            video_id = info['id']
            title = info['title']

            # Download and convert to mp3
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=True)
            file_path = os.path.splitext(info['_filename'])[0] + '.mp3'
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Audio file not found: {file_path}")

    except Exception as e:
        await message.channel.send(f"Error retrieving or processing video: {e}")
        return

    queue = get_queue(guild_id)
    is_playing = vc.is_playing()
    queue.append((title, file_path))

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
        await asyncio.sleep(2)
        if not get_queue(guild.id) and not vc.is_playing():
            await vc.disconnect()
        return

    title, file_path = queue.pop(0)
    await text_channel.send(f"Now playing: **{title}**")

    def after_playing(err):
        if err:
            print(f"Playback error: {err}")
            asyncio.run_coroutine_threadsafe(text_channel.send(f"Playback error: {err}"), main_loop)
        try:
            future = asyncio.run_coroutine_threadsafe(
                play_next(guild, text_channel), main_loop
            )
            future.result()
        except Exception as e:
            print(f"Error in after_playing: {e}")

    vc.play(discord.FFmpegPCMAudio(file_path, **FFMPEG_OPTIONS), after=after_playing)


def clear_queue(guild_id):
    song_queues.pop(guild_id, None)


async def skip_song(guild):
    vc: discord.VoiceClient = guild.voice_client
    if vc and vc.is_playing():
        vc.stop()  # Triggers after_playing
        return True
    elif vc and not vc.is_playing() and not get_queue(guild.id):
        await vc.disconnect()
    return False
