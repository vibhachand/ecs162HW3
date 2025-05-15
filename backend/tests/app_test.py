import sys
import os
import pytest
import requests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app
#run tests: pytest -v backend/tests
# https://testdriven.io/blog/flask-pytest/ + chatgpt syntax reference
#these tests both passed on my VS code workspace
#TEST 1: API Key - Making sure Flask server returns API key as expected
@pytest.fixture
def client():
    os.environ['NYT_API_KEY'] = '8fvDO25EE7zndsrAbATBBLlAusQP9S6N'
    with app.test_client() as client:
        yield client

def test_get_api_key(client):
    response = client.get('/api/key')
    assert response.status_code == 200
    data = response.get_json()
    assert data['apiKey'] == '8fvDO25EE7zndsrAbATBBLlAusQP9S6N'

#TEST 2: NYT API - Making sure it returns data in expected format
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