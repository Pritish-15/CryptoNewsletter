import requests

# Define sources to fetch HTML
SOURCES = [
    {
        "name": "CoinDesk",
        "url": "https://www.coindesk.com/"
    },
    {
        "name": "CoinTelegraph",
        "url": "https://cointelegraph.com/"
    }
]

def fetch_html():
    for source in SOURCES:
        try:
            print(f"Fetching HTML for {source['name']}...")
            response = requests.get(source["url"])
            if response.status_code == 200:
                print(f"HTML for {source['name']} fetched successfully.")
                print(response.text)  # Print the entire HTML content

            else:
                print(f"Failed to fetch {source['name']} (Status Code: {response.status_code})")
        except Exception as e:
            print(f"Error fetching {source['name']}: {e}")

if __name__ == "__main__":
    fetch_html()
