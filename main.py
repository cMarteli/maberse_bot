# Markus Bot
# Version 0.02
# Author: Glitch
# Modified March, 29, 2023

from webserver import keep_alive #needed for replit hosting

import os
import discord
import responses

TOKEN = os.environ['BOT_TOKEN'] #secret token is stored in replit

GREET_CHANNEL_ID = 432542755785408515 # this is the id of the "generalis" channel


async def send_message(message, user_message, is_private):
  try:
    response = responses.handle_response(user_message)
    await message.author.send(
      response) if is_private else await message.channel.send(response)

  except Exception as e:
    print(e)

# @TODO: required by discord, intents.all() might be a bad practice but the bot only has limited permissions
# need o verify how these differ from the permissions given from the bot portal
def run_discord_bot():
  intents = discord.Intents.all()
  intents.members = True
  client = discord.Client(intents=intents)

  @client.event
  async def on_member_join(member):
    # Greets a new member joining the server
    channel = client.get_channel(GREET_CHANNEL_ID)
    # Replace the message content as desired
    message = "Howdy, howdy!"
    await channel.send(f"{message} {member.mention}")

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

    if user_message.startswith('?'):
      user_message = user_message[1:]
      await send_message(message, user_message, is_private=True)
    else:
      await send_message(message, user_message, is_private=False)

  client.run(TOKEN)


#Bottom of Main.py

keep_alive()

TOKEN = os.environ['BOT_TOKEN']

run_discord_bot()