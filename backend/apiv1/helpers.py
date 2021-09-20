
from estat.models import (
    Category,
    StatsCode,
    SubCategory,
    Area
)
import random

from apiv1.serializers import (
    AreaSerializer,
    StatsCodeSerializer,
)


def get_random_data(stats_code_id=None):

    stats_code_id = get_stats_code(stats_code_id)

    # stats_codeに紐付いたcategory内のsub_categoryからランダムで1つずつ取得
    sub_category = get_sub_category(stats_code_id)

    # stats_codeに紐付いたareaの中からランダムで1つ取得
    area = get_area(stats_code_id)

    return {
        'stats_code': stats_code_id,
        'sub_category': sub_category,
        'area': area,
    }


def get_stats_code(stats_code_id=None):
    return random.choice(StatsCode.objects.all()).id


def get_area(stats_code_id):
    return random.choice(Area.objects.filter(stats_code=stats_code_id)).id


def get_sub_category(stats_code_id):
    # stats_codeに紐付いたcategoryを取得
    category_queryset = Category.objects.filter(stats_code=stats_code_id)

    sub_category = []
    # categoryに紐付いたsub_categoryからランダムで1つ取得
    for category in category_queryset:
        sub_category.append(random.choice(SubCategory.objects.filter(
            category_id=category)).id)
    return sub_category


def get_response_data(params, serializer):
    serialized_data = serializer.data[0]

    return {
        'results': serializer.data,
        'unit': serialized_data['unit'],
        'table': {
            'id': serialized_data['stats_code']['id'],
            'name': serialized_data['stats_code']['table_name']
        },
        'area': serialized_data['area'],
        'sub_category': serialized_data['sub_category'],
        'area_list': get_area_list(params['stats_code']),
        'category_list': get_category_list(params['stats_code']),
        'stats_code_list': get_stats_code_list(),
    }


def get_area_list(stats_code):
    # areaデータのリスト
    serializer = AreaSerializer(
        instance=Area.objects.filter(stats_code=stats_code),
        many=True
    )
    return serializer.data


def get_category_list(stats_code):
    category_queryset = Category.objects.filter(
        stats_code=stats_code).values('id', 'name')
    category_list = []
    for category in category_queryset:
        data = {
            **category,
            'sub_category_list': SubCategory.objects.filter(category_id=category['id']).values('id', 'name')}
        category_list.append(data)
    return category_list


def get_stats_code_list():
    # 登録されているすべてのstats codeを返す
    serializer = StatsCodeSerializer(
        instance=StatsCode.objects.all(),
        many=True,
    )
    return serializer.data
