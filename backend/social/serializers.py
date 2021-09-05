from django.contrib.auth import get_user_model
from rest_framework import serializers
from social_core import exceptions
from social_django.models import UserSocialAuth
from social_django.utils import load_backend, load_strategy

User = get_user_model()


class UserSocialAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSocialAuth
        fields = ['provider', ]


class CustomProviderAuthSerializer(serializers.Serializer):
    '''djoser.social.serializerから拝借'''

    def create(self, validated_data):
        return {}

    def validate(self, attrs):
        request = self.context["request"]
        if "state" in request.GET:
            self._validate_state(request.GET["state"])

        strategy = load_strategy(request)
        redirect_uri = strategy.session_get("redirect_uri")

        backend_name = self.context["view"].kwargs["provider"]
        backend = load_backend(strategy, backend_name,
                               redirect_uri=redirect_uri)
        user = request.user

        try:
            user = backend.auth_complete(user=user)
        except exceptions.AuthException as e:
            raise serializers.ValidationError(str(e))
        return {"user": user}

    def _validate_state(self, value):
        request = self.context["request"]
        strategy = load_strategy(request)
        redirect_uri = strategy.session_get("redirect_uri")

        backend_name = self.context["view"].kwargs["provider"]
        backend = load_backend(strategy, backend_name,
                               redirect_uri=redirect_uri)

        try:
            backend.validate_state()
        except exceptions.AuthMissingParameter:
            raise serializers.ValidationError(
                "State could not be found in request data."
            )
        except exceptions.AuthStateMissing:
            raise serializers.ValidationError(
                "State could not be found in server-side session data."
            )
        except exceptions.AuthStateForbidden:
            raise serializers.ValidationError(
                "Invalid state has been provided.")

        return value
