from django.urls import path

from login_record import views

app_name = 'login_record'
urlpatterns = [
    # file upload
    path('login/', views.LoginRecorderAPIView.as_view()),
    path('logout/', views.LogoutRecorderAPIView.as_view()),
]
