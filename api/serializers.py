from posts.models import *
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
   class Meta:
       model = Post
       fields = ['id', 'title', 'text', 'author', 'category', 'kind', 'created_at', 'rating']
