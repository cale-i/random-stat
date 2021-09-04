from django.contrib.auth import get_user_model
from djoser.compat import get_user_email_field_name
from djoser.conf import settings
from rest_framework import serializers

User = get_user_model()


class UserFunctionsMixin:
    # djoser.serializers.UserFunctionsMixin
    def get_user(self, is_active=True):
        try:
            user = User._default_manager.get(
                is_active=is_active,
                **{self.email_field: self.data.get(self.email_field, "")},
            )
            # if user.has_usable_password():
            return user
        except User.DoesNotExist:
            pass
        if (
            settings.PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND or settings.USERNAME_RESET_SHOW_EMAIL_NOT_FOUND
        ):
            self.fail("email_not_found")


class SendEmailResetSerializer(serializers.Serializer, UserFunctionsMixin):
    default_error_messages = {
        "email_not_found": settings.CONSTANTS.messages.EMAIL_NOT_FOUND
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.email_field = get_user_email_field_name(User)
        self.fields[self.email_field] = serializers.EmailField()
