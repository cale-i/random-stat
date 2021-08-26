from django.conf import settings
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.utils import timezone
from user_profile.models import UserProfile
from user_profile.serializers import UserProfileSerializer
from rest_framework.exceptions import ValidationError


User = get_user_model()

guest_email = settings.GUEST_EMAIL
guest_password = settings.GUEST_PASSWORD
guest_default_username = 'ゲストユーザーのプロフィールは､定期的に初期化しています｡'
guest_default_avatar = None
initialization_interval = 6


def exist_guest_user() -> bool:
    return bool(User.objects.filter(email=guest_email))


def get_guest_credentials() -> dict:
    return {'email': guest_email,
            'password': guest_password
            }


def create_guest_user():
    if exist_guest_user():
        return None

    User.objects.create_user(
        last_login=timezone.now(),
        username=guest_default_username,
        **get_guest_credentials()
    )


def initialize_username(user: User):
    # ユーザー名の初期化
    user.username = guest_default_username
    user.save()


def initialize_avatar(user: User):
    # アバターの初期化

    if exist_user_profile(user):
        # UserProfile table にレコード存在しない場合処理なし
        return

    user_profile = UserProfile.objects.get(user=user.id)
    data = {
        'image': guest_default_avatar
    }
    serializer = UserProfileSerializer(instance=user_profile, data=data)

    try:
        serializer.is_valid(raise_exception=True)
        serializer.save()
    except ValidationError as e:
        raise ValidationError(e.args[0])


def exist_user_profile(user: User) -> bool:
    return bool(UserProfile.objects.filter(user=user))


def initialize_guest_data():
    '''
    ゲストユーザー未作成の場合はここで作成
    一定時間経過でユーザー名, アバターイメージ初期化
        不適切なユーザー名･画像を定期的に削除することが目的
    '''
    if exist_guest_user() is False:
        create_guest_user()

    user = User.objects.get(email=guest_email)
    # user.last_login is Nullable
    last_login = user.last_login or user.date_joined

    refresh_time = last_login + timedelta(hours=initialization_interval)

    # アカウント作成から一定時間経過していた場合初期化
    if refresh_time <= timezone.now():
        initialize_username(user)
        initialize_avatar(user)
