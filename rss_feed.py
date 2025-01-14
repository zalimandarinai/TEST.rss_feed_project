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
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extracting articles (adjust selectors based on actual HTML)
    articles = []
    for item in soup.find_all('article'):  # Modify based on structure
        title = item.find('h1') or item.find('h2')  # Adjust selectors
        link = item.find('a')['href'] if item.find('a') else None
        if title and link:
            articles.append({'title': title.text.strip(), 'link': link})

    return jsonify({'articles': articles})

if __name__ == '__main__':
    app.run(debug=True)
