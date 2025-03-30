from telegram import Bot, Update
from telegram.ext import CommandHandler, CallbackContext
from telegram.ext import Application
import os

TELEGRAM_BOT_TOKEN = '7701656280:AAGUMGnzJhDpVxKf19Emsr1q7S-dhAz140U'  # Load token from environment variables

# Test for /start command
def test_start_command():
    update = Update(update_id=123, message=None)  # Mock update
    context = CallbackContext.from_update(update)
    start(update, context)  # Call the start command
    assert update.message.text == "Hello! I am your AI CryptoNewsletter Bot. Use /latest for news, /search <keyword> to find specific news, /price <coin> for live prices, /sentiment for market analysis, /generate_report for a visual market summary, and send a voice message to query using voice."

# Test for /latest command
def test_latest_command():
    update = Update(update_id=124, message=None)  # Mock update
    context = CallbackContext.from_update(update)
    latest_news(update, context)  # Call the latest news command
    assert update.message.text.startswith("📰 Latest Crypto News:")

# Test for /search command
def test_search_command():
    update = Update(update_id=125, message=None)  # Mock update
    context = CallbackContext.from_update(update)
    context.args = ["Bitcoin"]  # Mock search keyword
    search_news(update, context)  # Call the search command
    assert "No news found for 'Bitcoin'" not in update.message.text  # Ensure news is found

# Initialize the application
application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
