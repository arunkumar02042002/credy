import uuid

from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=255)
    uuid = models.CharField(max_length=100, default=uuid.uuid4)
    description = models.TextField(null=True, blank=True)
    genres = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self) -> str:
        return f'{self.title}'


class Collection(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='collections')
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, db_index=True)
    title = models.CharField(max_length=100)
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    movies = models.ManyToManyField(to=Movie, related_name='movies', through='MovieInCollection')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'title'], name='unique_user_title')
        ]

    def __str__(self) -> str:
        return f'{self.user.username}_{self.title}'


class MovieInCollection(models.Model):
    movie = models.ForeignKey(to=Movie, on_delete=models.CASCADE, db_index=True)
    collection = models.ForeignKey(to=Collection, on_delete=models.CASCADE, db_index=True)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['movie', 'collection'], name='unique_movie_in_collection')
        ]

    def __str__(self) -> str:
        return f'movie_{self.movie.title}_in_collection_{self.collection.title}'


class RequestCounter(models.Model):
    count = models.PositiveIntegerField(default=0)
    upadted_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.count)
