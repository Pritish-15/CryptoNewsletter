import json
import os
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont

def generate_image(prompt, save_path):
    """Generates a simple image with text and saves it locally."""
    try:
        # Create a blank image with white background
        img = Image.new('RGB', (1024, 1024), color='white')
        d = ImageDraw.Draw(img)

        # Load a font
        font = ImageFont.load_default()

        # Draw the prompt text on the image
        d.text((10, 10), prompt, fill=(0, 0, 0), font=font)

        # Save the image
        img.save(save_path)
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
                "url": article["url"],  # Changed 'link' to 'url'
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
