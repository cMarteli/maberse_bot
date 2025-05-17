# Markus Bot
# Version 0.11
# Author: Glitch
# Modified March, 29, 2023

from dotenv import load_dotenv
# TODO; check if still needed to keep server from timing out
from WebServer import keep_alive

import os
import discord
import Responses

load_dotenv()  # Load environment variables from .env

TOKEN = os.getenv('BOT_TOKEN')
WELCOME_MESSAGE = "Howdy, howdy!"
GREET_CHANNEL_ID = 432542755785408515  # "generalis" channel

# allows bot to send messages


async def send_message(message):
    try:
        response = await Responses.handle_response(message)
        if response is not None:
            await message.channel.send(response)
    except Exception as e:
        print(e)


def run_discord_bot():
    intents = discord.Intents.all()
    intents.members = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_member_join(member):
        channel = client.get_channel(GREET_CHANNEL_ID)
        await channel.send(f"{WELCOME_MESSAGE} {member.mention}")

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content.strip())
        channel = str(message.channel)

        print(f"{username} said: '{user_message}' ({channel})")

        await send_message(message)

    client.run(TOKEN)


keep_alive()
run_discord_bot()
