from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the RSS Feed API. Use /rss to fetch the RSS feed."

@app.route('/rss', methods=['GET'])
def get_rss():
    url = 'https://www.bloomberg.com/search?query=russia'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)

    # Check for successful response
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch data from Bloomberg', 'status_code': response.status_code}), 500

    soup = BeautifulSoup(response.content, 'html.parser')

    # Update selectors based on actual HTML structure
    articles = []
    for item in soup.find_all('div', class_='search-result-story'):  # Adjust class as per Bloomberg's structure
        title_tag = item.find('a', class_='headline-link')  # Adjust class for article title links
        if title_tag:
            title = title_tag.text.strip()
            link = title_tag['href']
            # Ensure link is complete (prepend domain if needed)
            full_link = link if link.startswith('http') else f"https://www.bloomberg.com{link}"
            articles.append({'title': title, 'link': full_link})

    # Return the scraped articles
    return jsonify({'articles': articles})

if __name__ == '__main__':
    app.run(debug=True)
