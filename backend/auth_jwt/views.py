from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from django.conf import settings
from .guest import get_guest_credentials, initialize_guest_data


from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework import status
from rest_framework.response import Response
from .signals import login_signal


cookie_max_age = settings.SIMPLE_JWT.get(
    'REFRESH_TOKEN_LIFETIME').total_seconds()
samesite = settings.JWT_COOKIE.get('SAMESITE')
secure = settings.JWT_COOKIE.get('SECURE')


class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None

    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('refresh_token')
        if attrs['refresh']:
            return super().validate(attrs)
        else:
            raise InvalidToken(
                'No valid token found in cookie \'refresh_token\'')


class CookieTokenObtainPairView(TokenObtainPairView):
    def finalize_response(self, request, response, *args, **kwargs):

        if response.data.get('access'):
            login_signal(request, response)

        if response.data.get('refresh'):
            response.set_cookie(
                'refresh_token',
                response.data['refresh'],
                max_age=cookie_max_age,
                httponly=True,
                samesite=samesite,
                secure=secure,
            )
            del response.data['refresh']

        return super().finalize_response(request, response, *args, **kwargs)


class CookieTokenRefreshView(TokenRefreshView):
    def finalize_response(self, request, response, *args, **kwargs):

        if response.data.get('refresh'):
            response.set_cookie(
                'refresh_token',
                response.data['refresh'],
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
