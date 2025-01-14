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

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises HTTPError for bad responses

        soup = BeautifulSoup(response.content, 'html.parser')
        articles = []

        # Find all article containers
        for item in soup.find_all('article'):
            # Extract title
            title_tag = item.find('h1') or item.find('h2') or item.find('h3')
            if title_tag and title_tag.a:
                title = title_tag.get_text(strip=True)
                link = title_tag.a['href']
                # Ensure the link is absolute
                if not link.startswith('http'):
                    link = 'https://www.bloomberg.com' + link
                articles.append({'title': title, 'link': link})

        return jsonify({'articles': articles})

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'HTTP request failed: {e}'}), 500
    except Exception as e:
        return jsonify({'error': f'An error occurred: {e}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
