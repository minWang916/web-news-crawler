from utils.database import LINKS_COLLECTION, SOURCES_COLLECTION
from utils.redis_cache import REDIS_CACHE
from utils.crawler import fetch_news

while True:
  i = (REDIS_CACHE.incr("current_index") - 1) % SOURCES_COLLECTION.count_documents({})
  print("Processing source number " , i)
  try:
    document = SOURCES_COLLECTION.find_one({"id": i})
    source = document["source"]
    site = document["site"]
    urlTag = document["urlTag"]
    titleTag = document["titleTag"]
    summaryTag = document["summaryTag"]
    print(fetch_news(source, site, urlTag, titleTag, summaryTag))
    print("Crawl successfully at " + SOURCES_COLLECTION.find_one({"id": i})["source"])
  except:
    print("Error occurs when crawling from ")