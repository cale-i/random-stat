
from estat.models import (
    Category,
    StatsCode,
    SubCategory,
    Area
)
import random


def get_random_data(stats_code_id=None):

    stats_code = get_stats_code(stats_code_id)
    stats_code_id = stats_code['id']

    # stats_codeに紐付いたcategory内のsub_categoryからランダムで1つずつ取得
    sub_category = get_sub_category(stats_code_id)

    # stats_codeに紐付いたareaの中からランダムで1つ取得
    area = get_area(stats_code_id)

    params = {
        'stats_code': stats_code_id,
        'sub_category': [e['id'] for e in sub_category],
        'area': area['id'],
    }
    meta = {
        'stats_code': stats_code,
        'sub_category': sub_category,
        'area': area
    }

    return params, meta


def get_meta_data(data):

    return {
        'stats_code': get_stats_code(data['stats_code']),
        'sub_category': get_sub_category_by_ids(data['sub_category']),
        'area': get_area_by_id(data['area']),
    }


def get_stats_code(stats_code_id=None):
    if not stats_code_id:
        return random.choice(StatsCode.objects.all().values('id', 'table_name_alias'))

    try:
        return StatsCode.objects.all().values('id', 'table_name_alias').get(id=stats_code_id)
    except StatsCode.DoesNotExist:
        raise StatsCode.DoesNotExist


def get_area(stats_code_id):
    return random.choice(Area.objects.filter(stats_code=stats_code_id).values('id', 'name'))


def get_sub_category(stats_code_id):
    # stats_codeに紐付いたcategoryを取得
    category_queryset = Category.objects.filter(stats_code=stats_code_id)
    sub_category = []
    # categoryに紐付いたsub_categoryからランダムで1つ取得
    for category in category_queryset:
        queryset = random.choice(SubCategory.objects.filter(
            category_id=category).values('id', 'name', 'category'))
        sub_category.append(queryset)

    return sub_category


def get_sub_category_by_ids(sub_category_ids):
    sub_category = []
    for sub_category_id in sub_category_ids:
        queryset = SubCategory.objects.all().values(
            'id', 'name', 'category').get(pk=sub_category_id)
        sub_category.append(queryset)
    return sub_category


def get_area_by_id(area_id):
    return Area.objects.all().values('id', 'name').get(pk=area_id)


def get_response_data(meta, serializer):
    # unit = serializer.data[0]
    unit = '人'

    return {
        'results': serializer.data,
        'unit': unit,
        **meta,
    }
