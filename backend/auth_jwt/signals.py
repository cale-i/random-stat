from django.contrib.auth import user_logged_in, user_logged_out
from .utils import get_user


def login_signal(request, response):
    # user objectを取得
    user_obj = get_user(
        access_token=response.data.get('access')
    )
    print('\n\n\n\n\n\n\n')
    print('user: ', type(user_obj))
    print('\n\n\n\n\n\n\n')
    user_logged_in.send(sender=user_obj.__class__,
                        request=request, user=user_obj)

    return
