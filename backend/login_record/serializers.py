from .models import LoginRecord
from rest_framework import serializers


class RecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = LoginRecord
        fields = ['login_time', 'logout_time', 'ip_address', 'user_agent']
