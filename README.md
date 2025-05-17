# 🎲 Maberse Bot

**The ultimate bot in terms of attack and defense.**

Maberse is a lightweight, Python-based Discord bot built for fun and utility — including music playback, dice rolling, weather updates, jokes, and more.

---

## 🚀 Quick Setup

```bash
# Create virtual environment and install core dependencies
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Ensure latest versions of core modules
pip install -U yt-dlp
pip install -U "discord.py[voice]"

# Add your Discord bot token to a .env file:
BOT_TOKEN=your_bot_token_here

# Then run:
python3 main.py