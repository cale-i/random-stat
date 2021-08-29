from django.urls import re_path

from social import views

urlpatterns = [
    re_path(
        r"^o/(?P<provider>\S+)/$",
        views.CustomProviderAuthView.as_view(),
        name="provider-auth",
    )
]
