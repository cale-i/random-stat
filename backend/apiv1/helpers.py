
from estat.models import (
    Category,
    StatsCode,
    SubCategory,
)
import random

from apiv1.serializers import AreaSerializer


def get_random_data(stats_code_id=''):
    params = {
        'stats_code': stats_code_id,
        'sub_category': [],
        'area': '',
    }

    #  get random prefix(stat_name_id + gov_org_id + title_id)
    if stats_code_id:
        stats_code_queryset = StatsCode.objects.get(
            id=stats_code_id)
    else:
        stats_code_queryset = random.choice(StatsCode.objects.all())
        stats_code_id = stats_code_queryset.id
        params['stats_code'] = stats_code_id

    # get category allay
    category_queryset = Category.objects.filter(
        stats_code_id__id__icontains=stats_code_id)
    # category_queryset = stats_code_queryset.category_set.all()

    for cat_id in category_queryset:
        sub_category_queryset = random.choice(SubCategory.objects.filter(
            category_id__id__icontains=cat_id.id))
        params['sub_category'].append(sub_category_queryset.id)

    # for category in category_queryset:
    #     sub_category_queryset = random.choice(
    #         category.subcategory_set.all())
    #     params['sub_category'].append(sub_category_queryset.id)

    # get random area
    area_queryset = random.choice(
        stats_code_queryset.area_set.all())
    # area_queryset = random.choice(
    #     Area.objects.all())

    params['area'] = area_queryset.id
    print('\n\n\n\n\n\n')
    print(params)
    print('\n\n\n\n\n\n')
    return params


def get_area_list(stats_code):
    # areaデータのリスト
    stats_code_queryset = StatsCode.objects.get(id=stats_code)
    area_queryset = stats_code_queryset.area_set.all()

    serializer = AreaSerializer(
        instance=area_queryset,
        many=True
    )
    return serializer.data


def make_category_list(category):
    # category-sub_category のリスト
    # 抽出したcategoryを受け取り、サブカテゴリと結合して出力
    # 引数categoryはOrdered Dictでの入力を想定

    ret = []
    for cat in category:
        queryset = SubCategory.objects.filter(
            category_id__id__icontains=cat['id']
        )

        sub_category_list = [
            {
                'id': q.id,
                'name': q.name,
            }
            for q in queryset
        ]
        ret.append({
            'id': cat['id'],
            'name': cat['name'],
            'sub_category_list': sub_category_list,
        })
    return ret


def get_stats_id_list():
    # 登録されているすべてのstats codeを返す
    queryset = StatsCode.objects.all()

    res = [
        {
            'id': q.id,
            'name': q.table_name,
        } for q in queryset]

    return res
