from django.urls import path

from apiv1 import views

app_name = 'apiv1'
urlpatterns = [
    path('timeseries/', views.TimeSeriesAPIView.as_view()),
    path('search/', views.TimeSeriesAPIView.as_view()),
    path('search/statscode/', views.StatsCodeAPIView.as_view()),



]
