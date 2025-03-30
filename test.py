import requests

SCRAPER_API_KEY = "YOUR_API_KEY"
test_url = "https://httpbin.org/ip"

proxy_url = f"http://api.scraperapi.com/?api_key={SCRAPER_API_KEY}&url={test_url}"
response = requests.get(proxy_url)

print(response.text)
