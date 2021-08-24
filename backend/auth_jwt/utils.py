from rest_framework_simplejwt.state import token_backend
from django.contrib.auth import get_user_model
from login_record.models import LoginRecord
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
    record.refresh_time = timezone.now()
    record.save()
