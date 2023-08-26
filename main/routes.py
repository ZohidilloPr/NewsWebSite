from django.urls import path
from .views import (
    CategoryListView, CategoryDetailView,
    
    NewsListView, NewsDetailView, NewsGETDetailWithSlug, NewsListCategoriWithSlug, 
    BreakingNewsListView,TheMostReadNews, Comment, TheMostWriteCommenNews, ChoicedCategoriesNews,
    TheLastFiveNews, UzbekistanInSevenDayFourNews, TodayNews, TheLastInSevenDaysNews, TheLastIn30DaysNews,
    
    AdsOnTopView, AdsOnMiddleView, AdsOnLeftView, AdsOnBottomView
) # 16
urlpatterns = [
    
    # """ START CATEGORY URLS """
    path(
        "category/",
        CategoryListView.as_view(),
        name="category_list"
    ),
    path(
        "category/<pk>/",
        CategoryDetailView.as_view(),
        name="category_detail"
    ),
    # """ END CATEGORY URLS """
    
    # """ START NEWS URLS """
    path(
        "news/", 
        NewsListView.as_view(),
        name="news_list"
    ),
    path(
        "news/filter/<slug>/",
        NewsListCategoriWithSlug.as_view(),
        name="news_list_slug"
    ),
    path(
        "news/detail/<int:pk>/",
        NewsDetailView.as_view(),
        name="news_detail_pk"
    ),
    path(
        "news/detail/slug/<slug>/",
        NewsGETDetailWithSlug.as_view(),
        name="news_detail_slug"
    ),
    path(
        "news/breaking/",
        BreakingNewsListView.as_view(),
        name="news_breaking"
    ),
    path(
        "news/carusel/",
        TheLastFiveNews.as_view(),
        name="news_carusel"
    ),
    path(
        "news/carusel/right/",
        UzbekistanInSevenDayFourNews.as_view(),
        name="news_carusel_right"
    ),
    path(
        "news/read/",
        TheMostReadNews.as_view(),
        name="news_read"
    ),
    path(
        "news/write/",
        TheMostWriteCommenNews.as_view(),
        name="news_write"
    ),
    path( 
        "news/choiced/",
        ChoicedCategoriesNews.as_view(),
        name="news_choiced"
    ),
    path( 
        "news/today/",
        TodayNews.as_view(),
        name="news_today"
    ),
    path( 
        "news/sevendays/",
        TheLastInSevenDaysNews.as_view(),
        name="news_7"
    ),
    path( 
        "news/30days/",
        TheLastIn30DaysNews.as_view(),
        name="news_30"
    ),
    
    # """ END NEWS URLS """
    
    # """ START COMMENTS URLS """
    path(
        "comment/<int:news_id>/",
        Comment,
        name = "comment_list_crate"
    ),
    # """ END COMMENTS URLS """
    
    # """ START ADS URLS """
    path(
        "ads/top/",
        AdsOnTopView.as_view(),
        name = "ads_top"
    ),
    path(
        "ads/middle/",
        AdsOnMiddleView.as_view(),
        name = "ads_middle"
    ),
    path(
        "ads/left/",
        AdsOnLeftView.as_view(),
        name = "ads_left"
    ),
    path(
        "ads/bottom/",
        AdsOnBottomView.as_view(),
        name = "ads_bottom"
    ),
    # """ END ADS URLS """
]