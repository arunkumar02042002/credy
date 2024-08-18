import uuid

from django.test import TestCase
from django.contrib.auth import get_user_model

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
