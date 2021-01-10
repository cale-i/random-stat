from django.urls import path, include

from apiv1 import views

app_name = 'apiv1'
urlpatterns = [
    path('chronological/', views.ChronologicalAPIView.as_view()),
    path('search/', views.ChronologicalAPIView.as_view()),



]
