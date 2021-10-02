from estat.models import (
    StatsCode,
    Area,
    Time,
    StatsData,
    StatHistory,
)
from rest_framework import serializers


class StatsCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = StatsCode
        fields = ['id', 'table_name', 'explanation']


class AreaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Area
        fields = ['id', 'name']


class TimeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Time
        fields = ['date']


class StatsDataSerializer(serializers.ModelSerializer):
    time = TimeSerializer()

    class Meta:
        model = StatsData
        fields = ['time', 'value']


class StatHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = StatHistory
        fields = ['stats_code', 'area', 'sub_category', 'user']
