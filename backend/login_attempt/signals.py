from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth import get_user_model, user_logged_in, user_logged_out, user_login_failed
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from .serializers import LoginRecordSerializer, FailedLoginAttemptSerializer
from .helpers import (
    get_user_agent,
    get_ip_address,
    get_username,
    get_password,
    get_http_accept,
    get_path_info,
    get_record,
)

User = get_user_model()


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    '''ログイン時に呼ばれる関数'''

    # IP addressを取得
    # reverse proxyを経由している場合､'REMOTE_ADDR'の値がreverse proxyのアドレスとなる

    data = {
        'user': user.id,
        'ip_address': get_ip_address(request),
        'user_agent': get_user_agent(request),
    }

    serializer = LoginRecordSerializer(data=data)

    try:
        serializer.is_valid(raise_exception=True)
        serializer.save()
    except ValidationError as e:
        raise ValidationError(e.args[0])


@ receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    '''ログアウト時に呼ばれる関数'''

    record = get_record(user, request)
    if record is None:
        return

    base_time = record.refresh_time \
        if record.refresh_time \
        else record.login_time
    life_time = settings.SIMPLE_JWT.get('REFRESH_TOKEN_LIFETIME')
    now_time = timezone.now()
    expiration_time = base_time + life_time

    #  login(1)  refresh        exp(refresh+lifetime)
    #    ↓          ↓            ↓
    #    |----------|------------|------------ ~
    #                     ↑               ↑
    #                   login(2)       login(3)

    # login(2) => min(login(2), exp) => login(2)
    # login(3) => min(login(3), exp) => exp

    data = {
        'logout_time': min(expiration_time, now_time),
    }
    serializer = LoginRecordSerializer(
        instance=record, data=data, partial=True)

    try:
        serializer.is_valid(raise_exception=True)
        serializer.save()
    except ValidationError as e:
        raise ValidationError(e.args[0])


@ receiver(user_login_failed)
def user_login_failed_callback(sender, request, **kwargs):
    '''ログイン失敗時に呼ばれる関数'''

    data = {
        'user_agent': get_user_agent(request),
        'ip_address': get_ip_address(request),
        'username': get_username(request),
        'password': get_password(request),
        'http_accept': get_http_accept(request),
        'path_info': get_path_info(request),
    }

    serializer = FailedLoginAttemptSerializer(data=data)

    try:
        serializer.is_valid(raise_exception=True)
        serializer.save()
    except ValidationError as e:
        raise ValidationError(e.args[0])
