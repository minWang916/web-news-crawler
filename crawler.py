import requests
from bs4 import BeautifulSoup
from database import LINKS_COLLECTION, SOURCES_COLLECTION
from urls import news_urls
from redis_cache import REDIS_CACHE
  
def extract_link(title_element, site):
  link = title_element.find('a')
  if link is None:
    link = title_element
  link = link.get("href")
  if link[0] == "/" or link[0] == ".":
    link = site + link
  return link

def fetch_news(source, site, urlTag, titleTag, summaryTag):
  try:
    response = requests.get(source)
    response.raise_for_status()
    page_content = response.content
    soup = BeautifulSoup(page_content, 'html.parser')

    # Extract the news content based on HTML structure
    title_elements = soup.find_all(class_=titleTag)
    url_elements = soup.find_all(class_=urlTag)
    print(title_elements)
    # print(len(title_elements))
    for title_element in title_elements:
      print(title_element)
    links = [extract_link(url_element, site) for url_element in url_elements]
    titles = [title_element.get_text().strip() for title_element in title_elements]
    print(links)
    print(titles)
    description_elements = soup.find_all(class_=summaryTag)
    descriptions = [description.get_text().strip() for description in description_elements]
    
    # If there is no description, fi
    if descriptions == []:
      descriptions = ["" for i in titles]

    articles = [{
      'title': title,
      'source': source,
      'site': site,
      'link': link,
      'summary': description
    } for title, link, description in zip(titles, links, descriptions)]
    print(articles)

    LINKS_COLLECTION.delete_many({"source": source})
    for article in articles:
      LINKS_COLLECTION.insert_one(article)
      
    return {'url': source, 'status': 'success'}
  except requests.RequestException as e:
      return {'url': source, 'error': str(e)}
  except Exception as e:
      return {'url': source, 'error': str(e)}
  
for i in range(0, 42):
  try:
    document = SOURCES_COLLECTION.find_one({"id": i})
    source = document["source"]
    site = document["site"]
    urlTag = document["urlTag"]
    titleTag = document["titleTag"]
    summaryTag = document["summaryTag"]
    print(fetch_news(source, site, urlTag, titleTag, summaryTag))
  except:
    print("Error occurs when crawling from " + SOURCES_COLLECTION.find_one({"id": i})["source"])

