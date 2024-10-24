from django.urls import path
from django.views.decorators.cache import cache_page

from .views import (NewsCreate, ArticleCreate,
                    NewsDelete, ArticleDelete,
                    NewsDetail, ArticleDetail,
                    PostList, PostSearch,
                    NewsUpdate, ArticleUpdate,
                    subscriptions)

app_name = 'posts'

urlpatterns = [
    path('', cache_page(60*5)(PostList.as_view()), name='posts_list'),
    path('posts/search/', PostSearch.as_view(), name='posts_search'),

    path('news/<pk>', cache_page(60*5)(NewsDetail.as_view()), name='news_detail'),
    path('articles/<pk>', cache_page(60*5)(ArticleDetail.as_view()), name='article_detail'),

    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),

    path('news/<int:pk>/update/', NewsUpdate.as_view(), name='news_update'),
    path('articles/<int:pk>/update/', ArticleUpdate.as_view(), name='article_update'),

    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('article/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),

    path('subscriptions/', subscriptions, name='subscriptions'),
]
