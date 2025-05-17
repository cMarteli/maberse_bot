# Markus Bot
# Version 0.4
# Author: Glitch
# Updated: May 17, 2025

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import Responses

# --- Load Config ---
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
GREET_CHANNEL_ID = 432542755785408515  # "generalis"
WELCOME_MESSAGE = "Howdy, howdy!"

# --- Bot Setup ---
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f"[INFO] {bot.user} is now running!")


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(GREET_CHANNEL_ID)
    if channel:
        await channel.send(f"{WELCOME_MESSAGE} {member.mention}")
    else:
        print("[WARN] Greet channel not found.")


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

if __name__ == '__main__':
    try:
        bot.run(TOKEN)
    except Exception as e:
        print(f"[CRITICAL] Failed to start bot: {e}")
