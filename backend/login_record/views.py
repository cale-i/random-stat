
from django.contrib.auth import get_user_model
from rest_framework import status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import (
    user_logged_in,
    user_logged_out,
)

User = get_user_model()


class LoginRecorderAPIView(views.APIView):
    '''ログイン時に呼び出し､user_logged_in signalを経由してログイン情報の記録を行う'''

    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user

        # user_logged_out signalsの発火
        # 有効期限切れTokenのログアウト情報を記録するために呼び出す
        user_logged_out.send(sender=user.__class__,
                             request=request, user=user)

        # user_logged_in signalsの発火
        user_logged_in.send(sender=user.__class__,
                            request=request, user=user)

        return Response(status.HTTP_204_NO_CONTENT)


class LogoutRecorderAPIView(views.APIView):
    '''ログアウト時に呼び出し､user_logged_out signalを経由してログイン情報の記録を行う'''

    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        user_logged_out.send(sender=user.__class__,
                             request=request, user=user)

        return Response(status.HTTP_204_NO_CONTENT)
