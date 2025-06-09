# Markus Bot
# Version 0.4
# Author: Glitch
# Updated: May 17, 2025

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import Responses
import asyncio
from Player import get_queue  # Import this to check if queue is empty

# --- Load Config ---
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
GREET_CHANNEL_ID = 432542755785408515  # "generalis"
WELCOME_MESSAGE = "Howdy, howdy!"

# --- Bot Setup ---
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True
from soundmap import load_user_sounds

bot = commands.Bot(command_prefix='!', intents=intents)

user_sound_map = load_user_sounds()  # user_id: sound_filename

# --- Voice Join Sound Trigger ---
@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:
        sound_filename = user_sound_map.get(member.id)
        if not sound_filename:
            return  # No sound assigned to this user

        try:
            channel = after.channel
            vc = member.guild.voice_client

            if not vc or not vc.is_connected():
                vc = await channel.connect()
            else:
                await vc.move_to(channel)

            if not vc.is_playing():
                sound_path = os.path.join("sounds", sound_filename)
                if not os.path.exists(sound_path):
                    print(f"[WARN] Sound file not found: {sound_path}")
                    return

                audio_source = discord.FFmpegPCMAudio(sound_path)
                vc.play(audio_source)

                while vc.is_playing():
                    await asyncio.sleep(1)

                # Disconnect only if no queue exists
                queue = get_queue(member.guild.id)
                if not queue and not vc.is_playing():
                    await vc.disconnect()

        except Exception as e:
            print(f"[ERROR] Failed to play sound for user {member.id}: {e}")


# --- Bot Ready ---
@bot.event
async def on_ready():
    print(f"[INFO] {bot.user} is now running!")

# --- Greet New Members ---
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(GREET_CHANNEL_ID)
    if channel:
        await channel.send(f"{WELCOME_MESSAGE} {member.mention}")
    else:
        print("[WARN] Greet channel not found.")

# --- Message Handling ---
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    print(f"{message.author} said: '{message.content.strip()}' ({message.channel})")
    await send_message(message)


async def send_message(message: discord.Message):
    try:
        response = await Responses.handle_response(message)
        if response:
            await message.channel.send(response)
    except Exception as e:
        print(f"[ERROR] Failed to process message: {e}")

# --- Run Bot ---
if __name__ == '__main__':
    try:
        bot.run(TOKEN)
    except Exception as e:
        print(f"[CRITICAL] Failed to start bot: {e}")
