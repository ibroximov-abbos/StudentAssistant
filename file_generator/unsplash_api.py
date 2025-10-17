import requests

import os
API_KEY = os.getenv("UNSPLASH_API_KEY")

def download_and_save_image(url, filename):
    """Rasmni faylga saqlaydi"""
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        return filename
    return None


def search_unsplash(query):
    url = f"https://api.unsplash.com/search/photos"
    params = {
        "query": query,
        "per_page": 5
    }
    headers = {
        "Authorization": f"Client-ID {API_KEY}"
    }
    
    response = requests.get(url, headers=headers, params=params)
    print(response, 'response')
    
    if response.status_code == 200:
        data = response.json()
        return data['results']
    else:
        print(f"Xato: {response.status_code}")
        return []
    


def image(theme):
    i = 1
    photos = search_unsplash(theme)
    for photo in photos:
        download_and_save_image(photo['urls']['regular'], f"{theme}-{i}")
        print(photo['urls']['regular'])
        i += 1



