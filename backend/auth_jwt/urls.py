from django.urls import path

from auth_jwt import views

app_name = 'auth_jwt'
urlpatterns = [

    path('jwt/create/', views.CookieTokenObtainPairView.as_view()),
    path('jwt/create/guest/', views.GuestCookieTokenObtainPairView.as_view()),
    path('jwt/refresh/', views.CookieTokenRefreshView.as_view()),
    path('jwt/logout/', views.LogoutTokenRefreshView.as_view()),


]
