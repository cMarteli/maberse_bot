from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import MyJokes
import Weather
import discord
import pytz

# --- Daily Message ---
async def send_daily_message(bot: discord.Client, channel_id: int):
    joke = await MyJokes.tell_joke()
    temperature = await Weather.getweather()
    place = Weather.getLocation()
    message = f"**Daily Update!**\n\n" \
              f"Here is your daily joke:\n{joke}\n\n" \
              f"The current weather in {place} is {temperature}°C."
    
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send(message)
    else:
        print(f"[WARN] Daily message channel not found: {channel_id}")


# --- Scheduler Setup ---
def start(bot: discord.Client, channel_id: int):
    scheduler = AsyncIOScheduler(timezone=pytz.timezone('Australia/Perth'))
    scheduler.add_job(
        lambda: send_daily_message(bot, channel_id),
        CronTrigger(hour=6, minute=0, second=0)
    )
    scheduler.start()
    print("[INFO] Daily message scheduler started for timezone Australia/Perth.")

