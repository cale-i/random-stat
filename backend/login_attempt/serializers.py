from .models import FailedLoginAttempt, LoginRecord
from rest_framework import serializers


class RecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = LoginRecord
        fields = ['login_time', 'logout_time', 'ip_address', 'user_agent']


class GuestRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = LoginRecord
        fields = ['login_time', 'logout_time', ]


class LoginRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = LoginRecord
        fields = '__all__'


class FailedLoginAttemptSerializer(serializers.ModelSerializer):

    class Meta:
        model = FailedLoginAttempt
        fields = '__all__'
