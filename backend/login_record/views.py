from django.conf import settings
from django.contrib.auth import get_user_model, user_logged_in, user_logged_out
from django.utils import timezone
from rest_framework import status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import LoginRecord
from .serializers import RecordSerializer, GuestRecordSerializer


User = get_user_model()


class LoginRecorderAPIView(views.APIView):
    '''ログイン時に呼び出し､user_logged_in signalを経由してログイン情報の記録を行う'''

    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user

        # 有効期限切れTokenのログアウト情報を記録するために呼び出す
        self.fill_expired_logout_time(user, request)

        # user_logged_in signalsの発火
        user_logged_in.send(sender=user.__class__,
                            request=request, user=user)

        return Response(status.HTTP_204_NO_CONTENT)

    def fill_expired_logout_time(self, user, reqest):
        records = LoginRecord.objects.filter(
            user=user, logout_time__isnull=True)

        if not records:
            # 不明なエラー
            return

        for record in records:
            login_time = record.login_time
            life_time = settings.SIMPLE_JWT.get('ACCESS_TOKEN_LIFETIME')
            now_time = timezone.now()

            expiration_time = login_time + life_time

            # 有効期限切れならTrue
            is_expired = now_time > expiration_time
            if is_expired:
                record.logout_time = expiration_time
                record.save()


class LogoutRecorderAPIView(views.APIView):
    '''ログアウト時に呼び出し､user_logged_out signalを経由してログイン情報の記録を行う'''

    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        user_logged_out.send(sender=user.__class__,
                             request=request, user=user)

        return Response(status.HTTP_204_NO_CONTENT)


class RecordAPIView(views.APIView):
    '''
    ユーザーに紐付いたログイン履歴を返す
    returnのフォーマット:[{},{},{}...]
    pagenationは行わず､最新10件のみを返す
    '''
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):

        user = request.user
        records = LoginRecord.objects.filter(user=user)[:10]
        serializer = get_serializer(instance=records, user=user)
        return Response(serializer.data, status.HTTP_200_OK)


def is_guest_user(user):
    return user.email == settings.GUEST_EMAIL


def get_serializer(instance, user):
    # ゲストユーザーの場合､ダミーのIPアドレスを返す
    # 専用のserializerで対応
    if is_guest_user(user):
        return GuestRecordSerializer(instance, many=True)
    else:
        return RecordSerializer(instance, many=True)
