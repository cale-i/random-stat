from django.urls import re_path, path
from django.conf import settings

from social_core.utils import setting_name

from social import views

extra = getattr(settings, setting_name('TRAILING_SLASH'), True) and '/' or ''

urlpatterns = [
    # ソーシャルアカウントを使ってログイン
    re_path(
        r"^o/(?P<provider>\S+)/$",
        views.CustomProviderAuthView.as_view(),
        name="provider-auth",
    ),

    # disconnection
    re_path(r'^disconnect/(?P<backend>[^/]+){0}$'.format(extra), views.DisconnectView.as_view(),
            name='disconnect'),

    # ログイン後､追加のアカウント連携
    re_path(
        r"^connect/(?P<provider>\S+)/$",
        views.ConnectView.as_view(),
        name="provider-auth",
    ),

    path('services/', views.UserSocialAuthAPIView.as_view())
]
