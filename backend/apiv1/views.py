import datetime


from django_filters import rest_framework as filters
from estat.models import StatsData
from rest_framework import generics, status, views
from rest_framework.response import Response

from apiv1.serializers import StatsDataSerializer
from apiv1.stat_hist import (
    persist_stat_history,
    get_stat_history,
)
from .helpers import (
    get_random_data,
    get_response_data,
    get_meta_data,
)

stats_data_queryset = StatsData.objects.all() \
    .select_related('area') \
    .select_related('time') \
    .select_related('stats_code') \
    .prefetch_related('category') \
    .prefetch_related('sub_category') \
    .prefetch_related('sub_category__category') \
    .order_by('time')


class TimeSeriesFilter(filters.FilterSet):

    area = filters.CharFilter(field_name='area__id', method='get_area')
    # time = filters.CharFilter(field_name='time__id', method='get_time')

    sub_category = filters.CharFilter(
        field_name='sub_category__id',
        method='get_sub_category'
    )

    stats_code = filters.CharFilter(
        field_name='stats_code__id', method='get_stats_code')

    def get_area(self, queryset, name, value):
        return queryset.filter(**{name: value})

    # def get_time(self, queryset, name, value):
    #     return queryset.filter(**{name: value})

    def get_sub_category(self, queryset, name, value):
        return self.separate_params(queryset, name, value)

    def get_stats_code(self, queryset, name, value):
        return queryset.filter(**{name: value})

    def separate_params(self, queryset, name, value):

        # listで送られたvalueが勝手にstrに変換されるためlistに変換
        if type(value) is str:
            table = str.maketrans('', '', '[] \'')
            value = value.translate(table).split(',')
            qs = queryset
            for val in value:
                qs = qs.filter(**{name: val})
            return qs


class TimeSeriesAPIView(views.APIView):

    def get(self, request, *args, **kwargs):
        start = datetime.datetime.now()
        print(f'start: {start}')

        # 存在しないパターンの組み合わせの場合、もう一度取得する
        # time_out = 0
        # while True:
        grd_start = datetime.datetime.now()
        print(f'get_random_data starts: {grd_start}',)
        params, meta = get_random_data()

        grd_end = datetime.datetime.now()
        print(f'get_random_data ends: {grd_end}')
        print(f'time: {grd_end-grd_start}')

        # params = {
        #     'sub_category': [
        #         '00200521_00200_001_tab_020',
        #         '00200521_00200_001_cat01_100'
        #     ],
        #     'area': '00000'
        # }

        filterset = TimeSeriesFilter(
            params,
            queryset=stats_data_queryset
        )

        # if filterset.qs:
        #     break

        # time_out += 1

        # if time_out > 5:
        #     break

        serializer = StatsDataSerializer(instance=filterset.qs, many=True)

        data = get_response_data(meta, serializer)
        end = datetime.datetime.now()
        persist_stat_history(user=request.user, params=params)
        print(f'end: {end}')
        print(f'time: {end-start}')

        return Response(data, status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        # 検索用
        print(request.data)

        meta = get_meta_data(request.data)
        filterset = TimeSeriesFilter(
            request.data, queryset=stats_data_queryset)

        serializer = StatsDataSerializer(instance=filterset.qs, many=True)
        data = get_response_data(meta, serializer)
        persist_stat_history(user=request.user, params=request.data)

        return Response(data, status.HTTP_200_OK)


class StatsCodeAPIView(views.APIView):
    def post(self, request, *args, **kwargs):

        # 検索用
        print(request.data)
        params, meta = get_random_data(request.data['stats_code'])

        filterset = TimeSeriesFilter(params, queryset=stats_data_queryset)

        serializer = StatsDataSerializer(instance=filterset.qs, many=True)
        data = get_response_data(meta, serializer)

        persist_stat_history(user=request.user, params=params)
        return Response(data, status.HTTP_200_OK)


class StatHistoryView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        page_size = 1

        # userで履歴をフィルター
        params, page_data = get_stat_history(
            request,
            page_size=page_size,
        )

        # 登録直後等､履歴が存在しない場合終了
        if not params:
            return Response(status.HTTP_204_NO_CONTENT)

        meta = get_meta_data(params)
        # 履歴から統計表を作成
        filterset = TimeSeriesFilter(params, queryset=stats_data_queryset)
        serializer = StatsDataSerializer(instance=filterset.qs, many=True)
        data = {
            **get_response_data(meta, serializer),
            **page_data
        }

        return Response(data, status.HTTP_200_OK)
