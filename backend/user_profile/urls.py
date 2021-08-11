from django.urls import path, include

from user_profile import views

app_name = 'avatar'
urlpatterns = [
    # file upload
    path('avatar/', views.UserAvaterAPIView.as_view()),

]
