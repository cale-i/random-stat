from django.conf import settings
from rest_framework import status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import LoginRecord
from .serializers import RecordSerializer, GuestRecordSerializer


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
