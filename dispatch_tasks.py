from tasks import fetch_news, news_urls
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

for element in news_urls:
    url, site, titleTag, summaryTag = element
    task = fetch_news.delay(url, site, titleTag, summaryTag)
    logger.info(f'Dispatched task {task.id} for URL: {url}')
