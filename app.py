from flask import Flask, render_template
from utils.database import LINKS_COLLECTION

app = Flask(__name__)

# Route for the main page
@app.route('/')
def main_page():
  articles = []
  all_articles = LINKS_COLLECTION.find()
  for article in all_articles:
    articles.append({
      "title": article["title"],
      "link": article["link"],
      "summary": article["summary"]
    })
  return render_template('index.html', articles = articles)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)