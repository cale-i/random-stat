from django.conf import settings
from django.contrib.auth import get_user_model, user_logged_in, user_logged_out
from django.db import models
from django.dispatch import receiver
from django.utils import timezone
User = get_user_model()


class LoginRecord(models.Model):
    '''ユーザーログイン履歴'''

    class Meta:
        db_table = 'login_record'

    user = models.ForeignKey(
        User,
        verbose_name='ユーザー',
        on_delete=models.CASCADE,
    )
    login_time = models.DateTimeField(
        verbose_name='ログイン時刻',
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
        blank=False,
        null=False,
        # unpack_ipv4=True
    )
    device_type = models.CharField(
        verbose_name='接続デバイス(PC, Android, iPhone, or blank',
        max_length=7,
        blank=True,
        null=True,
    )
    web_browser = models.CharField(
        verbose_name='接続ブラウザ(Chrome, Firefox, Safari, etc)',
        max_length=10,
        blank=True,
        null=True,
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


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    '''ログイン時に呼ばれる関数'''
    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    print('meta: ', request.META)
    print('HTTP_USER_AGENT : ', request.META.get('HTTP_USER_AGENT'))
    print('---------------------------------------------------------------')
    print('headers', request.headers)
    print('User-Agent', request.headers.get('User-Agent'))
    print(request.META.get('HTTP_X_FORWARDED_FOR'))

    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')

    # IP addressを取得
    # reverse proxyを経由している場合､'REMOTE_ADDR'の値がreverse proxyのアドレスとなる
    forwarded_addresses = request.META.get('HTTP_X_FORWARDED_FOR')
    ip_address = forwarded_addresses.split(',')[0] \
        if forwarded_addresses  \
        else request.META.get('REMOTE_ADDR')

    LoginRecord.objects.create(
        user=user,
        login_time=timezone.now(),
        ip_address=ip_address,
    )


@ receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    '''ログアウト時に呼ばれる関数'''

    # ログインから30分以上経過している場合はlogin_time + 30分がlogout_time
    # そうでない場合は､現在時刻

    records = LoginRecord.objects.filter(user=user, logout_time__isnull=True)

    if not records:
        # 不明なエラー
        return

    # logout_timeが存在しないすべてのオブジェクトを埋める
    for record in records:

        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        print('ログアウト処理')
        login_time = record.login_time
        life_time = settings.SIMPLE_JWT.get('ACCESS_TOKEN_LIFETIME')
        now_time = timezone.now()

        expiration_time = login_time + life_time

        # 有効期限切れならTrue
        is_expired = now_time > expiration_time
        record.logout_time = expiration_time \
            if is_expired \
            else now_time

        record.save()
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
