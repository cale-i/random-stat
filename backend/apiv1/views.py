from django_filters import rest_framework as filters
from rest_framework.response import Response
from rest_framework import (
    generics,
    views,
    status
)

import random

from example.models import Book
from .serializers import BookSerializer

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

from apiv1.serializers import (
    StatNameSerializer,
    GovOrgSerializer,
    TitleSerializer,
    StatsCodeSerializer,
    CategorySerializer,
    SubCategorySerializer,
    AreaSerializer,
    TimeSerializer,
    StatsDataSerializer,
)


class ChronologicalFilter(filters.FilterSet):
    # time = filters.CharFilter(field_name='time__id', method='get_time')
    area = filters.CharFilter(field_name='area__id', method='get_area')
    time = filters.CharFilter(field_name='time__id', method='get_time')
    # time = filters.CharFilter(field_name='time__id', method='get_time')

    sub_category = filters.CharFilter(
        field_name='sub_category__id',
        method='get_sub_category'
    )

    def get_area(self, queryset, name, value):
        return queryset.filter(**{name: value})

    def get_time(self, queryset, name, value):
        return queryset.filter(**{name: value})

    def get_sub_category(self, queryset, name, value):
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
            return qs


class ChronologicalAPIView(views.APIView):
    def get(self, request, *args, **kwargs):
        data = {
            'results': [],
            'unit': {},
            'table_name': {},
            'sub_category': {},
            'area': {},
        }

        queryset = StatsData.objects.all() \
            .select_related('area') \
            .select_related('time') \
            .select_related('stats_code') \
            .select_related('stats_code__stat_name') \
            .select_related('stats_code__gov_org') \
            .select_related('stats_code__title') \
            .prefetch_related('category') \
            .prefetch_related('category__stats_code') \
            .prefetch_related('sub_category') \
            .prefetch_related('sub_category__category')

        # 存在しないパターンの組み合わせの場合、もう一度取得する
        queryset_length = 0
        time_out = 0
        while not queryset_length:

            params = self.get_random_data()
            # params = {
            #     'sub_category': [
            #         '00200521_00200_001_tab_020',
            #         '00200521_00200_001_cat01_100'
            #     ],
            #     'area': '00000'
            # }

            filterset = ChronologicalFilter(
                params,
                queryset=queryset
            )
            queryset_length = len(filterset.qs)
            print(queryset_length)

            time_out += 1

            if time_out > 5:
                break

        serializer = StatsDataSerializer(instance=filterset.qs, many=True)
        data['results'] = serializer.data
        # print(serializer.data[0]['stats_code']['table_name'])
        # print(serializer.data[0]['area'])
        data['table_name'] = serializer.data[0]['stats_code']['table_name']
        data['area'] = serializer.data[0]['area']
        data['unit'] = serializer.data[0]['unit']
        data['sub_category'] = serializer.data[0]['sub_category']
        data['category'] = serializer.data[0]['category']

        return Response(data, status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        queryset = StatsData.objects.all() \
            .select_related('area') \
            .select_related('time') \
            .select_related('stats_code') \
            .prefetch_related('category') \
            .select_related('stats_code__stat_name') \
            .select_related('stats_code__gov_org') \
            .select_related('stats_code__title')

        # 検索用
        filterset = ChronologicalFilter(request.data, queryset=queryset)

        serializer = StatsDataSerializer(instance=filterset.qs, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    def get_area_list(self):
        pass

    def get_category_list(self):
        pass

    def get_random_data(self):

        params = {
            'sub_category': [],
            'area': '',
        }

        #  get random prefix(stat_name_id + gov_org_id + title_id)
        stats_code_queryset = random.choice(StatsCode.objects.all())
        stats_code_id = stats_code_queryset.id

        # get category allay
        category_queryset = Category.objects.filter(
            stats_code_id__id__icontains=stats_code_id)

        for cat_id in category_queryset:
            sub_category_queryset = random.choice(SubCategory.objects.filter(
                category_id__id__icontains=cat_id.id))
            params['sub_category'].append(sub_category_queryset.id)

        # get random area
        area_queryset = random.choice(
            Area.objects.all())

        params['area'] = area_queryset.id
        print(params)
        return params


class ChronologicalListAPIView(generics.ListAPIView):

    # def get(self, request, *args, **kwargs):
    # queryset = StatsData.objects.filter(time__id__iexact='00200521_00200_1_time_1920000000') \
    queryset = StatsData.objects.all() \
        .select_related('area') \
        .select_related('time') \
        .select_related('stats_code') \
        .prefetch_related('category') \
        .select_related('stats_code__stat_name') \
        .select_related('stats_code__gov_org') \
        .select_related('stats_code__title')

    filter_class = ChronologicalFilter
    serializer_class = StatsDataSerializer


class BookListAPIView(generics.ListAPIView):
    """本モデルの一覧取得APIクラス"""

    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookRetrieveAPIView(generics.RetrieveAPIView):
    """本モデルの詳細取得APIクラス"""

    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookCreateAPIView(generics.CreateAPIView):
    """本モデルの登録APIクラス"""

    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookUpdateAPIView(generics.UpdateAPIView):
    """本モデルの更新・一部更新APIクラス"""

    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDestroyAPIView(generics.DestroyAPIView):
    """本モデルの削除APIクラス"""

    queryset = Book.objects.all()
