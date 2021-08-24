from django.urls import path

from login_record import views

app_name = 'login_record'
urlpatterns = [
    # file upload
    path('', views.RecordAPIView.as_view()),
]
