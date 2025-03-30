# AI CryptoNewsletter Curator

This project aggregates, summarizes, and analyzes cryptocurrency newsletters using AI.

## Project Overview

The AI CryptoNewsletter Curator is designed to provide users with the latest insights and trends in the cryptocurrency market. It scrapes various cryptocurrency newsletters, summarizes the content, and analyzes the sentiment of the articles to help users stay informed.

## Core Functionalities

- **Scraping**: The project scrapes cryptocurrency newsletters for the latest news articles.
- **Summarization**: It summarizes the scraped news articles to provide concise information.
- **Sentiment Analysis**: The project analyzes the sentiment of the news articles using VADER sentiment analysis, categorizing them as positive, negative, or neutral.
- **Telegram Bot Integration**: A Telegram bot allows users to interact with the service. Users can:
  - Use `/latest` to get the latest news.
  - Use `/search <keyword>` to find specific news articles.
  - Use `/price <coin>` to get live cryptocurrency prices.
  - Use `/sentiment` to analyze market sentiment.
  - Use `/generate_report` to receive a visual market summary.
- **Image Generation**: The bot can generate visual reports of market trends and sentiment using OpenAI's image generation capabilities.

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/AI-CryptoNewsletter-Curator.git
   ```
2. Navigate to the project directory:
   ```bash
   cd AI-CryptoNewsletter-Curator
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up your environment variables in a `.env` file:
   ```
   OPENAI_API_KEY=your_openai_api_key
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   ```

5. Run the main application:
   ```bash
   python src/main.py
   ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the contributors and the open-source community for their support.
