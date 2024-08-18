from django.urls import path

from .views import CollectionListCreateView, CollectionRetrieveUpdateDestroyView

urlpatterns = [
    path('collections,/', view=CollectionListCreateView.as_view(), name='collection-list-create'),
    path('collection/<uuid:uuid>/', view=CollectionRetrieveUpdateDestroyView.as_view(), name='collection-retrive-update-destroy')
]
