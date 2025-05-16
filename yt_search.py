import asyncio
import discord
from yt_dlp import YoutubeDL

YDL_OPTIONS = {
    'format': 'bestaudio[abr<=96]/bestaudio/best',  # Prefer <=96kbps audio
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
    voice_channel = message.author.voice.channel if message.author.voice else None

    if not voice_channel:
        await message.channel.send("You're not in a voice channel, mate.")
        return

    try:
        vc: discord.VoiceClient = await voice_channel.connect()
    except discord.ClientException:
        vc = discord.utils.get(message.guild.voice_clients)
        if not vc:
            await message.channel.send("Error joining voice channel.")
            return

    with YoutubeDL(YDL_OPTIONS) as ydl:
        try:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)[
                'entries'][0]
            audio_url = info['url']
        except Exception as e:
            await message.channel.send("Error retrieving video.")
            print(e)
            return

    title = info['title']

    # Capture the bot's asyncio loop properly
    loop = asyncio.get_event_loop()

    def after_playing(err):
        if err:
            print(f"Player error: {err}")
        else:
            # Schedule disconnect coroutine from non-async callback
            asyncio.run_coroutine_threadsafe(vc.disconnect(), loop)

    vc.stop()
    vc.play(discord.FFmpegPCMAudio(audio_url, **
            FFMPEG_OPTIONS), after=after_playing)
    await message.channel.send(f"Now playing: **{title}**")
