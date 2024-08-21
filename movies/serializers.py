from rest_framework import serializers

from .models import Movie, Collection, RequestCounter

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'genres', 'uuid']


class CollectionCreateSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True, required=False)
    
    class Meta:
        model = Collection
        fields = ['title', 'description', 'movies', 'uuid']
        read_only_fields = ['uuid']

    def create(self, validated_data):
        user = self.context['request'].user
        movies_data  = validated_data.pop('movies', [])
        all_movies = []
        
        if len(movies_data ) > 0:
            uuids = [movie.get('uuid', None) for movie in movies_data]
            existing_movies = Movie.objects.filter(uuid__in=uuids)

            # Find existing movies
            existing_uuids = set(existing_movies.values_list('uuid', flat=True))

            # Create new movies (those not already existing)
            new_movies = [
                Movie(**movie) for movie in movies_data
                if movie['uuid'] not in existing_uuids
            ]
            
            if len(new_movies) > 0:
                Movie.objects.bulk_create(new_movies)

            # Add both existing and newly created movies to the collection
            all_movies = list(existing_movies) + new_movies

        collection, created = Collection.objects.get_or_create(title=validated_data.pop('title'), user=user, defaults=validated_data)
        if all_movies: collection.movies.add(*all_movies)

        return collection


class CollectionListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collection
        fields = ['title', 'description', 'uuid']


class CollectionSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True, read_only=True)

    class Meta:
        model = Collection
        fields = ['title', 'description', 'movies', 'uuid']
        read_only_fields = ['uuid']


class RequestCounterSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestCounter
        fields = ['count']
