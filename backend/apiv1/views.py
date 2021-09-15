import datetime
import random

from django_filters import rest_framework as filters
from estat.models import (Area, Category, GovOrg, StatName, StatsCode,
                          StatsData, SubCategory, Time, Title)
from rest_framework import generics, serializers, status, views
from rest_framework.response import Response

from apiv1.serializers import (AreaSerializer, CategorySerializer,
                               GovOrgSerializer, StatNameSerializer,
                               StatsCodeSerializer, StatsDataSerializer,
                               SubCategorySerializer, TimeSerializer,
                               TitleSerializer)
from apiv1.stat_hist import (
    persist_stat_history,
)


class TimeSeriesFilter(filters.FilterSet):

    # time = filters.CharFilter(field_name='time__id', method='get_time')
    area = filters.CharFilter(field_name='area__id', method='get_area')
    time = filters.CharFilter(field_name='time__id', method='get_time')
    # time = filters.CharFilter(field_name='time__id', method='get_time')

    sub_category = filters.CharFilter(
        field_name='sub_category__id',
        method='get_sub_category'
    )

    stats_code = filters.CharFilter(
        field_name='stats_code__id', method='get_stats_code')

    def get_area(self, queryset, name, value):
        return queryset.filter(**{name: value})

    def get_time(self, queryset, name, value):
        return queryset.filter(**{name: value})

    def get_sub_category(self, queryset, name, value):
        return self.separate_params(queryset, name, value)

    def get_stats_code(self, queryset, name, value):
        return self.separate_params(queryset, name, value)

    # def get_random_data(self, queryset, name, value)

    # def add_prefix(self, queryset, name, value):
    #     prefix = name
    #     return prefix

    def separate_params(self, queryset, name, value):

        # listで送られたvalueが勝手にstrに変換されるためlistに変換
        if type(value) is str:
            table = str.maketrans('', '', '[] \'')
            value = value.translate(table).split(',')
            # print(name)
            # print(value)
            # print({name: value})
            qs = queryset
            for val in value:
                qs = qs.filter(**{name: val})
                # print(qs.query)
                print(len(qs))
                # print(qs)
            # print(qs)
            return qs


class TimeSeriesAPIView(views.APIView):
    def __init__(self):
        self.queryset = StatsData.objects.all() \
            .select_related('area') \
            .select_related('time') \
            .select_related('stats_code') \
            .select_related('stats_code__stat_name') \
            .select_related('stats_code__gov_org') \
            .select_related('stats_code__title') \
            .prefetch_related('category') \
            .prefetch_related('category__stats_code') \
            .prefetch_related('sub_category') \
            .prefetch_related('sub_category__category') \
            .prefetch_related('area__stats_code') \
            .order_by('time')

    def get(self, request, *args, **kwargs):
        start = datetime.datetime.now()
        print(f'start: {start}')

        # 存在しないパターンの組み合わせの場合、もう一度取得する
        time_out = 0
        while True:

            params = self.get_random_data()
            # params = {
            #     'sub_category': [
            #         '00200521_00200_001_tab_020',
            #         '00200521_00200_001_cat01_100'
            #     ],
            #     'area': '00000'
            # }

            filterset = TimeSeriesFilter(
                params,
                queryset=self.queryset
            )

            if filterset.qs:
                break

            time_out += 1

            if time_out > 5:
                break

        serializer = StatsDataSerializer(instance=filterset.qs, many=True)
        table = {
            'id': serializer.data[0]['stats_code']['id'],
            'name': serializer.data[0]['stats_code']['table_name']
        }

        data = {
            'results': serializer.data,
            'unit': serializer.data[0]['unit'],
            # 'table_name': serializer.data[0]['stats_code']['table_name'],
            'table': table,
            'area': serializer.data[0]['area'],
            'sub_category': serializer.data[0]['sub_category'],
            'area_list': self.get_area_list(table['id']),
            'category_list': self.make_category_list(
                category=serializer.data[0]['category']),
            'stats_code_list': self.get_stats_id_list(),
        }

        end = datetime.datetime.now()
        persist_stat_history(user=request.user, params=params)
        print(f'end: {end}')
        print(f'time: {end-start}')

        return Response(data, status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        # 検索用
        print(request.data)

        filterset = TimeSeriesFilter(request.data, queryset=self.queryset)

        serializer = StatsDataSerializer(instance=filterset.qs, many=True)
        table = {
            'id': serializer.data[0]['stats_code']['id'],
            'name': serializer.data[0]['stats_code']['table_name']
        }
        data = {
            'results': serializer.data,
            'unit': serializer.data[0]['unit'],
            # 'table_name': serializer.data[0]['stats_code']['table_name'],
            'table': table,
            'area': serializer.data[0]['area'],
            'sub_category': serializer.data[0]['sub_category'],
            'area_list': self.get_area_list(table['id']),
            'category_list': self.make_category_list(
                category=serializer.data[0]['category']),
            'stats_code_list': self.get_stats_id_list(),
        }
        persist_stat_history(user=request.user, params=request.data)

        return Response(data, status.HTTP_200_OK)

    def get_area_list(self, stats_code):
        # areaデータのリスト
        stats_code_queryset = StatsCode.objects.get(id=stats_code)
        area_queryset = stats_code_queryset.area_set.all()

        serializer = AreaSerializer(
            instance=area_queryset,
            many=True
        )
        return serializer.data

    def make_category_list(self, category):
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
        # print(ret)
        return ret

    def get_random_data(self):

        params = {
            'sub_category': [],
            'area': '',
        }

        # stats code
        stats_code_list = StatsCode.objects.all()
        stats_code_queryset = random.choice(stats_code_list)
        stats_code_id = stats_code_queryset.id
        params['stats_code'] = stats_code_id

        # get category allay
        category_queryset = Category.objects.filter(
            stats_code_id__id__icontains=stats_code_id)
        # category_queryset = stats_code_queryset.category_set.all()

        category_list = []
        for cat_id in category_queryset:
            category_list.append(cat_id)
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
        area_id = area_queryset.id
        params['area'] = area_id

        return params

    # get_stats_id_list 登録されているすべてのstats codeを返す
    def get_stats_id_list(self):
        queryset = StatsCode.objects.all()

        res = [
            {
                'id': q.id,
                'name': q.table_name,
            } for q in queryset]

        return res


class StatsCodeAPIView(TimeSeriesAPIView):
    def get(self):
        return Response(None, status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):

        # 検索用
        print(request.data)
        params = self.get_random_data(request.data['stats_code_id'])

        filterset = TimeSeriesFilter(params, queryset=self.queryset)

        serializer = StatsDataSerializer(instance=filterset.qs, many=True)
        table = {
            'id': serializer.data[0]['stats_code']['id'],
            'name': serializer.data[0]['stats_code']['table_name']
        }
        data = {
            'results': serializer.data,
            'unit': serializer.data[0]['unit'],
            # 'table_name': serializer.data[0]['stats_code']['table_name'],
            'table': table,
            'area': serializer.data[0]['area'],
            'sub_category': serializer.data[0]['sub_category'],
            'area_list': self.get_area_list(table['id']),
            'category_list': self.make_category_list(
                category=serializer.data[0]['category']),
            'stats_code_list': self.get_stats_id_list(),
        }

        persist_stat_history(user=request.user, params=params)
        return Response(data, status.HTTP_200_OK)

    def get_random_data(self, stats_code_id=''):
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
        return params
