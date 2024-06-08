from flask import Flask, render_template
from utils.database import LINKS_COLLECTION
import math

app = Flask(__name__)


def truncate_url(url, length=30):
    if len(url) > length:
        return url[:length] + "..."
    return url


app.jinja_env.filters['truncate_url'] = truncate_url


@app.route('/')
@app.route('/page/<int:page>') 
def main_page(page=1):
  articles_per_page = 10
  all_articles = list(LINKS_COLLECTION.find())
  articles = sorted(all_articles, key=lambda x: not x.get("summary", "") != "")


  fireant_articles = [article for article in articles if "https://fireant.vn/" in article.get("link", "")][:10]

  
  vnexpress_articles = [article for article in articles if "https://vnexpress.net/" in article.get("link", "")][:10]


  total_articles = len(articles)
  total_pages = math.ceil(total_articles / articles_per_page)
  start_idx = (page - 1) * articles_per_page
  end_idx = start_idx + articles_per_page

  paginated_articles = articles[start_idx:end_idx]

  pagination = {
      'total_pages': total_pages,
      'current_page': page,
      'previous_page': page - 1 if page > 1 else None,
      'next_page': page + 1 if page < total_pages else None,
  }

  return render_template('index.html', 
                          articles=paginated_articles, 
                          pagination=pagination, 
                          max=max, 
                          min=min, 
                          fireant_articles=fireant_articles,
                          vnexpress_articles=vnexpress_articles,)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)