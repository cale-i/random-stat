from django.contrib.auth import user_logged_in
from django.contrib.auth import get_user_model

UserModel = get_user_model()


def login_signal(strategy, user: UserModel = None, *args, **kwargs):
    """fire user_logged_in signal"""
    if not user:
        return
    request = strategy.request
    user_logged_in.send(sender=user.__class__,
                        request=request, user=user)
