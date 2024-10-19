from rest_framework import viewsets
from rest_framework import permissions

from .serializers import *
from posts.models import *


class NewsViewset(viewsets.ModelViewSet):
    queryset = Post.objects.filter(kind='NW')
    serializer_class = PostSerializer


class ArticlesViewset(viewsets.ModelViewSet):
    queryset = Post.objects.filter(kind='AR')
    serializer_class = PostSerializer
