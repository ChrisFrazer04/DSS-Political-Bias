from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_cors import cross_origin
import numpy
import spacy
import re
from article_processing import filter_text, scrape_url


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

nlp = spacy.load("en_core_web_sm")

@app.route('/api/article', methods=['POST', 'OPTIONS'])
@cross_origin()
def scrape_article():
    print(request.json)
    url = request.json
    pattern = r"\s"
    url = re.sub(pattern, "", url)
    raw_text = scrape_url(url)
    clean_text = filter_text(raw_text, nlp)
    if len(clean_text.split()) < 20:
        clean_text = "Cannot Scrape Article"
    return jsonify({"text": clean_text})

if __name__ == '__main__':
    app.run(debug=True)