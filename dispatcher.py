from utils.database import SOURCES_COLLECTION, SOURCES_BACKUP
from utils.redis_cache import REDIS_CACHE
from utils.crawler import fetch_news

while True:
  # Get index from Redis
  i = (REDIS_CACHE.incr("current_index") - 1) % SOURCES_COLLECTION.count_documents({})

  # Backup for index in Redis
  REDIS_CACHE.incr("current_index_backup")
  if (i == None):
    i = (REDIS_CACHE.get("current_index_backup") - 1) % SOURCES_COLLECTION.count_documents({})

  # Crawl source
  print("Processing source number " , i)
  try:
    # Get source to crawl
    document = SOURCES_COLLECTION.find_one({"id": i})
    # Backup for source
    if (document == None):
      document = SOURCES_BACKUP.find_one({"id": i})

    source = document["source"]
    site = document["site"]
    urlTag = document["urlTag"]
    titleTag = document["titleTag"]
    summaryTag = document["summaryTag"]

    print(fetch_news(source, site, urlTag, titleTag, summaryTag))
    print("Crawl successfully at " + SOURCES_COLLECTION.find_one({"id": i})["source"])
  except:
    print("Error occurs when crawling from ")