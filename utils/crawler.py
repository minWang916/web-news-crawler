import requests
from bs4 import BeautifulSoup
from utils.database import LINKS_COLLECTION
  
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
    links = [extract_link(url_element, site) for url_element in url_elements]
    titles = [title_element.get_text().strip() for title_element in title_elements]
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
    # print(articles)

    LINKS_COLLECTION.delete_many({"source": source})
    for article in articles:
      LINKS_COLLECTION.insert_one(article)
      
    return {'url': source, 'status': 'success'}
  except requests.RequestException as e:
      return {'url': source, 'error': str(e)}
  except Exception as e:
      return {'url': source, 'error': str(e)}

