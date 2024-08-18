from django.urls import path

from .views import CollectionListCreateView, CollectionRetrieveUpdateDestroyView, MovieListView

urlpatterns = [
    path('movies/', view=MovieListView.as_view(), name='movies'),
    path('collections,/', view=CollectionListCreateView.as_view(), name='collection-list-create'),
    path('collection/<uuid:uuid>/', view=CollectionRetrieveUpdateDestroyView.as_view(), name='collection-retrive-update-destroy')
]
