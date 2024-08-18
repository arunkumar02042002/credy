from collections import Counter

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