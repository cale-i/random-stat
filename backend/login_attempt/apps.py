from django.apps import AppConfig


class LoginAttemptConfig(AppConfig):
    name = 'login_attempt'

    def ready(self):
        from login_attempt.signals import (
            user_logged_in_callback,
            user_logged_out_callback,
            user_login_failed_callback
        )
