from rest_framework_simplejwt.state import token_backend
from django.contrib.auth import get_user_model

User = get_user_model()


def get_user(access_token):
    decoded_token = token_backend.decode(token=access_token, verify=True)
    return User.objects.get(pk=decoded_token['user_id'])
