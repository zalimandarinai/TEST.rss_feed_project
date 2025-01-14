from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/rss', methods=['GET'])
def get_rss():
    url = 'https://www.bloomberg.com/search?query=russia'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Process RSS feed here (customized per site structure)
    articles = []
    for item in soup.find_all('article'):  # Adjust selector
        title = item.find('h1') or item.find('h2')  # Adjust
        link = item.find('a')['href'] if item.find('a') else None
        if title and link:
            articles.append({'title': title.text.strip(), 'link': link})
    
    return jsonify({'articles': articles})

if __name__ == '__main__':
    app.run(debug=True)
