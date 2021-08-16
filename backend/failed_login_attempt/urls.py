from django.urls import path
from failed_login_attempt import views


urlpatterns = [
    path('failed/', views.FailedLoginAttemptAPIView.as_view()),
]
