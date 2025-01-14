import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from flask import Flask, Response

app = Flask(__name__)

# URL for Bloomberg Russia News
url = "https://www.bloomberg.com/search?query=russia"

@app.route('/rss')
def rss_feed():
    try:
        # Fetch the page content
        response = requests.get(url)

        # Parse the HTML page
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract the news articles (adjust based on page structure)
        articles = soup.find_all('article', class_='story-package-module__story')

        # Create the RSS feed
        fg = FeedGenerator()
        fg.title("Bloomberg Russia News")
        fg.link(href=url, rel="alternate")
        fg.description("RSS feed for Bloomberg articles about Russia")
        fg.docs("http://www.rssboard.org/rss-specification")
        fg.generator("python-feedgen")

        # Add articles to the RSS feed
        for article in articles:
            title = article.find('a').get_text(strip=True)
            link = article.find('a')['href']
            description = article.find('p').get_text(strip=True) if article.find('p') else "No description available"

            # Add each article to the feed
            fe = fg.add_entry()
            fe.title(title)
            fe.link(href=f"https://www.bloomberg.com{link}")
            fe.description(description)

        # Generate the RSS feed content
        rss_feed = fg.rss_str(pretty=True)

        # Serve the RSS feed
        return Response(rss_feed, mimetype='application/rss+xml')

    except Exception as e:
        return Response(f"Error generating RSS feed: {e}", status=500)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
