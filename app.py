from flask import Flask, render_template
from utils.database import LINKS_COLLECTION

app = Flask(__name__)

# Route for the main page
@app.route('/')
def main_page():
  rows = []
  articles = LINKS_COLLECTION.find()
  for article in articles:
    rows.append({
      "title": article["title"],
      "link": article["link"],
      "summary": article["summary"]
    })
  return render_template('index.html', rows = rows)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)