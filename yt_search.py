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


async def join_and_play(message, query):
    if not message.author.voice or not message.author.voice.channel:
        await message.channel.send("You're not in a voice channel, mate.")
        return

    voice_channel = message.author.voice.channel

    vc: discord.VoiceClient = message.guild.voice_client

    if vc and vc.channel != voice_channel:
        await vc.move_to(voice_channel)
    elif not vc:
        try:
            vc = await voice_channel.connect()
        except discord.ClientException as e:
            await message.channel.send("Failed to connect to the voice channel.")
            print(f"Voice connection error: {e}")
            return

    with YoutubeDL(YDL_OPTIONS) as ydl:
        try:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)[
                'entries'][0]
            audio_url = info['url']
            title = info['title']
        except Exception as e:
            await message.channel.send("Error retrieving video.")
            print(f"YDL Error: {e}")
            return

    await message.channel.send(f"Now playing: **{title}**")

    loop = asyncio.get_event_loop()

    def after_playing(err):
        if err:
            print(f"Playback error: {err}")
        asyncio.run_coroutine_threadsafe(vc.disconnect(), loop)

    try:
        vc.stop()
        vc.play(discord.FFmpegPCMAudio(audio_url, **
                FFMPEG_OPTIONS), after=after_playing)
    except Exception as e:
        await message.channel.send("Failed to play the audio.")
        print(f"Playback setup error: {e}")
