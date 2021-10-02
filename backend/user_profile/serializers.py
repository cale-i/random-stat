from rest_framework import serializers
from .models import UserProfile
from django.contrib.auth import get_user_model

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('image', 'social_image_url')
