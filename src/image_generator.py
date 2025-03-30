import json
import openai
import os
from dotenv import load_dotenv

def generate_image(prompt, save_path):
    """Generates an image using DALL·E and saves it locally."""
    try:
        response = openai.Image.create(
            model="dall-e-2",
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        
        image_url = response["data"][0]["url"]
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(response.content)  # Save image

        print(f"✅ Image saved: {save_path}")
        return save_path
    except Exception as e:
        print(f"❌ Error in image generation: {e}")
        return None

def process_sentiment_data(input_file="D:/frosthack/AI-CryptoNewsletter-Curator/data/sentiment_data.json", output_file="D:/frosthack/AI-CryptoNewsletter-Curator/data/final_report.json"):
    """Loads sentiment data, generates images, and saves final report."""
    with open(input_file, "r", encoding="utf-8") as f:
        sentiment_data = json.load(f)
    
    final_report = {}
    for source, articles in sentiment_data.items():
        final_report[source] = []
        for article in articles:
            prompt = f"Crypto news visualization: {article['title']}, Sentiment: {article['gpt_sentiment']}"
            image_path = f"images/{article['title'].replace(' ', '_')}.png"
            os.makedirs("images", exist_ok=True)
            os.makedirs("data", exist_ok=True)
            generated_image = generate_image(prompt, image_path)
            
            final_report[source].append({
                "title": article["title"],
                "link": article["link"],
                "summary": article["summary"],
                "sentiment": article["gpt_sentiment"],
                "image": generated_image
            })
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(final_report, f, indent=4)
    print(f"✅ Final report saved to {output_file}")

if __name__ == "__main__":
    process_sentiment_data()
    print("🚀 Image generation complete!")
