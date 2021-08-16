from django.contrib.auth import get_user_model, user_login_failed
from django.db import models
from django.dispatch import receiver
User = get_user_model()


class FailedLoginAttempt(models.Model):
    '''ログイン失敗'''

    class Meta:
        db_table = 'failed_login_attempt'

    user_agent = models.CharField(
        verbose_name='User-Agent',
        max_length=255,
        db_index=True
    )
    ip_address = models.GenericIPAddressField(
        verbose_name='接続元IPアドレス',
        null=True,
        db_index=True
    )
    username = models.CharField(
        verbose_name="me", max_length=255, null=True, db_index=True)

    password = models.CharField(
        verbose_name="Username",
        max_length=255,
        null=True,
        db_index=True
    )
    http_accept = models.CharField(
        verbose_name=("HTTP Accept"), max_length=1025)
    path_info = models.CharField(verbose_name=("Path"), max_length=255)

    attempt_time = models.DateTimeField(
        verbose_name='Attempt Time',
        auto_now_add=True,
    )

    def __str__(self):
        return f"Attempted Access: {self.attempt_time}"


@ receiver(user_login_failed)
def user_login_failed_callback(sender, request, **kwargs):
    '''ログイン失敗時に呼ばれる関数'''

    FailedLoginAttempt.objects.create(
        user_agent=get_user_agent(request),
        ip_address=get_ip_address(request),
        username=get_username(request),
        password=get_password(request),
        http_accept=get_http_accept(request),
        path_info=get_path_info(request),
    )


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
