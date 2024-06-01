from redis_cache import REDIS_CACHE
from database import SOURCES_COLLECTION
from crawler import fetch_news

# increase value of current_index(redis cache) by 1
# REDIS_CACHE.incr("current_index", 1)
# print(int(REDIS_CACHE.get("current_index")))

# crawler
for i in range(0, 42):
    try:
        document = SOURCES_COLLECTION.find_one({"id": i})
        source = document["source"]
        site = document["site"]
        urlTag = document["urlTag"]
        titleTag = document["titleTag"]
        summaryTag = document["summaryTag"]
        fetch_news(source, site, urlTag, titleTag, summaryTag)

        # increase the redis cache by 1 after crawling from a source
        REDIS_CACHE.incr("current_index", 1)
    except:
        print("Error occurs when crawling from " + SOURCES_COLLECTION.find_one({"id": i})["source"])

# print the redis cache value after crawling
print(int(REDIS_CACHE.get("current_index")))

# print the source with id 10
source_with_id = SOURCES_COLLECTION.find_one({"id": 10})
print(source_with_id)