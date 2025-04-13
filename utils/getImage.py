import os
import requests

UNSPLASH_ACCESS_KEY = "DRmIdv3BGE_OHcNUoDmusE8mZUEvIy9VR4OW-Yw6UEw"
DEFAULT_IMAGE_URL = "https://images.unsplash.com/photo-1451187580459-43490279c0fa?ixlib=rb-1.2.1&auto=format&fit=crop&w=1352&q=80"

def get_search_query(title, subtitle, content):
    """Determine the best search query based on content"""
    text = f"{title.lower()} {subtitle.lower()} {content.lower()}"
    
    keyword_mapping = {
        'python': ['python', 'flask', 'django'],
        'programming': ['programming', 'coding', 'developer', 'code'],
        'technology': ['technology', 'tech', 'computer', 'software'],
        'web': ['web', 'website', 'internet', 'html', 'css'],
        'design': ['design', 'ui', 'ux', 'interface'],
        'data': ['data', 'database', 'analysis', 'analytics'],
        'science': ['science', 'research', 'physics', 'biology'],
        'business': ['business', 'startup', 'entrepreneur']
    }
    
    matched_categories = []
    for category, keywords in keyword_mapping.items():
        if any(keyword in text for keyword in keywords):
            matched_categories.append(category)
    
    if not matched_categories:
        return "blog writing"
    
    if 'python' in matched_categories:
        return "python programming"
    if 'web' in matched_categories:
        return "web development"
    if 'data' in matched_categories:
        return "data science"
    
    return ' '.join(matched_categories[:2])

def fetch_unsplash_image(query):
    """Fetch a random image from Unsplash based on query"""
    if not UNSPLASH_ACCESS_KEY:
        return DEFAULT_IMAGE_URL
        
    url = "https://api.unsplash.com/photos/random"
    params = {
        'query': query,
        'client_id': UNSPLASH_ACCESS_KEY,
        'orientation': 'landscape'
    }
    
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        return response.json()['urls']['regular']
    except (requests.RequestException, KeyError):
        return DEFAULT_IMAGE_URL

def get_blog_image(title, subtitle, content):
    """Main utility function to get appropriate image for blog"""
    query = get_search_query(title, subtitle, content)
    return fetch_unsplash_image(query)