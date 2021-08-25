from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginRecord(models.Model):
    '''ユーザーログイン履歴'''

    class Meta:
        db_table = 'login_record'
        ordering = ['-id']

    user = models.ForeignKey(
        User,
        verbose_name='ユーザー',
        on_delete=models.CASCADE,
    )
    login_time = models.DateTimeField(
        verbose_name='ログイン時刻',
        blank=True,
        null=True,
        auto_now_add=True,
    )
    refresh_time = models.DateTimeField(
        verbose_name='リフレッシュトークン発行時刻',
        blank=True,
        null=True,
    )
    logout_time = models.DateTimeField(
        verbose_name='ログアウト時刻',
        blank=True,
        null=True,
    )
    ip_address = models.GenericIPAddressField(
        verbose_name='接続元IPアドレス',
        null=True,
        db_index=True
    )
    user_agent = models.CharField(
        verbose_name='User-Agent',
        max_length=255,
        db_index=True
    )

    def __str__(self):
        login_dt = timezone.localtime(self.login_time)

        return f'{self.user.username} - {login_dt.year}/{login_dt.month}/{login_dt.day} {login_dt.hour}:{login_dt.minute}:{login_dt.second} - {self.get_diff_time()}'

    def get_diff_time(self):
        '''ログアウト時刻 - ログイン時刻'''
        if self.logout_time:
            time_diff = self.logout_time - self.login_time
            hour = time_diff.seconds // 3600
            minute = time_diff.seconds // 60 % 60
            return f'{hour}時間{minute}分'
        else:
            return '現在利用中のセッション'


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
