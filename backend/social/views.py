from djoser.social.views import ProviderAuthView
from auth_jwt.views import CookieTokenObtainPairView


class CustomProviderAuthView(ProviderAuthView, CookieTokenObtainPairView):
    pass
