from django.urls import path, include

from user_profile import views

app_name = 'upload'
urlpatterns = [
    # file upload
    path('avatar/', views.UserAvaterAPIView.as_view()),

]
