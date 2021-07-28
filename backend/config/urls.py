from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf.urls import re_path
from django.views.generic import TemplateView
from django.views.generic import RedirectView


from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),


    # ROOT
    path('', TemplateView.as_view(template_name='index.html')),

    # JWT
    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/auth/', include('djoser.urls.jwt')),
    
    # API
    path('api/v1/', include('apiv1.urls')),
    
    # Redirect
    re_path('', RedirectView.as_view(url='/')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
