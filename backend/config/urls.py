
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf.urls import re_path
from django.views.generic import TemplateView


urlpatterns = [

    path('admin/', admin.site.urls),

    # djoser Sign Up
    path('api/v1/auth/', include('djoser.urls')),

    # djoser extend Set password for social auth
    path('api/v1/auth/social/', include('djoser_extend.urls')),

    # auth_jwt Login, Logout, Refresh
    path('api/v1/auth/', include('auth_jwt.urls')),

    # Extended social_auth.urls disconnection
    path('api/v1/auth/social/', include('social.urls')),

    # Login Record
    path('api/v1/auth/record/', include('login_attempt.urls')),

    # File Upload
    path('api/v1/user-profile/', include('user_profile.urls')),

    # e-stat
    path('api/v1/', include('apiv1.urls')),

    # RedirectViewの場合､/activation/等のURIが機能しないため､TemplateViewでindex.htmlを返す｡
    # 存在しないURIの場合は､RedirectViewと同様に/を返す
    re_path('', TemplateView.as_view(template_name='index.html')),
]

if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    # 開発用Webサーバ(runserver)使用時のメディアファイル配信設定
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
