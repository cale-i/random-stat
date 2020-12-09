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
    AreaSerializer,
    TimeSerializer,
    StatsDataSerializer,
)


class ChronologicalFilter(filters.FilterSet):
    # time = filters.CharFilter(field_name='time__id', method='get_time')
    area = filters.CharFilter(field_name='area__id', method='get_area')
    time = filters.CharFilter(field_name='time__id', method='get_time')
    # time = filters.CharFilter(field_name='time__id', method='get_time')

    category = filters.CharFilter(
        field_name='category__id', method='get_category')

    def get_area(self, queryset, name, value):
        return queryset.filter(**{name: value})

    def get_time(self, queryset, name, value):
        return queryset.filter(**{name: value})

    def get_category(self, queryset, name, value):
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

            name = f'{name}__in'
            return queryset.filter(**{name: value})


class ChronologicalAPIView(views.APIView):

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
        # filterset = ChronologicalFilter(request.data, queryset=queryset)

        # ランダム用
        params = self.get_random_data()
        filterset = ChronologicalFilter(
            params, queryset=queryset)

        serializer = StatsDataSerializer(instance=filterset.qs, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    def get_random_data(self):

        params = {
            'category': [],
            'area': '',
        }

        #  get random prefix(stat_name_id + gov_org_id + title_id)
        stats_code_queryset = random.choice(StatsCode.objects.all())
        prefix = f"{stats_code_queryset.stat_name.id}_{stats_code_queryset.gov_org.id}_{stats_code_queryset.title.id}"

        # get random category
        category_queryset = random.choice(
            Category.objects.filter(id__icontains=prefix))

        params['category'] = category_queryset.id

        # get random area
        area_queryset = random.choice(
            Area.objects.filter(id__icontains=prefix))

        params['area'] = area_queryset.id

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
