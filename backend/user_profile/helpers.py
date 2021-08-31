from .models import UserProfile
from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage
import os

User = get_user_model()


def exist_user_image(user_id: int):
    '''
    user_idに紐付いたimageを返す｡
    user_idに紐付いたUserProfileが存在しない場合､及び
    user_idに紐付いたUserProfileが存在するが､imageがNoneの場合は
    Noneを返す
    '''
    queryset = UserProfile.objects.filter(pk=user_id)
    if not queryset:
        return False

    user_profile = queryset.get(pk=user_id)

    return bool(user_profile.image)


def save_user_profile(
        user_id: int = None,
        user: User = None,
        image=None,
        social_image_url: str = None):
    '''
        user_idとimageを渡して保存し､UserProfileオブジェクトを返す
        '''
    if not (user or user_id):
        # userもuser_idも渡されない場合
        raise ValueError

    if user is None:
        user = User.objects.get(pk=user_id)

    defaults = {'user': user, }
    if image:
        defaults['image'] = image

    if social_image_url:
        defaults['social_image_url'] = social_image_url

    user_profile, created = UserProfile.objects.update_or_create(
        user=user,
        defaults=defaults,
    )
    return user_profile


def get_default_image():
    '''
    S3からデフォルトのアバターイメージのURLを取得する関数
    デフォルトのアバターイメージが存在しない場合空文字を返す
    '''

    FILE_DIR = 'avatar'
    FILE_NAME = 'default-avatar.jpg'
    FILE_PATH = os.path.join(FILE_DIR, FILE_NAME)

    if (default_storage.exists(FILE_PATH) is False):
        return ''

    return default_storage.url(FILE_PATH)
