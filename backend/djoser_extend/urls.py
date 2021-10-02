from django.urls import path
from . import views

urlpatterns = [
    # set password
    path('users/set_password/', views.setPasswordView.as_view()),
]
