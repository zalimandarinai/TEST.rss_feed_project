import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator

def fetch_bloomberg_russia():
    # Bloomberg search URL for "Russia"
    url = "https://www.bloomberg.com/search?query=russia"

    # Fetch the page content
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code != 200:
        raise Exception(f"Failed to fetch Bloomberg page. Status code: {response.status_code}")

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all article entries (make sure this matches the page structure)
    articles = soup.find_all('article', class_='story-package-module__story')

    # Prepare RSS feed generator
    fg = FeedGenerator()
    fg.title("Bloomberg Russia News")
    fg.link(href=url, rel="alternate")
    fg.description("RSS feed for Bloomberg articles about Russia")
    fg.docs("http://www.rssboard.org/rss-specification")
    fg.generator("python-feedgen")
    
    # Set the lastBuildDate to the current time
    from datetime import datetime
    fg.lastBuildDate(datetime.utcnow())

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

# Main function to generate and save the RSS feed
if __name__ == "__main__":
    try:
        rss_feed = fetch_bloomberg_russia()
        with open("bloomberg_russia.xml", "w", encoding="utf-8") as f:
            f.write(rss_feed)
        print("RSS feed generated successfully: bloomberg_russia.xml")
    except Exception as e:
        print(f"Error: {e}")
