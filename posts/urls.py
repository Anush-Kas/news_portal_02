from django.urls import path
from django.views.decorators.cache import cache_page

from .views import (PostCreate, PostDelete, PostDetail, PostList, PostSearch,
                    PostUpdate, subscriptions)

app_name = 'posts'

urlpatterns = [
    path('', cache_page(60*5)(PostList.as_view()), name='posts_list'),
    path('posts/search/', PostSearch.as_view(), name='posts_search'),
    path('post/<pk>', cache_page(60*5)(PostDetail.as_view()), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('post/<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('subscriptions/', subscriptions, name='subscriptions'),
]
