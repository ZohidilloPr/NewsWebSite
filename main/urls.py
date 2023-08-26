from django.urls import path
from .views import (
    Home, DetailNews, 
    SearchEngine, GetAllNewsList,
    FilterByCategory, CreateComment, FilterByDate, ContactUs, subscribe
)


urlpatterns = [
    path(
        '',
        Home,
        name='home'
    ),
    path(
        'yangilik/<slug>/',
        DetailNews,
        name='detail_news'
    ),
    path(
        'category/<id>/',
        FilterByCategory,
        name='filter_by_category'
    ),
    path(
        'comments/',
        CreateComment,
        name='comments'
    ),
    path(
        'search/',
        SearchEngine,
        name='search_engine'
    ),
    path(
        'filter_date/<date>/',
        FilterByDate,
        name='filter_by_date'
    ),
    path(
        'news/',
        GetAllNewsList.as_view(),
        name='news_list_view'
    ),
    path(
        'contact/',
        ContactUs,
        name='contact_us'
    ),
    path(
        'subs/',
        subscribe,
        name='subscribe'
    ),
]