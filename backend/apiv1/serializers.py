from estat.models import (
    StatName,
    GovOrg,
    Title,
    StatsCode,
    Category,
    SubCategory,
    Area,
    Time,
    StatsData,
)
from rest_framework import serializers

from example.models import Book


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = '__all__'


class StatNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = StatName
        fields = '__all__'


class GovOrgSerializer(serializers.ModelSerializer):

    class Meta:
        model = GovOrg
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Title
        fields = '__all__'


class StatsCodeSerializer(serializers.ModelSerializer):
    stat_name = StatNameSerializer()
    gov_org = GovOrgSerializer()
    title = TitleSerializer()

    class Meta:
        model = StatsCode
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    stats_code = StatsCodeSerializer()

    class Meta:
        model = Category
        fields = '__all__'


class SubCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = SubCategory
        fields = '__all__'


class AreaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Area
        fields = '__all__'


class TimeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Time
        fields = '__all__'


class StatsDataSerializer(serializers.ModelSerializer):

    category = CategorySerializer(many=True)
    sub_category = SubCategorySerializer(many=True)
    area = AreaSerializer()
    time = TimeSerializer()
    stats_code = StatsCodeSerializer()

    class Meta:
        model = StatsData
        fields = '__all__'
