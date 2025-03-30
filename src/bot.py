import os
import json
import requests
import nltk
import io
import speech_recognition as sr
from PIL import Image
from nltk.sentiment import SentimentIntensityAnalyzer
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import openai
from dotenv import load_dotenv
from stability_sdk import client  # Stability AI for image generation

# Load environment variables
load_dotenv()

# Load API keys
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")
COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price"

openai.api_key = OPENAI_API_KEY  # Set OpenAI API Key

# Load news data
NEWS_FILE = "D:/frosthack/AI-CryptoNewsletter-Curator/data/final_report.json"
def load_news():
    try:
        with open(NEWS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Initialize Sentiment Analyzer
nltk.download('vader_lexicon', quiet=True)
sia = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    sentiment = sia.polarity_scores(text)
    if sentiment['compound'] >= 0.3:
        return "🟢 Bullish (Positive Sentiment)"
    elif sentiment['compound'] <= -0.3:
        return "🔴 Bearish (Negative Sentiment)"
    else:
        return "🟡 Neutral"

# Command: /start
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "Hello! I am your AI CryptoNewsletter Bot. Use /latest for news, /search <keyword> to find news, /price <coin> for live prices, /sentiment for market analysis, /generate_report for a visual summary, and send a voice message to query using voice.")

# Command: /latest
async def latest_news(update: Update, context: CallbackContext) -> None:
    news_data = load_news()
    if not news_data:
        await update.message.reply_text("❌ No news articles available.")
        return
    response = "📰 Latest Crypto News:\n"
    for source, articles in news_data.items():
        for item in articles[:5]:
            response += f"\n🔹 {item['title']}\n{item['url']}\n"
    await update.message.reply_text(response)

# Command: /search <keyword>
async def search_news(update: Update, context: CallbackContext) -> None:
    if not context.args:
        await update.message.reply_text("Please provide a keyword. Example: /search Bitcoin")
        return
    
    keyword = " ".join(context.args).lower()
    news_data = load_news()
    filtered_news = [item for articles in news_data.values() for item in articles if keyword in item['title'].lower() or keyword in item['summary'].lower()]
    
    if not filtered_news:
        await update.message.reply_text(f"No news found for '{keyword}'.")
        return
    
    response = f"📰 News related to '{keyword}':\n"
    for item in filtered_news[:5]:
        response += f"\n🔹 {item['title']}\n{item['url']}\n"
    await update.message.reply_text(response)

# Command: /price <coin>
async def get_price(update: Update, context: CallbackContext) -> None:
    if not context.args:
        await update.message.reply_text("Please provide a coin symbol. Example: /price bitcoin")
        return
    
    coin = context.args[0].lower()
    response = requests.get(COINGECKO_API_URL, params={"ids": coin, "vs_currencies": "usd"})
    
    if response.status_code == 200 and coin in response.json():
        price = response.json()[coin]["usd"]
        await update.message.reply_text(f"💰 {coin.capitalize()} Price: ${price}")
    else:
        await update.message.reply_text("❌ Invalid coin or price not available.")

# Stability AI Image Generation
def generate_crypto_image(prompt):
    stability_api = client.StabilityInference(key=STABILITY_API_KEY, verbose=True)
    response = stability_api.generate(prompt=prompt, width=1024, height=1024, steps=50)
    
    for resp in response:
        for artifact in resp.artifacts:
            if artifact.type == 1:
                img = Image.open(io.BytesIO(artifact.binary))
                img_path = "generated_crypto_image.png"
                img.save(img_path)
                return img_path
    return None

# Command: /sentiment
async def get_sentiment(update: Update, context: CallbackContext) -> None:
    news_data = load_news()
    if not news_data:
        await update.message.reply_text("❌ No news articles available.")
        return

    sentiment_results = [analyze_sentiment(item['summary']) for articles in news_data.values() for item in articles[:5]]
    response = f"📊 **Crypto Market Sentiment Analysis:**\n\n🟢 Bullish News: {sentiment_results.count('🟢 Bullish (Positive Sentiment)')}\n🔴 Bearish News: {sentiment_results.count('🔴 Bearish (Negative Sentiment)')}\n🟡 Neutral News: {sentiment_results.count('🟡 Neutral')}"
    await update.message.reply_text(response)

# Command: /generate_report
async def generate_report(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    image_path = generate_crypto_image("A futuristic crypto market analysis with Bitcoin trends, AI charts")
    
    if image_path:
        await context.bot.send_photo(chat_id=chat_id, photo=open(image_path, 'rb'))
        await update.message.reply_text("Here's your AI-generated crypto analysis image! 📊🚀")
    else:
        await update.message.reply_text("Failed to generate an image. Try again later.")

# Voice Query Handling
async def voice_query(update: Update, context: CallbackContext) -> None:
    file = await update.message.voice.get_file()
    file_path = "voice_message.ogg"
    await file.download_to_drive(file_path)
    
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
    
    await update.message.reply_text(f"🎙️ You said: {text}")
    
    if "price" in text.lower():
        context.args = [text.split()[-1]]
        await get_price(update, context)
    elif "news" in text.lower():
        await latest_news(update, context)
    elif "sentiment" in text.lower():
        await get_sentiment(update, context)
    else:
        await update.message.reply_text("I couldn't understand your request. Please try again.")

# Telegram Bot Setup
application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("latest", latest_news))
application.add_handler(CommandHandler("search", search_news))
application.add_handler(CommandHandler("price", get_price))
application.add_handler(CommandHandler("sentiment", get_sentiment))
application.add_handler(CommandHandler("generate_report", generate_report))
application.add_handler(MessageHandler(filters.VOICE, voice_query))

if __name__ == "__main__":
    application.run_polling()
