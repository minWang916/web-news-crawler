import requests
from bs4 import BeautifulSoup
from database import LINKS_COLLECTION, SOURCES_COLLECTION
from redis_cache import REDIS_CACHE

news_urls = [
  ('https://vnexpress.net/kinh-doanh/chung-khoan', 'https://vnexpress.net', 'title-news', 'description'),
  ('https://kinhtedothi.vn/tai-chinh-chung-khoan.html', 'https://kinhtedothi.vn', 'story__title', 'story__summary'),
]

def extract_link(title_element, site):
  link = title_element.find('a').get('href')
  if link[0] == "/":
    link = site + link
  return link

def fetch_news(url, site, titleTag, summaryTag):
  try:
    response = requests.get(url)
    response.raise_for_status()
    page_content = response.content
    soup = BeautifulSoup(page_content, 'html.parser')

    # Extract the news content based on HTML structure
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
    print(articles)

    for article in articles:
      LINKS_COLLECTION.insert_one(article)
      
    return {'url': url, 'status': 'success'}
  except requests.RequestException as e:
      return {'url': url, 'error': str(e)}
  except Exception as e:
      return {'url': url, 'error': str(e)}
  
for element in news_urls:
  url, site, titleTag, summaryTag = element
  fetch_news(url, site, titleTag, summaryTag)

REDIS_CACHE.set("current_index", 1)
print(int(REDIS_CACHE.get("current_index")))