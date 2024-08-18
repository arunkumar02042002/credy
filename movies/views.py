from rest_framework.generics import ListCreateAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import CollectionCreateSerializer, CollectionListSerializer
from .models import Collection, Movie
from .helpers import get_favorite_genres

class CollectionListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            'collection_uuid':serializer.data['uuid']
        }, status=status.HTTP_201_CREATED)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'is_success':True,
            'data':{
                'collections':serializer.data
            },
            'favourite_genres':get_favorite_genres(queryset)
        })
    
    def get_queryset(self):
        return Collection.objects.filter(user=self.request.user).prefetch_related('movies')
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CollectionListSerializer
        return CollectionCreateSerializer
