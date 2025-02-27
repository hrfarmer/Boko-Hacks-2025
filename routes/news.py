from flask import Blueprint, render_template, jsonify, request
import requests
import json
import os 

news_bp = Blueprint('news', __name__, url_prefix='/apps/news')

# Base URL for the News API
NEWS_API_BASE_URL = "https://saurav.tech/NewsAPI"

# Mapping of our categories to API categories
CATEGORY_MAPPING = {
    'business': 'business',
    'technology': 'technology',
    'world': 'general'
}

DEFAULT_COUNTRY = 'us'

INTERNAL_NEWS = [
    {
        "title": "CONFIDENTIAL: Security Breach Report Q3",
        "description": "Details of recent security incidents affecting customer data. For internal review only.",
        "url": "#internal-only",
        "publishedAt": "2025-01-15T08:30:00Z",
        "urlToImage": ""
    },
    {
        "title": "CONFIDENTIAL: Upcoming Product Launch",
        "description": "Specifications for our next-gen product launch in Q2. Contains proprietary information.",
        "url": "#internal-only",
        "publishedAt": "2025-02-01T10:15:00Z",
        "urlToImage": ""
    },
    {
        "title": "CONFIDENTIAL: Internal API Credentials",
        "description": f"API_KEY: {os.getenv('API_KEY')}  ADMIN_KEY: {os.getenv('ADMIN_KEY')}",
        "url": "#internal-only",
        "publishedAt": "2025-01-30T14:45:00Z",
        "urlToImage": ""
    }
]

@news_bp.route('/')
def news_page():
    """Render the news page"""
    return render_template('news.html')

@news_bp.route('/fetch', methods=['GET'])
def fetch_news():
    """Fetch news from the News API with a vulnerability"""
    try:
        # Get category from request, default to business
        category = request.args.get('category', 'business')
        
        # Map our category to API category
        api_category = CATEGORY_MAPPING.get(category, 'business')
        api_url = f"{NEWS_API_BASE_URL}/top-headlines/category/{api_category}/{DEFAULT_COUNTRY}.json"
        
        print(f"Fetching news from: {api_url}")
        
        # Fetch news from external API
        response = requests.get(api_url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])[:10]  # Limit to 10 articles
            
            filter_param = request.args.get('filter', '{}')
            
            try:
                filter_options = json.loads(filter_param)
                print(f"Filter options: {filter_options}")
                
                if filter_options.get('showInternal') == True:
                    # Add internal news to the results
                    print("Adding internal news to results!")
                    articles = INTERNAL_NEWS + articles
            except json.JSONDecodeError:
                print(f"Invalid filter parameter: {filter_param}")
            
            # Transform the data to match our expected format
            transformed_data = {
                'success': True,
                'category': category,
                'data': []
            }
            
            # Process articles
            for article in articles:
                transformed_data['data'].append({
                    'title': article.get('title', 'No Title'),
                    'content': article.get('description', 'No content available'),
                    'date': article.get('publishedAt', ''),
                    'readMoreUrl': article.get('url', '#'),
                    'imageUrl': article.get('urlToImage', '')
                })
            
            return jsonify(transformed_data)
        else:
            return jsonify({
                'success': False,
                'error': f'Failed to fetch news. Status code: {response.status_code}'
            }), response.status_code
    except Exception as e:
        print(f"Error fetching news: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500