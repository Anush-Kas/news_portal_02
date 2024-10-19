from rest_framework import routers
from django.urls import path, include
from .views import *


router = routers.DefaultRouter()
router.register(r'news', NewsViewset, basename='news')
router.register(r'articles', ArticlesViewset, basename='articles')


urlpatterns = [
   path('api/', include(router.urls)),
   path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
