from django.conf import settings
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.utils import timezone


User = get_user_model()

initialization_interval = 12


def get_guest_credentials():
    return {'email': settings.GUEST_EMAIL,
            'password': settings.GUEST_PASSWORD
            }


def initialize_guest_data():
    # 一定時間経過でユーザー名, アバターイメージ初期化
    # 不適切なユーザー名･画像を定期的に削除することが目的
    user = User.objects.get(email=settings.GUEST_EMAIL)
    refresh_time = user.date_joined + timedelta(hours=initialization_interval)

    # アカウント作成から一定時間経過していた場合初期化
    if refresh_time <= timezone.now():
        initialize_username(user)
        initialize_avatar(user)


def initialize_username(user):
    # ユーザー名の初期化
    user.username = user.email
    user.save()


def initialize_avatar(user):
    # アバターの初期化
    from user_profile.models import UserProfile

    if UserProfile.objects.filter(user=user):
        # アバターが登録されている場合
        user_profile = UserProfile.objects.get(user=user.id)
        user_profile.image = None
        user_profile.save()