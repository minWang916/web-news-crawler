import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from celery_config import Celery
import os
import logging
from dotenv import load_dotenv

load_dotenv()

# MongoDB setup
MONGO_USERNAME = os.environ.get("MONGO_USERNAME")
MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD")
MONGO_URI = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@links.qyv15f1.mongodb.net/?retryWrites=true&w=majority&appName=Links"

client = MongoClient(MONGO_URI)
db = client.get_database('news_db')
LINKS_COLLECTION = db['links']

# Celery app
app = Celery('tasks', broker='redis://localhost:6379/0')

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

news_urls = [
    ('https://vnexpress.net/kinh-doanh/chung-khoan', 'https://vnexpress.net', 'title-news', 'description'),
    ('https://kinhtedothi.vn/tai-chinh-chung-khoan.html', 'https://kinhtedothi.vn', 'story__title', 'story__summary'),
]

def extract_link(title_element, site):
    link = title_element.find('a').get('href')
    if link and link[0] == "/":
        link = site + link
    return link

@app.task
def fetch_news(url, site, titleTag, summaryTag):
    logger.info(f'Starting task for URL: {url}')
    try:
        response = requests.get(url)
        response.raise_for_status()
        page_content = response.content
        soup = BeautifulSoup(page_content, 'html.parser')

        title_elements = soup.find_all(class_=titleTag)
        links = [extract_link(title_element, site) for title_element in title_elements]
        titles = [title_element.get_text().strip() for title_element in title_elements]
        description_elements = soup.find_all(class_=summaryTag)
        descriptions = [description.get_text().strip() for description in description_elements]

        articles = [{
            'title': title,
            'site': site,
            'link': link,
            'summary': description
        } for title, link, description in zip(titles, links, descriptions)]
        logger.info(f'Fetched {len(articles)} articles from {url}')

        for article in articles:
            LINKS_COLLECTION.insert_one(article)

        logger.info(f'Task completed for URL: {url}')
        return {'url': url, 'status': 'success'}
    except requests.RequestException as e:
        logger.error(f'Error fetching {url}: {str(e)}')
        return {'url': url, 'error': str(e)}
    except Exception as e:
        logger.error(f'Error processing {url}: {str(e)}')
        return {'url': url, 'error': str(e)}
