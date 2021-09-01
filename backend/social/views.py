from djoser.social.views import ProviderAuthView
from auth_jwt.views import CookieTokenObtainPairView
from django.contrib.auth import get_user_model
from rest_framework import status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from social_django.models import UserSocialAuth

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
        # serializer = UserSocialAuthSerializer(instance=queryset, many=True)
        serializer = UserSocialAuthSerializer(instance=queryset, many=True)

        return Response(serializer.data, status.HTTP_200_OK)
