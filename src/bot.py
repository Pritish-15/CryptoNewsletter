import os
from dotenv import load_dotenv
import json
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Load environment variables from .env file
load_dotenv()

# Load API keys from environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN").strip()  # Ensure no leading/trailing spaces
COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price"

# Load news data
NEWS_FILE = "D:/frosthack/AI-CryptoNewsletter-Curator/data/final_report.json"
def load_news():
    with open(NEWS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hello! I am your AI CryptoNewsletter Bot. Use /latest for news, /search <keyword> to find specific news, /price <coin> for live prices, and /sentiment for market analysis.")

# Command: /latest (Fetch latest news)
async def latest_news(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    news_data = load_news()
    if not any(news_data.values()):  # Check if all lists are empty
        await update.message.reply_text("❌ No news available at the moment.")
        return
    response = "📰 Latest Crypto News:\n"
    for url, items in news_data.items():
        for item in items[:5]:  # Show top 5 news from each source
            response += f"\n🔹 {item['title']}\n{item['url']}\n"





    await update.message.reply_text(response)

# Command: /search <keyword> (Search specific crypto news)
async def search_news(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Please provide a keyword. Example: /search Bitcoin")
        return
    
    keyword = " ".join(context.args).lower()
    news_data = load_news()
    filtered_news = [item for source in news_data.values() for item in source if keyword in item['title'].lower() or keyword in item['summary'].lower()]

    
    if not filtered_news:
        await update.message.reply_text(f"No news found for '{keyword}'.")
        return
    
    response = f"📰 News related to '{keyword}':\n"
    for item in filtered_news[:5]:  # Show top 5 results
        response += f"\n🔹 {item['title']}\n{item['url']}\n"
    await update.message.reply_text(response)

# Command: /price <coin> (Fetch live price from CoinGecko)
async def get_price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Please provide a coin symbol. Example: /price bitcoin")
        return
    
    coin = context.args[0].lower()
    params = {"ids": coin, "vs_currencies": "usd"}
    response = requests.get(COINGECKO_API_URL, params=params)
    
    if response.status_code == 200 and coin in response.json():
        price = response.json()[coin]["usd"]
        await update.message.reply_text(f"💰 {coin.capitalize()} Price: ${price}")
    else:
        await update.message.reply_text("❌ Invalid coin or price not available.")

# Telegram Bot Setup
application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("latest", latest_news))
application.add_handler(CommandHandler("search", search_news))
application.add_handler(CommandHandler("price", get_price))

# Start bot
if __name__ == "__main__":
    application.run_polling()
