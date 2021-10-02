from .serializers import RecordSerializer, GuestRecordSerializer
from django.conf import settings


def is_guest_user(user):
    return user.email == settings.GUEST_EMAIL


def get_serializer(instance, user):
    # ゲストユーザーの場合､ダミーのIPアドレスを返す
    # 専用のserializerで対応
    if is_guest_user(user):
        return GuestRecordSerializer(instance, many=True)
    else:
        return RecordSerializer(instance, many=True)
