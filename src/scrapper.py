import requests
from bs4 import BeautifulSoup
import json
import time
import random

# Load configuration from JSON file
with open("src/config.json", "r") as config_file:
    config = json.load(config_file)

SOURCES = config["SOURCES"]
USER_AGENTS = config["USER_AGENTS"]

# Function to scrape news
def scrape_news_with_retries(max_retries=3):
    news_data_dict = {}

    for source in SOURCES:
        try:
            print(f"Scraping {source['name']}...")
            headers = {"User-Agent": random.choice(USER_AGENTS)}  # Use user agents from config

            for attempt in range(max_retries):
                response = requests.get(source["url"], headers=headers)
                if response.status_code == 200:
                    break
                print(f"Attempt {attempt + 1} failed. Retrying...")
                time.sleep(2 ** attempt)  # Exponential backoff

            if response.status_code != 200:
                print(f"Failed to fetch {source['name']} (Status Code: {response.status_code})")
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            articles = soup.find_all(source["article_tag"])  # Removed class filtering for flexibility

            print(f"Found {len(articles)} articles for {source['name']}.")

            if not articles:
                print(f"No articles found for {source['name']}. Check the structure.")
                continue

            news_data_dict[source["name"]] = []  # Initialize list for this source
            for article in articles[:10]:  # Limit to 10 articles per source
                title_tag = article.find("h2") or article.find("h3") or article.find("a")
                summary_tag = article.find("p")  # Keeping it simple for now
                link_tag = article.find("a", href=True)

                if title_tag and link_tag:
                    title = title_tag.text.strip()
                    summary = summary_tag.text.strip() if summary_tag else "No summary available"
                    url = link_tag["href"]
                    if not url.startswith("http"):
                        url = source["url"] + url

                    if title and summary and url:  # Ensure all variables are set
                        news_data_dict[source["name"]].append({
                            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),  # Add timestamp
                            "source": source["name"],
                            "title": title,
                            "summary": summary,  # Keeping it as summary for now
                            "url": url
                        })
        except Exception as e:
            print(f"Error scraping {source['name']}: {e}")
        time.sleep(2)  # Avoid hitting the server too fast

    return news_data_dict  # Return the dictionary instead of the list


# Save to JSON
def save_news(news):
    if not news:
        print("No news articles were scraped. Check sources.")
        return
    
    with open("D:/frosthack/AI-CryptoNewsletter-Curator/data/scraped_data.json", "w", encoding="utf-8") as f:
        # Save the scraped news data to a JSON file
        json.dump(news, f, indent=4, ensure_ascii=False)

    print("✅ News data saved successfully!")

if __name__ == "__main__":
    scraped_news = scrape_news_with_retries()
    save_news(scraped_news)
    print("✅ News scraping completed!")
