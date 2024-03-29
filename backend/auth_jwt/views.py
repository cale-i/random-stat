from django.conf import settings
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .guest import get_guest_credentials, initialize_guest_data
from .serializers import CookieTokenRefreshSerializer
from .signals import login_signal, logout_signal
from .utils import has_valid_password, update_refresh_time

cookie_max_age = settings.SIMPLE_JWT.get(
    'REFRESH_TOKEN_LIFETIME').total_seconds()
samesite = settings.JWT_COOKIE.get('SAMESITE')
secure = settings.JWT_COOKIE.get('SECURE')


class RefreshTokenSetCookieMixin(views.APIView):
    def finalize_response(self, request, response, *args, **kwargs):

        access_token = response.data.get('access', None)
        refresh_token = response.data.get('refresh', None)

        if access_token:
            logout_signal(request, response)
            login_signal(request, response)

            # 有効なパスワードが設定されているか
            response.data['valid_password'] = has_valid_password(access_token)

        if refresh_token:
            response.set_cookie(
                'refresh_token',
                refresh_token,
                max_age=cookie_max_age,
                httponly=True,
                samesite=samesite,
                secure=secure,
            )
            del response.data['refresh']

        return super().finalize_response(request, response, *args, **kwargs)


class CookieTokenObtainPairView(TokenObtainPairView, RefreshTokenSetCookieMixin):
    pass


class CookieTokenRefreshView(TokenRefreshView):
    def finalize_response(self, request, response, *args, **kwargs):

        access_token = response.data.get('access', None)
        refresh_token = response.data.get('refresh', None)

        if access_token:
            update_refresh_time(access_token=access_token)

            # 有効なパスワードが設定されているか
            response.data['valid_password'] = has_valid_password(access_token)

        if refresh_token:
            response.set_cookie(
                'refresh_token',
                refresh_token,
                max_age=cookie_max_age,
                httponly=True,
                samesite=samesite,
                secure=secure,
            )
            del response.data['refresh']

        return super().finalize_response(request, response, *args, **kwargs)
    serializer_class = CookieTokenRefreshSerializer


class GuestCookieTokenObtainPairView(CookieTokenObtainPairView):
    def post(self, request, *args, **kwargs):
        initialize_guest_data()
        serializer = self.get_serializer(data=get_guest_credentials())
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class LogoutTokenRefreshView(TokenRefreshView):
    '''ログアウト時に呼び出し､user_logged_out signalを経由してログイン情報の記録を行う'''
    serializer_class = CookieTokenRefreshSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('access'):
            # ログアウトシグナル
            logout_signal(request, response)

            del response.data['access']

        if response.data.get('refresh'):
            # Cookieに保存された旧 Refresh Token を削除
            response.delete_cookie('refresh_token')

            del response.data['refresh']

        return super().finalize_response(request, response, *args, **kwargs)
