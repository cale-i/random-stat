from auth_jwt.views import RefreshTokenSetCookieMixin
from django.contrib.auth import REDIRECT_FIELD_NAME, get_user_model
from django.views.decorators.cache import never_cache
from djoser.social.serializers import ProviderAuthSerializer
from djoser.social.views import ProviderAuthView
from rest_framework import status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from social_core.actions import do_disconnect
from social_django.models import UserSocialAuth
from social_django.utils import load_backend, load_strategy

from .serializers import CustomProviderAuthSerializer, UserSocialAuthSerializer

User = get_user_model()


class UserSocialAuthAPIView(views.APIView):
    # 連携済みサービス一覧を返す
    serializer_class = UserSocialAuthSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = User.objects.get(pk=request.user.id)

        queryset = UserSocialAuth.objects.filter(user=user)
        serializer = UserSocialAuthSerializer(instance=queryset, many=True)
        data = {
            'valid_password': user.has_usable_password(),
            'providers': serializer.data
        }
        return Response(data, status.HTTP_200_OK)


class DisconnectView(views.APIView):
    permission_classes = [IsAuthenticated]

    @never_cache
    def post(self, request, backend, * args, **kwargs):

        strategy = load_strategy(request)
        backend = load_backend(strategy, backend,
                               redirect_uri=None)

        return do_disconnect(
            backend,
            request.user,
            redirect_name=REDIRECT_FIELD_NAME
        )


class CustomProviderAuthView(ProviderAuthView, RefreshTokenSetCookieMixin):

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            # アカウント連携
            return CustomProviderAuthSerializer
        # アカウント登録
        return ProviderAuthSerializer
