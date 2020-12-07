from rest_framework import generics, views

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

from .serializers import (
    StatNameSerializer,
    GovOrgSerializer,
    TitleSerializer,
    StatsCodeSerializer,
    CategorySerializer,
    AreaSerializer,
    TimeSerializer,
    StatsDataSerializer,
)


class ChronologicalListAPIView(generics.ListAPIView):

    # query = StatsData.objects.all()
    queryset = StatsData.objects.all() \
        .select_related('area') \
        .select_related('time') \
        .select_related('stats_code') \
        .prefetch_related('category') \
        .select_related('stats_code__stat_name') \
        .select_related('stats_code__gov_org') \
        .select_related('stats_code__title')

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
