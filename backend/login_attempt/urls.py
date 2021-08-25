from django.urls import path

from login_attempt import views

app_name = 'login_attempt'
urlpatterns = [
    path('login/', views.RecordAPIView.as_view()),
]
