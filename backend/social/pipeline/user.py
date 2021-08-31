from django.contrib.auth import user_logged_in
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from user_profile.serializers import UserProfileSerializer
from user_profile.helpers import (
    save_user_profile,
    # exist_user_image,
)

UserModel = get_user_model()


def login_signal(strategy, user: UserModel = None, *args, **kwargs):
    """fire user_logged_in signal"""
    if not user:
        return
    request = strategy.request
    user_logged_in.send(sender=user.__class__,
                        request=request, user=user)


def create_user_profile(response, user=None, *args, **kwargs):
    # 取得したavatarからUserProfile.imageを作成する
    if not user:
        return

    data = {
        'social_image_url': response.get('picture', None)

    }
    serializer = UserProfileSerializer(data=data)

    try:
        serializer.is_valid(raise_exception=True)
        save_user_profile(
            user=user,
            social_image_url=serializer.validated_data.get('social_image_url')
        )
    except ValidationError as e:
        raise ValidationError(str(e))

    return
