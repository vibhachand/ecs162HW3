from flask import Flask, redirect, url_for, session, request, jsonify
import requests
from authlib.integrations.flask_client import OAuth
from flask_cors import CORS
from authlib.common.security import generate_token
import os

# app = Flask(__name__)

static_path = os.getenv('STATIC_PATH','static')
template_path = os.getenv('TEMPLATE_PATH','templates')

app = Flask(__name__, static_folder=static_path, template_folder=template_path)
app.secret_key = os.urandom(24)
CORS(app)

oauth = OAuth(app)

nonce = generate_token()


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
def home():
    user = session.get('user')
    if user:
        return f"<h2>Logged in as {user['email']}</h2><a href='/logout'>Logout</a>"
    return '<a href="/login">Login with Dex</a>'

@app.route('/login')
def login():
    session['nonce'] = nonce
    redirect_uri = 'http://localhost:8000/authorize'
    return oauth.flask_app.authorize_redirect(redirect_uri, nonce=nonce)

@app.route('/authorize')
def authorize():
    token = oauth.flask_app.authorize_access_token()
    nonce = session.get('nonce')

    user_info = oauth.flask_app.parse_id_token(token, nonce=nonce)  # or use .get('userinfo').json()
    session['user'] = user_info
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
