import json

def summarize_news(scraped_data):
    summarized_data = {}
    
    for source, articles in scraped_data.items():
        summarized_data[source] = []
        for article in articles:
            summarized_data[source].append({
                "title": article.get("title", "No Title"),
                "summary": article.get("summary", "No summary available"),
                "url": article.get("url", "No URL")
            })
    
    return summarized_data

if __name__ == "__main__":
    with open("D:/frosthack/AI-CryptoNewsletter-Curator/data/scraped_data.json", "r", encoding="utf-8") as file:
        scraped_data = json.load(file)
    
    summarized_data = summarize_news(scraped_data)
    
    with open("D:/frosthack/AI-CryptoNewsletter-Curator/data/summarized_data.json", "w", encoding="utf-8") as json_file:
        json.dump(summarized_data, json_file, indent=4)
    
    print("Summarized data stored successfully in summarize_data.json.")
