from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the RSS Feed API. Use /rss to fetch the RSS feed."

@app.route('/rss', methods=['GET'])
def get_rss():
    # Bloomberg search URL
    url = 'https://www.bloomberg.com/search?query=russia'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        # Fetch the page
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return jsonify({'error': 'Failed to fetch data from Bloomberg', 'status_code': response.status_code}), 500
        
        # Parse the page with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Initialize an empty list to store articles
        articles = []

        # Find all article containers
        for item in soup.find_all('div', class_='summary__content'):
            title_tag = item.find('a')  # Find the <a> tag within the article container
            if title_tag:
                title = title_tag.text.strip()
                link = title_tag['href']
                # Ensure the link is complete
                full_link = link if link.startswith('http') else f"https://www.bloomberg.com{link}"
                articles.append({'title': title, 'link': full_link})
        
        # Return the articles in JSON format
        return jsonify({'articles': articles})
    
    except Exception as e:
        # Handle any scraping or connection errors
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
