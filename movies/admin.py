from django.contrib import admin
from .models import Movie, Collection, MovieInCollection, RequestCounter

# Register your models here.
admin.site.register(Collection)
admin.site.register(Movie)
admin.site.register(MovieInCollection)
admin.site.register(RequestCounter)