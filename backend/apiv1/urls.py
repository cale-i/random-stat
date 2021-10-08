from django.urls import path

from apiv1 import views

app_name = 'apiv1'
urlpatterns = [
    path('timeseries/', views.TimeSeriesAPIView.as_view()),
    path('timeseries/statscode/', views.StatsCodeListView.as_view()),
    path('timeseries/area/', views.AreaListView.as_view()),
    path('timeseries/category/', views.CategoryListView.as_view()),
    path('timeseries/history/', views.StatHistoryView.as_view()),
    path('search/', views.TimeSeriesAPIView.as_view()),
    path('search/statscode/', views.StatsCodeAPIView.as_view()),
    path('timeseries/favorites/', views.FavoritesView.as_view()),
    path('timeseries/favorites/isfavorites/',
         views.IsFavoriteView.as_view()),
]
