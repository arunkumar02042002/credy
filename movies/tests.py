import uuid

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Movie, Collection, MovieInCollection

User = get_user_model()

class MovieModelTest(TestCase):
    def setUp(self):
        self.movie = Movie.objects.create(
            title='Inception',
            uuid='123e4567-e89b-12d3-a456-426614174000',
            description='A mind-bending thriller',
            genres='Sci-Fi, Thriller'
        )

    def test_movie_creation(self):
        self.assertEqual(self.movie.title, 'Inception')
        self.assertEqual(self.movie.uuid, '123e4567-e89b-12d3-a456-426614174000')
        self.assertEqual(self.movie.description, 'A mind-bending thriller')
        self.assertEqual(self.movie.genres, 'Sci-Fi, Thriller')


class CollectionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.collection = Collection.objects.create(
            user=self.user,
            title='My Favorite Movies',
            description='A collection of my favorite movies'
        )

    def test_collection_creation(self):
        self.assertEqual(self.collection.user, self.user)
        self.assertEqual(self.collection.title, 'My Favorite Movies')
        self.assertEqual(self.collection.description, 'A collection of my favorite movies')

    def test_unique_user_title_constraint(self):
        """Test the unique constraint on user and title in the Collection model"""
        with self.assertRaises(Exception):
            Collection.objects.create(
                user=self.user,
                title='My Favorite Movies',
                description='A duplicate collection title'
            )


class MovieInCollectionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.movie = Movie.objects.create(
            title='Inception',
            uuid='123e4567-e89b-12d3-a456-426614174000',
            description='A mind-bending thriller',
            genres='Sci-Fi, Thriller'
        )
        self.collection = Collection.objects.create(
            user=self.user,
            title='My Favorite Movies',
            description='A collection of my favorite movies'
        )
        self.movie_in_collection = MovieInCollection.objects.create(
            movie=self.movie,
            collection=self.collection
        )

    def test_movie_in_collection_creation(self):
        self.assertEqual(self.movie_in_collection.movie.title, 'Inception')
        self.assertEqual(self.movie_in_collection.collection.title, 'My Favorite Movies')


    def test_unique_movie_in_collection_constraint(self):
        """Test the unique constraint on movie and collection in the MovieInCollection model"""
        with self.assertRaises(Exception):
            MovieInCollection.objects.create(
                movie=self.movie,
                collection=self.collection
            )


class CollectionListCreateViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.url = reverse('collection-list-create')

        self.movie1 = Movie.objects.create(
            title="Movie 1",
            uuid="cc51020f-1bd6-42ad-84e7-e5c0396435a8",
            description="Description for movie 1",
            genres="Action,Commedy,Fantasy,Horror"
        )
        self.movie2 = Movie.objects.create(
            title="Movie 2",
            uuid="9a4fcb67-24f6-4cda-8f49-ad66b689f481",
            description="Description for movie 2",
            genres="Commedy,Drama,Horror,Love"
        )
        self.movie3 = Movie.objects.create(
            title="Movie 3",
            uuid="9a4fcb67-24f6-4cda-8f49-ad66b689f486",
            description="Description for movie 3",
            genres="Commedy,Drama,Horror"
        )
        self.collection_data = {
            "title": "My Collection",
            "description": "A collection of my favorite movies",
            "movies": [
                {
                    "title": "Movie 1",
                    "description": "Description for movie 1",
                    "genres": "Action",
                    "uuid": "cc51020f-1bd6-42ad-84e7-e5c0396435a8"
                },
                {
                    "title": "Movie 2",
                    "description": "Description for movie 2",
                    "genres": "Comedy,Drama",
                    "uuid": "9a4fcb67-24f6-4cda-8f49-ad66b689f481"
                },
                {
                    "title":"Movie 3",
                    "uuid":"9a4fcb67-24f6-4cda-8f49-ad66b689f486",
                    "description":"Description for movie 3",
                    "genres":"Commedy,Drama,Horror"
                }
            ]
        }

    def test_create_collection(self):
        response = self.client.post(self.url, self.collection_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('collection_uuid', response.data)
        collection_uuid = response.data['collection_uuid']
        collection = Collection.objects.get(uuid=collection_uuid)

        self.assertEqual(collection.title, self.collection_data['title'])
        self.assertEqual(collection.description, self.collection_data['description'])
        self.assertEqual(collection.movies.count(), 3)

    def test_list_collections(self):
        Collection.objects.create(user=self.user, title="Collection 1", description="Desc 1")
        Collection.objects.create(user=self.user, title="Collection 2", description="Desc 2")

        response = self.client.get(self.url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']['collections']), 2)
        self.assertTrue(response.data['is_success'])
        self.assertIn('favourite_genres', response.data)

    def test_get_favourite_genres(self):
        collection = Collection.objects.create(user=self.user, title="Collection 1", description="Desc 1")
        collection.movies.add(self.movie1, self.movie2, self.movie3)

        response = self.client.get(self.url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['favourite_genres'], ['Commedy', 'Horror', 'Drama'])

    def test_create_collection_with_existing_movies(self):
        existing_movie_uuid = self.movie1.uuid
        collection_data_with_existing_movie = {
            "title": "New Collection with Existing Movie",
            "description": "Collection with an existing movie",
            "movies": [
                {
                    "title": "Movie 1",
                    "description": "Description for movie 1",
                    "genres": "Action",
                    "uuid": existing_movie_uuid
                },
            ]
        }

        response = self.client.post(self.url, collection_data_with_existing_movie, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        collection_uuid = response.data['collection_uuid']
        collection = Collection.objects.get(uuid=collection_uuid)

        self.assertEqual(collection.movies.count(), 1)
        self.assertEqual(collection.movies.first().uuid, existing_movie_uuid)