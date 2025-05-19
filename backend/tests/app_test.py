#run tests: pytest -v backend/tests
# https://testdriven.io/blog/flask-pytest/ + chatgpt syntax reference
import sys
import os
import pytest
import mongomock
import requests
from unittest.mock import patch
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app


# the following client(monkeypatch) is from CHATGPT-----------------------------
@pytest.fixture
def client(monkeypatch):
    # Use mongomock and patch get_db() to return mocked collection
    mock_db = mongomock.MongoClient().db.collection

    # Patch collection reference in app
    monkeypatch.setattr("app.collection", mock_db)

    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
#---------------------------------------------------------------------------------

def test_get_api_key(client):
    os.environ['NYT_API_KEY'] = '8fvDO25EE7zndsrAbATBBLlAusQP9S6N'
    response = client.get('/api/key')
    assert response.status_code == 200
    assert response.get_json()['apiKey'] == '8fvDO25EE7zndsrAbATBBLlAusQP9S6N'

#TEST NYT API - Making sure it returns data in expected format
def get_nyt_data():
    apiKey = os.getenv('NYT_API_KEY')
    response = requests.get(f'https://api.nytimes.com/svc/search/v2/articlesearch.json?api-key={apiKey}')
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
def test_api_data_format():
    data = get_nyt_data()
    assert data is not None, "1"
    for article in data['response']['docs']:
        assert isinstance(article['headline']['main'], str), f"headline"
        assert isinstance(article['web_url'], str), f"url"
        assert isinstance(article['byline']['original'], str), f"byline"
        assert isinstance(article['abstract'], str), f"abstract"
        assert isinstance(article.get('multimedia', {}), dict), f"multimedia"

def test_add_data(client):
    # mock comment
    test_comment = {
        "article": "test_headline",
        "username": "test_user",
        "comment": "testing testing",
        "comment_id": "",
        "isReply": False
    }
    response = client.post('/api/add_data', json=test_comment)
    assert response.status_code == 201
    data = response.get_json()
    assert 'message' in data
    assert data['message'] == 'Data added to MongoDB'

# test if comments are being returned correctly
def test_get_comments(client):
    # Add a mock comment first
    client.post('/api/add_data', json={
        "article": "test_article",
        "username": "tester",
        "comment": "Hello world",
        "comment_id": "",
        "isReply": False
    })
    response = client.get('/get_comments?article=test_article')
    assert response.status_code == 200
    comments = response.get_json()
    assert isinstance(comments, list)
    for comment in comments:
        assert comment['article'] == 'test_article'
        assert not comment['isReply']
        assert '_id' in comment
        assert 'comment' in comment

# test if replies are being returned correctly
def test_get_replies(client):
    # post mock comment
    client.post('/api/add_data', json={
        "article": "test_article",
        "username": "fake_user",
        "comment": "reply_msg",
        "comment_id": "parent_cmt",
        "isReply": True
    })
    response = client.get('/get_replies?comment_id=parent_cmt')
    assert response.status_code == 200
    replies = response.get_json()
    assert isinstance(replies, list)
    for reply in replies:
        assert reply['comment_id'] == "parent_cmt"
        assert reply['isReply']

def test_add_data_empty(client):
    response = client.post('/api/add_data', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'No data provided'

def test_add_data_exception(client):
    test_comment = {
        "article": "test",
        "username": "test",
        "comment": "test",
        "comment_id": "",
        "isReply": False
    }

    # CITE: CHATPGT ---Patch insert_one to raise an exception
    with patch('app.collection.insert_one', side_effect=Exception("Mock insert failure")):
    #-----------------
        response = client.post('/api/add_data', json=test_comment)
        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'Mock insert failure' in data['error']

def test_home_logged_in(client):
    # CITE: CHATGPT-------------------------------
    with client.session_transaction() as session:
        session['user'] = {
            'email': 'test@example.com',
            'name': 'Amy'
        }
    #--------------------------------

    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['loggedIn'] is True
    assert data['name'] == 'Amy'
    assert data['email'] == 'test@example.com'

def test_home_not_logged_in(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['loggedIn'] is False

def test_logout(client):
    # CITE: CHATGPT-------------------------------
    with client.session_transaction() as sess:
    #--------------------------------------------
        sess['user'] = {'email': 'test@example.com'}
        
    response = client.get('/logout')
    assert response.status_code == 302
    assert response.headers['Location'] == '/'
    with client.session_transaction() as sess:
        assert 'user' not in sess
# Run:
    # coverage run -m pytest
    # coverage html