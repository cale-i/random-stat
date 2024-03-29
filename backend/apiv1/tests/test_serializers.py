from apiv1.tests.factories.favorites import FavoritesFactory
from django.test import TestCase
from django.contrib.auth import get_user_model


from apiv1.serializers import (
    StatsCodeSerializer,
    AreaSerializer,
    TimeSerializer,
    FavoritesSerializer,
)

from apiv1.tests.factories.estat import (
    StatsCodeFactory,
    AreaFactory,
    TimeFactory,
)


class TestStatsCodeSerializer(TestCase):
    """
    StatsCodeSerializerのテストクラス
    """

    def test_output_data(self):
        """出力データの内容検証"""
        data = {
            'id': '0003410379',
            'table_name_alias': '総人口',
            'explanation': '1)　沖縄県は調査されなかったため，含まれていない。<br>2)　長野県西筑摩群山口村と岐阜県中津川市の境界紛争地域人口（男39人，女34人）は全国に含まれているが，長野県及び岐阜県のいずれにも含まれていない。',
        }
        # シリアライザを作成
        stats_code = StatsCodeFactory(**data)
        serializer = StatsCodeSerializer(instance=stats_code)

        # シリアライザの出力内容を検証
        expected_data = {
            'id': data['id'],
            'table_name_alias': data['table_name_alias'],
            'explanation': data['explanation'],
        }
        self.assertDictEqual(serializer.data, expected_data)


class TestAreaSerializer(TestCase):
    """
    AreaSerializerのテストクラス
    """

    def test_output_data(self):
        """出力データの内容検証"""

        data = {
            'id': 'wwww',
            'name': '全国',
        }
        # シリアライザを作成
        area = AreaFactory(**data)
        serializer = AreaSerializer(instance=area)

        # シリアライザの出力内容を検証
        expected_data = {
            'id': data['id'],
            'name': data['name'],
        }
        self.assertDictEqual(serializer.data, expected_data)


class TestTimeSerializer(TestCase):
    """
    TimeSerializerのテストクラス
    """

    def test_output_data(self):
        """出力データの内容検証"""

        data = {"date": "19500000"}
        # シリアライザを作成
        time = TimeFactory(**data)
        serializer = TimeSerializer(instance=time)

        # シリアライザの出力内容を検証
        expected_data = {
            'date': data['date'],
        }
        self.assertDictEqual(serializer.data, expected_data)


class TestFavoritesSerializer(TestCase):
    """
    FavoritesSerializerのテストクラス
    """

    @ classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = get_user_model().objects.create_user(
            username='user',
            email='example@example.com',
            password='password',
        )

    def test_output_data(self):
        """出力データの内容検証"""
        data = {
            'user': self.user,
        }

        # シリアライザを作成
        favorites = FavoritesFactory(**data)
        serializer = FavoritesSerializer(instance=favorites)

        # シリアライザの出力内容を検証
        expected_data = {
            'user': data['user'].id,
            'area': '00000',
            'sub_category': [],
            'stats_code': '0003412176',
        }
        self.assertDictEqual(serializer.data, expected_data)
