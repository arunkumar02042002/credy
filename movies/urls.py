from django.urls import path

from . import views as movies_views

urlpatterns = [
    path('movies/', view=movies_views.MovieListView.as_view(), name='movies'),
    path('collections,/', view=movies_views.CollectionListCreateView.as_view(), name='collection-list-create'),
    path('collection/<uuid:uuid>/', view=movies_views.CollectionRetrieveUpdateDestroyView.as_view(), name='collection-retrive-update-destroy'),
    path('request-count/', view=movies_views.RequestCounterView.as_view(), name='request-count'),
    path('request-count/reset/', view=movies_views.ResetCounterView.as_view(), name='request-count-reset'),
]
