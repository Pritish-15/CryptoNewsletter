import os
import requests

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Load API keys from environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN").strip()

# Test the bot token
url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getMe"
response = requests.get(url)

if response.status_code == 200:
    print("Token is valid. Bot is operational.")
else:
    print("Invalid token or bot is not operational.")
