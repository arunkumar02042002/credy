from django.shortcuts import get_object_or_404

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from . import serializers as movie_serializers
from .models import Collection
from .helpers import get_favorite_genres, CredyMovieUtil


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
            return movie_serializers.CollectionListSerializer
        return movie_serializers.CollectionCreateSerializer


class CollectionRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = movie_serializers.CollectionSerializer
    lookup_field = 'uuid'

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def get_object(self):
        queryset = self.get_queryset()
        return get_object_or_404(queryset, uuid=self.kwargs.get(self.lookup_field))
    
    def get_queryset(self):
        return Collection.objects.filter(user=self.request.user).prefetch_related('movies')
    

class MovieListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        page = request.query_params.get('page', 1)
        result, success = CredyMovieUtil.get_movies(page=page)
        if success:
            return Response(result)
        
        return Response({
            'details':'Unable to fetch movies after many tries.'
        }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        