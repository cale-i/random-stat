from datetime import timedelta
from django.utils import timezone
from .models import LoginRecord
from .models import FailedLoginAttempt


def get_user_agent(request) -> str:
    return request.META.get('HTTP_USER_AGENT', '<unknown>')[:255]


def get_ip_address(request) -> str:
    # IP addressを取得
    # reverse proxyを経由している場合､'REMOTE_ADDR'の値がreverse proxyのアドレスとなる
    forwarded_addresses = request.META.get('HTTP_X_FORWARDED_FOR')
    ip_address = forwarded_addresses.split(',')[0] \
        if forwarded_addresses  \
        else request.META.get('REMOTE_ADDR')
    return ip_address


def get_username(request) -> str:
    request_data = getattr(request, "data", request.POST)

    username = request_data.get('email', None) \
        if request_data.get('email', None) \
        else request_data.get('username', None)

    return username


def get_password(request) -> str:
    request_data = getattr(request, "data", request.POST)
    return request_data.get('password', None)


def get_http_accept(request) -> str:
    return request.META.get("HTTP_ACCEPT", "<unknown>")[:1025]


def get_path_info(request) -> str:
    return request.META.get('PATH_INFO', '<unknown>')[:255]


def get_record(user, request):
    '''User-Agentが一致する場合､同一セッションとみなす'''
    records = LoginRecord.objects.filter(
        user=user,
        logout_time__isnull=True,
        user_agent=request.headers.get('User-Agent'),
    )

    if not records:
        # 不明なエラー
        return

    return records.latest('pk')


def has_same_record(data: dict) -> bool:
    '''直近1秒以内の重複するレコードの存在を確認'''
    time_within_ms = 500
    attempt_time = timezone.now() - timedelta(milliseconds=time_within_ms)
    records = FailedLoginAttempt.objects.filter(
        attempt_time__gte=attempt_time, **data)
    print('\n\n\n\n')
    print(records)
    print('\n\n\n\n')
    return bool(records)
