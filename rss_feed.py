import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from flask import Flask, Response

app = Flask(__name__)

def fetch_bloomberg_russia():
    # Bloomberg search URL for "Russia"
    url = "https://www.bloomberg.com/search?query=russia"

    # Fetch the page content
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code != 200:
        raise Exception(f"Failed to fetch Bloomberg page. Status code: {response.status_code}")

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all article entries
    articles = soup.find_all('article', class_='story-package-module__story')

    # Prepare RSS feed generator
    fg = FeedGenerator()
    fg.title("Bloomberg Russia News")
    fg.link(href=url, rel="alternate")
    fg.description("RSS feed for Bloomberg articles about Russia")
    
    # Extract and add articles to the feed
    for article in articles:
        title = article.find('a').get_text(strip=True)
        link = article.find('a')['href']
        description = article.find('p').get_text(strip=True) if article.find('p') else "No description available"

        # Add each article to the RSS feed
        fe = fg.add_entry()
        fe.title(title)
        fe.link(href=f"https://www.bloomberg.com{link}")
        fe.description(description)

    # Generate the RSS feed
    return fg.rss_str(pretty=True).decode('utf-8')

@app.route("/")
def get_feed():
    try:
        rss_feed = fetch_bloomberg_russia()
        return Response(rss_feed, mimetype="application/rss+xml")
    except Exception as e:
        return f"Error: {e}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
