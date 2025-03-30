import json
import openai
import os
from dotenv import load_dotenv
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# Load API keys from .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
print(f"Loaded OpenAI API Key: {OPENAI_API_KEY}")  # Debugging line to check API key
openai.api_key = OPENAI_API_KEY


# Ensure NLTK resources are available
nltk.download("vader_lexicon")
sia = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    """Analyzes sentiment using GPT-3.5-turbo and VADER."""
    try:
        # VADER sentiment analysis
        vader_score = sia.polarity_scores(text)
        vader_sentiment = (
            "Positive" if vader_score["compound"] > 0.05 else
            "Negative" if vader_score["compound"] < -0.05 else "Neutral"
        )
        
        # Removed GPT-3.5-turbo sentiment analysis
        gpt_sentiment = "Not applicable"  # Placeholder since we are not using OpenAI

        
        return vader_sentiment, "Not applicable"  # Return only VADER sentiment

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
