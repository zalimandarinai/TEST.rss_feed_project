from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the RSS Feed API. Use /rss to fetch the RSS feed."

@app.route('/rss', methods=['GET'])
def get_rss():
    # Setup Selenium WebDriver
    options = Options()
    options.add_argument('--headless')  # Run Chrome in headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Open Bloomberg search page
        url = 'https://www.bloomberg.com/search?query=russia'
        driver.get(url)

        # Allow time for JavaScript to load
        time.sleep(5)

        # Find articles using Selenium
        articles = []
        article_elements = driver.find_elements(By.CLASS_NAME, 'summary__content')
        for element in article_elements:
            try:
                title_element = element.find_element(By.TAG_NAME, 'a')
                title = title_element.text.strip()
                link = title_element.get_attribute('href')
                articles.append({'title': title, 'link': link})
            except:
                continue

        return jsonify({'articles': articles})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        # Close the WebDriver
        driver.quit()

if __name__ == '__main__':
    app.run(debug=True)
