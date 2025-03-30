import json
import openai
import os
from dotenv import load_dotenv
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# Load API keys from .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Ensure NLTK resources are available
nltk.download("vader_lexicon")
sia = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    """Analyzes sentiment using GPT-4 and VADER."""
    try:
        # VADER sentiment analysis
        vader_score = sia.polarity_scores(text)
        vader_sentiment = (
            "Positive" if vader_score["compound"] > 0.05 else
            "Negative" if vader_score["compound"] < -0.05 else "Neutral"
        )
        
        # GPT-4 sentiment analysis
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Analyze the sentiment of the following crypto article summary (Positive, Neutral, or Negative)."},
                {"role": "user", "content": text}
            ]
        )
        gpt_sentiment = response['choices'][0]['message']['content'].strip()
        
        return vader_sentiment, gpt_sentiment
    except Exception as e:
        print(f"❌ Error in sentiment analysis: {e}")
        return "Unknown", "Unknown"

def process_summarized_data(input_file="D:/frosthack/AI-CryptoNewsletter-Curator/data/summarized_data.json", 
                            output_file="D:/frosthack/AI-CryptoNewsletter-Curator/data/sentiment_data.json"):
    """Loads summarized data, performs sentiment analysis, and saves results."""
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            summarized_data = json.load(f)
    
        sentiment_results = {}
        for source, articles in summarized_data.items():
            sentiment_results[source] = []
            for article in articles:
                print(f"📊 Analyzing sentiment for: {article['title']}")
                vader_sentiment, gpt_sentiment = analyze_sentiment(article['summary'])
                sentiment_results[source].append({
                    "title": article["title"],
                    "url": article["url"],  # Fixed 'link' to 'url'
                    "summary": article["summary"],
                    "vader_sentiment": vader_sentiment,
                    "gpt_sentiment": gpt_sentiment
                })
        
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(sentiment_results, f, indent=4)

    except Exception as e:
        print(f"❌ Error in processing summarized data: {e}")
        return
    
    print(f"✅ Sentiment data saved to {output_file}")

if __name__ == "__main__":
    process_summarized_data()
    print("🚀 Sentiment analysis complete!")
