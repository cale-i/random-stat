from django.test import TestCase
from django.utils.timezone import localtime

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

from example.models import Book
from apiv1.serializers import BookSerializer


class TestStatNameSerializer(TestCase):
    """
    StatNameSerializerのテストクラス
    """

    def test_input_valid(self):
        """入力データのバリデーション(OK)"""

        # シリアライザを作成
        input_data = {
            'id': '00200521',
            'name': '国勢調査',
        }
        serializer = StatNameSerializer(data=input_data)

        # バリデーションの結果を検証
        self.assertEqual(serializer.is_valid(), True)

    def test_input_invalid_if_id_is_blank(self):
        """入力データのバリデーション(NG: idが空文字)"""

        # シリアライザを作成
        input_data = {
            'id': '',
            'name': '国勢調査',
        }
        serializer = StatNameSerializer(data=input_data)

        # バリデーションの結果を検証
        self.assertEqual(serializer.is_valid(), False)
        self.assertCountEqual(serializer.errors.keys(), ['id'])
        self.assertCountEqual(
            [e.code for e in serializer.errors['id']],
            ['blank'],
        )

    def test_input_invalid_if_name_is_blank(self):
        """入力データのバリデーション(NG: nameが空文字)"""

        # シリアライザを作成
        input_data = {
            'id': '00200521',
            'name': '',
        }
        serializer = StatNameSerializer(data=input_data)

        # バリデーションの結果を検証
        self.assertEqual(serializer.is_valid(), False)
        self.assertCountEqual(serializer.errors.keys(), ['name'])
        self.assertCountEqual(
            [e.code for e in serializer.errors['name']],
            ['blank'],
        )

    def test_output_data(self):
        """出力データの内容検証"""

        # シリアライザを作成
        stat_name = StatName.objects.create(
            id='00200521',
            name='国勢調査',
        )
        serializer = StatNameSerializer(instance=stat_name)

        # シリアライザの出力内容を検証
        expected_data = {
            'id': stat_name.id,
            'name': stat_name.name,
        }
        self.assertDictEqual(serializer.data, expected_data)


class TestGovOrgSerializer(TestCase):
    """
    GovOrgSerializerのテストクラス
    """

    def test_input_valid(self):
        """入力データのバリデーション(OK)"""

        # シリアライザを作成
        input_data = {
            'id': '00200',
            'name': '総務省',
        }
        serializer = GovOrgSerializer(data=input_data)

        # バリデーションの結果を検証
        self.assertEqual(serializer.is_valid(), True)

    def test_input_invalid_if_id_is_blank(self):
        """入力データのバリデーション(NG: idが空文字)"""

        # シリアライザを作成
        input_data = {
            'id': '',
            'name': '総務省',
        }
        serializer = GovOrgSerializer(data=input_data)

        # バリデーションの結果を検証
        self.assertEqual(serializer.is_valid(), False)
        self.assertCountEqual(serializer.errors.keys(), ['id'])
        self.assertCountEqual(
            [e.code for e in serializer.errors['id']],
            ['blank'],
        )

    def test_input_invalid_if_name_is_blank(self):
        """入力データのバリデーション(NG: nameが空文字)"""

        # シリアライザを作成
        input_data = {
            'id': '00200',
            'name': '',
        }
        serializer = GovOrgSerializer(data=input_data)

        # バリデーションの結果を検証
        self.assertEqual(serializer.is_valid(), False)
        self.assertCountEqual(serializer.errors.keys(), ['name'])
        self.assertCountEqual(
            [e.code for e in serializer.errors['name']],
            ['blank'],
        )

    def test_output_data(self):
        """出力データの内容検証"""

        # シリアライザを作成
        gov_org = GovOrg.objects.create(
            id='00200',
            name='総務省',
        )
        serializer = GovOrgSerializer(instance=gov_org)

        # シリアライザの出力内容を検証
        expected_data = {
            'id': gov_org.id,
            'name': gov_org.name,
        }
        self.assertDictEqual(serializer.data, expected_data)


class TestTitleSerializer(TestCase):
    """
    TitleSerializerのテストクラス
    """

    def test_input_valid(self):
        """入力データのバリデーション(OK)"""

        # シリアライザを作成
        input_data = {
            'id': '001',
            'name': '男女別人口及び人口性比－全国，都道府県（大正9年～平成27年）',
        }
        serializer = TitleSerializer(data=input_data)

        # バリデーションの結果を検証
        self.assertEqual(serializer.is_valid(), True)

    def test_input_invalid_if_id_is_blank(self):
        """入力データのバリデーション(NG: idが空文字)"""

        # シリアライザを作成
        input_data = {
            'id': '',
            'name': '男女別人口及び人口性比－全国，都道府県（大正9年～平成27年）',
        }
        serializer = TitleSerializer(data=input_data)

        # バリデーションの結果を検証
        self.assertEqual(serializer.is_valid(), False)
        self.assertCountEqual(serializer.errors.keys(), ['id'])
        self.assertCountEqual(
            [e.code for e in serializer.errors['id']],
            ['blank'],
        )

    def test_input_invalid_if_name_is_blank(self):
        """入力データのバリデーション(NG: nameが空文字)"""

        # シリアライザを作成
        input_data = {
            'id': '001',
            'name': '',
        }
        serializer = TitleSerializer(data=input_data)

        # バリデーションの結果を検証
        self.assertEqual(serializer.is_valid(), False)
        self.assertCountEqual(serializer.errors.keys(), ['name'])
        self.assertCountEqual(
            [e.code for e in serializer.errors['name']],
            ['blank'],
        )

    def test_output_data(self):
        """出力データの内容検証"""

        # シリアライザを作成
        title = Title.objects.create(
            id='001',
            name='男女別人口及び人口性比－全国，都道府県（大正9年～平成27年）',
        )
        serializer = TitleSerializer(instance=title)

        # シリアライザの出力内容を検証
        expected_data = {
            'id': title.id,
            'name': title.name,
        }
        self.assertDictEqual(serializer.data, expected_data)


class TestStatsCodeSerializer(TestCase):
    """
    StatsCodeSerializerのテストクラス
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.input_data = {
            'id': '00200521_00200_001',
            'statistics_name': '時系列データ 男女，年齢，配偶関係',
            'table_name': '男女別人口及び人口性比－全国，都道府県（大正9年～平成27年）',
            'explanation': ' 1)　沖縄県は調査されなかったため，含まれていない。<br>2)　長野県西筑摩群山口村と岐阜県中津川市の境界紛争地域人口（男39人，女34人）は全国に含まれているが，長野県及び岐阜県のいずれにも含まれていない。',
            'stat_name': {
                'id': '00200521',
                'name': '総務省',
            },
            'gov_org': {
                'id': '00200',
                'name': '国勢調査',
            },
            'title': {
                'id': '001',
                'name': '男女別人口及び人口性比－全国，都道府県（大正9年～平成27年）',
            },
        }

    def test_input_valid(self):
        """入力データのバリデーション(OK)"""

        # シリアライザを作成
        input_data = self.input_data.copy()
        serializer = StatsCodeSerializer(data=input_data)
        # バリデーションの結果を検証
        self.assertEqual(serializer.is_valid(), True)

    def test_input_invalid_if_id_is_blank(self):
        """入力データのバリデーション(NG: idが空文字)"""

        # シリアライザを作成
        input_data = self.input_data.copy()
        input_data['id'] = ''

        serializer = StatsCodeSerializer(data=input_data)

        # バリデーションの結果を検証
        self.assertEqual(serializer.is_valid(), False)
        self.assertCountEqual(serializer.errors.keys(), ['id'])
        self.assertCountEqual(
            [e.code for e in serializer.errors['id']],
            ['blank'],
        )

    def test_input_invalid_if_statistics_name_is_blank(self):
        """入力データのバリデーション(NG: statistics_nameが空文字)"""

        # シリアライザを作成
        input_data = self.input_data.copy()
        input_data['statistics_name'] = ''
        serializer = StatsCodeSerializer(data=input_data)

        # バリデーションの結果を検証
        self.assertEqual(serializer.is_valid(), False)
        self.assertCountEqual(serializer.errors.keys(), ['statistics_name'])
        self.assertCountEqual(
            [e.code for e in serializer.errors['statistics_name']],
            ['blank'],
        )
