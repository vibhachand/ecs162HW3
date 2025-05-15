from flask import Flask, jsonify, send_from_directory, request
import os
import requests
from flask_cors import CORS
from pymongo import MongoClient

static_path = os.getenv('STATIC_PATH','static')
template_path = os.getenv('TEMPLATE_PATH','templates')
# Mongo connection
mongo_uri = os.getenv("MONGO_URI")
mongo = MongoClient(mongo_uri)
db = mongo.get_default_database()


app = Flask(__name__, static_folder=static_path, template_folder=template_path)
CORS(app)

@app.route('/api/key')
def get_key():
    return jsonify({'apiKey': os.getenv('NYT_API_KEY')})

@app.route('/articles', methods=['GET'])
def get_articles():
    NYT_API_KEY = os.getenv('NYT_API_KEY')
    
    # find articles relevant to UC Davis
    query = '"UC Davis"' 
    url = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q={query}&api-key={NYT_API_KEY}"


    try:
        # GET request to NYI API
        response = requests.get(url)
        response.raise_for_status() #check for HTTP errors 
        data = response.json()

        # create empty array to store articles + their info
        articles = []
        # loop through each article in search results from API request
        for article in data['response']['docs']:
            multimedia = article['multimedia']
            default = multimedia['default']
            image_url = default['url']

            # get the necessary information for each article
            article_info = {
                'headline': article['headline']['main'],
                'url': article['web_url'],
                'author': article['byline']['original'],
                'abstract':  article['snippet'],
                'image': image_url,
                'caption': multimedia['caption']
            }
            # add article to articles list
            articles.append(article_info)
    
        return jsonify({'articles': articles})

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/')
@app.route('/<path:path>')
def serve_frontend(path=''):
    if path != '' and os.path.exists(os.path.join(static_path,path)):
        return send_from_directory(static_path, path)
    return send_from_directory(template_path, 'index.html')

@app.route("/test-mongo")
def test_mongo():
    return jsonify({"collections": db.list_collection_names()})

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)),debug=debug_mode)