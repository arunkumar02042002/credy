from collections import Counter

import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings

def get_favorite_genres(collections):
    '''
    function to find favorite genres of a user
    '''
    genres = []
    if len(collections) == 0:
        return genres
    
    for collection in collections:
        for movie in collection.movies.all():
            if movie.genres is not None:
                genres += movie.genres.split(',')
    counter = Counter(genres)
    genres = sorted(counter.keys(), key=lambda genre: -counter[genre])
    if len(genres) <= 3:
        return genres
    return genres[:3]


class CredyMovieUtil:

    @staticmethod
    def get_movies(page=1) -> dict:
        url = f'https://demo.credy.in/api/v1/maya/movies/?page={page}'

        tries = 3
        while tries > 0:
            response = requests.get(url=url, verify=False, timeout=60)
            if response.status_code != 200:
                tries -= 1
                continue
            result = response.json()
            result['next_page_num'] = int(page)+1 if result['next'] else None
            result['previous_page_num'] = int(page)-1 if int(page) > 0 else None
            return result, True
        return {}, False
