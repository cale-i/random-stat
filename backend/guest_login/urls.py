from django.urls import path

from guest_login import views

app_name = 'guest_login'
urlpatterns = [

    path('jwt/create/', views.GuestLoginAPIView.as_view()),

]
