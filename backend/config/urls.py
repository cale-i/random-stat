
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf.urls import re_path
from django.views.generic import TemplateView
from django.views.generic import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),


    # ROOT
    path('', TemplateView.as_view(template_name='index.html')),

    # Guest Login JWT
    path('api/v1/auth/guest/', include('guest_login.urls')),

    # JWT
    path('api/v1/auth/', include('djoser.urls')),

    # auth_jwt
    path('api/v1/auth/', include('auth_jwt.urls')),

    # Login Record
    path('api/v1/login-record/', include('login_record.urls')),

    # Login failed
    path('api/v1/login-attempt/', include('failed_login_attempt.urls')),

    # file upload
    path('api/v1/user-profile/', include('user_profile.urls')),

    # API
    path('api/v1/', include('apiv1.urls')),

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

urlpatterns += [
    # Redirect
    # DEBUG分岐以前で定義するとすべてリダイレクトされるためこの位置に置く
    # リダイレクトの場合､/activation/等のURIが機能しないため､index.htmlを返す｡
    # 存在しないURIの場合は､リダイレクトと同様に/を返す
    re_path('', TemplateView.as_view(template_name='index.html')),
    # re_path('', RedirectView.as_view(url='/')),
]
