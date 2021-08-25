from django.contrib.auth import user_logged_in, user_logged_out, user_login_failed
from .utils import get_user


def login_signal(request, response):
    # user objectを取得
    user_obj = get_user(
        access_token=response.data.get('access')
    )
    user_logged_in.send(sender=user_obj.__class__,
                        request=request, user=user_obj)

    return


def logout_signal(request, response):
    user_obj = get_user(
        access_token=response.data.get('access')
    )
    user_logged_out.send(sender=user_obj.__class__,
                         request=request, user=user_obj)
    return


def failed_login_signal(request):
    user_login_failed.send(
        sender=__name__, credentials=None, request=request)
