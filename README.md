# 🎲 Maberse Bot

**The ultimate bot in terms of attack and defense.**

Maberse is a lightweight, Python-based Discord bot built for fun and utility — including music playback, dice rolling, weather updates, jokes, and more.

---

## ✨ Features

- **🎲 Dice Rolling:** Advanced dice notation for all your TTRPG needs.
- **🤣 Jokes:** Random jokes from the web.
- **🌦️ Weather:** Get the current weather for a specified location.
- **🎵 Music:** Play music from YouTube in your voice channel.
- **☀️ Daily Message:** A daily message with a joke and the weather at 6 am.

---

## 🚀 Quick Setup

```bash
# Create virtual environment and install core dependencies
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Ensure latest versions of core modules
pip install -U yt-dlp
pip install -U "discord.py[voice]"

# Create a a.env file and add your Discord bot token and bot channel ID
BOT_TOKEN=your_bot_token_here
BOT_CHANNEL_ID=your_bot_channel_id_here

# Then run:
python3 main.py