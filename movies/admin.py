from django.contrib import admin
from .models import Movie, Collection, MovieInCollection

# Register your models here.
admin.site.register(Collection)
admin.site.register(Movie)
admin.site.register(MovieInCollection)