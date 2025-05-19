from flask import Flask, redirect, url_for, session, request, jsonify
import requests
from authlib.integrations.flask_client import OAuth
from flask_cors import CORS
from authlib.common.security import generate_token
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from bson.objectid import ObjectId

# app = Flask(__name__)
load_dotenv()

static_path = os.getenv('STATIC_PATH','static')
template_path = os.getenv('TEMPLATE_PATH','templates')

app = Flask(__name__, static_folder=static_path, template_folder=template_path)
app.secret_key = os.urandom(24)
CORS(app)

# idk
CORS(app, supports_credentials=True, origins='http://localhost:5173')

# define user class
from typing import NamedTuple

class UserTuple(NamedTuple):
    user_id : int
    name : str
    email : str

oauth = OAuth(app)

nonce = generate_token()

# establish user database
mongo_uri = os.getenv("MONGO_URI")
client2 = MongoClient(mongo_uri)
db2 = client2["mydb"]
users_collection = db2["users"]

# establish comments database
client = MongoClient('mongodb://root:rootpassword@mongo:27017/')
db = client['comments']
collection = db['data']

oauth.register(
    name=os.getenv('OIDC_CLIENT_NAME'),
    client_id=os.getenv('OIDC_CLIENT_ID'),
    client_secret=os.getenv('OIDC_CLIENT_SECRET'),
    #server_metadata_url='http://dex:5556/.well-known/openid-configuration',
    authorization_endpoint="http://localhost:5556/auth",
    token_endpoint="http://dex:5556/token",
    jwks_uri="http://dex:5556/keys",
    userinfo_endpoint="http://dex:5556/userinfo",
    device_authorization_endpoint="http://dex:5556/device/code",
    client_kwargs={'scope': 'openid email profile'}
)

@app.route("/test-mongo")
def test_mongo():
    test_doc = {"message": "Hello, MongoDB!"}
    collection.insert_one(test_doc)
    return "Inserted test doc into MongoDB!"

# delete comments
@app.route('/api/delete_comment', methods=['DELETE'])
def delete_comment():
    comment_id = request.args.get('comment_id')
    if not comment_id:
        return jsonify({"error": "No comment_id provided"}), 400

    try:
        result = collection.delete_one({"_id": ObjectId(comment_id)})
        replies_res = collection.delete_many({"comment_id": comment_id})
        print(replies_res)
        if result.deleted_count == 1:
            return jsonify({"message": "deleted comment"}), 200
        else:
            return jsonify({"error": "no comment"}), 404
    except Exception as e:
        print("Error deleting comment:", e)
        return jsonify({"error": str(e)}), 500
    

@app.route('/api/add_data', methods=['POST'])
def add_data():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        print("Received data:", data)
        collection.insert_one(data)
        return jsonify({'message': 'Data added to MongoDB'}), 201
    except Exception as e:
        print("Error inserting data:", e)
        return jsonify({'error': str(e)}), 500

# get stand-alone/parent comments 
@app.route('/get_comments')
def get_comments():
    article_id = request.args.get('article')
    articleComments = collection.find({
        "article": article_id,
        "isReply": False
    })
    comments = list(articleComments)
    for c in comments:
        c['_id'] = str(c['_id'])  # Convert ObjectId to string
    return jsonify(comments)

# get replies of parent comments
@app.route('/get_replies')
def get_replies():
    comment_id = request.args.get('comment_id')
    comment_replies = collection.find({"comment_id": comment_id})
    comments = list(comment_replies)
    for c in comments:
        c['_id'] = str(c['_id'])  # Convert ObjectId to string
    return jsonify(comments)

#---------END OF API CALLS FOR COMMENTS------------

# get NYT api key
@app.route('/api/key')
def get_key():
    return jsonify({'apiKey': os.getenv('NYT_API_KEY')})

# get articles from NYT
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
def home():
    user = session.get('user')
    if user:
        return jsonify({
        'email': user.get('email'),
        'name': user.get('name'),
        'loggedIn': True
    })
    return jsonify({'loggedIn': False})

@app.route('/login')
def login():
    client_name = os.getenv('OIDC_CLIENT_NAME')
    session['nonce'] = nonce
    redirect_uri = 'http://localhost:8000/authorize'
    return getattr(oauth, client_name).authorize_redirect(redirect_uri, nonce=nonce)

@app.route('/authorize')
def authorize():
    client_name = os.getenv('OIDC_CLIENT_NAME')
    print("Authorizing with client:", client_name)

    token = getattr(oauth, client_name).authorize_access_token()
    print("Access token received.")

    nonce = session.get('nonce')
    user_info = getattr(oauth, client_name).parse_id_token(token, nonce=nonce)

    session['user'] = user_info

    email = user_info.get('email')
    print(email)
    name = user_info.get('name')

    curr_user = users_collection.find_one({'email': email})

    if not curr_user:
        new_user = {'email': email, 'name': name}
        users_collection.insert_one(new_user)


    # Redirect to frontend with login status
    return redirect(f'http://localhost:5173/?loggedIn=true&email={email}&username={name}')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
