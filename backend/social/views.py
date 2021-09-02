from auth_jwt.views import CookieTokenObtainPairView
from django.contrib.auth import REDIRECT_FIELD_NAME, get_user_model
from django.views.decorators.cache import never_cache
from djoser.social.views import ProviderAuthView
from rest_framework import status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from social_core.actions import do_disconnect
from social_django.models import UserSocialAuth
from social_django.utils import load_backend, load_strategy

from social.serializers import UserSocialAuthSerializer

User = get_user_model()


class CustomProviderAuthView(ProviderAuthView, CookieTokenObtainPairView):
    pass


class UserSocialAuthAPIView(views.APIView):
    serializer_class = UserSocialAuthSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = User.objects.get(pk=request.user.id)

        queryset = UserSocialAuth.objects.filter(user=user)
        serializer = UserSocialAuthSerializer(instance=queryset, many=True)

        return Response(serializer.data, status.HTTP_200_OK)


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
