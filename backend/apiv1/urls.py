from django.urls import path, include

from apiv1 import views

app_name = 'apiv1'
urlpatterns = [
    path('test/', views.ChronologicalListAPIView.as_view()),
    path('chronological/', views.ChronologicalAPIView.as_view()),


]
