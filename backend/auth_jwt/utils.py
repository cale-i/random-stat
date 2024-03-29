from rest_framework_simplejwt.state import token_backend
from django.contrib.auth import get_user_model
from login_attempt.models import LoginRecord
from login_attempt.serializers import LoginRecordSerializer
from rest_framework.exceptions import ValidationError

from django.utils import timezone


User = get_user_model()


def get_user(access_token):
    decoded_token = token_backend.decode(token=access_token, verify=True)
    return User.objects.get(pk=decoded_token['user_id'])


def update_refresh_time(access_token):
    '''
    /auth/jwt/refresh/リクエスト時(refresh token 再発行時)に呼ばれる関数
    現在時刻をrefresh_timeに上書きする
    '''
    records = LoginRecord.objects.filter(
        user=get_user(access_token=access_token),
        logout_time__isnull=True
    )

    if not records:
        # 不明なエラー
        return

    record = records.latest('pk')

    data = {
        'refresh_time': timezone.now()

    }
    serializer = LoginRecordSerializer(
        instance=record, data=data, partial=True)

    try:
        serializer.is_valid(raise_exception=True)
        serializer.save()
    except ValidationError as e:
        raise ValidationError(e.args[0])


def has_valid_password(access_token: str) -> bool:
    '''有効なパスワードが設定されているかを判別'''
    user = get_user(access_token)
    if hasattr(user, 'has_usable_password'):
        valid_password = user.has_usable_password()
    else:
        valid_password = True
    return valid_password
