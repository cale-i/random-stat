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

    input_data = {
        'id': '00200521',
        'name': '国勢調査',
    }

    def test_input_valid(self):
        """入力データのバリデーション(OK)"""

        # シリアライザを作成
        input_data = self.input_data.copy().copy()
        serializer = StatNameSerializer(data=input_data)
        # バリデーションの結果を検証
        serializer.is_valid()
        self.assertEqual(serializer.is_valid(), True)

    def test_input_invalid_if_id_is_blank(self):
        """入力データのバリデーション(NG: idが空文字)"""

        # シリアライザを作成
        input_data = self.input_data.copy().copy()
        input_data['id'] = ''
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
        input_data = self.input_data.copy().copy()
        input_data['name'] = ''
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

    input_data = {
        'id': '00200',
        'name': '総務省',
    }

    def test_input_valid(self):
        """入力データのバリデーション(OK)"""

        # シリアライザを作成
        input_data = self.input_data.copy()
        serializer = GovOrgSerializer(data=input_data)

        # バリデーションの結果を検証
        self.assertEqual(serializer.is_valid(), True)

    def test_input_invalid_if_id_is_blank(self):
        """入力データのバリデーション(NG: idが空文字)"""

        # シリアライザを作成
        input_data = self.input_data.copy()

        input_data['id'] = ''
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
        input_data = self.input_data.copy()
        input_data['name'] = ''
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
        input_data = self.input_data.copy()

        # シリアライザを作成
        gov_org = GovOrg.objects.create(
            id=input_data['id'],
            name=input_data['name'],
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

    input_data = {
        'id': '001',
        'name': '男女別人口及び人口性比－全国，都道府県（大正9年～平成27年）',
    }

    def test_input_valid(self):
        """入力データのバリデーション(OK)"""

        # シリアライザを作成
        input_data = self.input_data.copy()
        serializer = TitleSerializer(data=input_data)

        # バリデーションの結果を検証
        self.assertEqual(serializer.is_valid(), True)

    def test_input_invalid_if_id_is_blank(self):
        """入力データのバリデーション(NG: idが空文字)"""

        # シリアライザを作成
        input_data = self.input_data.copy()
        input_data['id'] = ''
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
        input_data = self.input_data.copy()

        input_data['name'] = ''
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

        input_data = self.input_data.copy()
        # シリアライザを作成
        title = Title.objects.create(
            id=input_data['id'],
            name=input_data['name'],
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
    input_data = {
        'id': '00200521_00200_001',
        'statistics_name': '時系列データ 男女，年齢，配偶関係',
        'table_name': '男女別人口及び人口性比－全国，都道府県（大正9年～平成27年）',
        'explanation': ' 1)　沖縄県は調査されなかったため，含まれていない。<br>2)　長野県西筑摩群山口村と岐阜県中津川市の境界紛争地域人口（男39人，女34人）は全国に含まれているが，長野県及び岐阜県のいずれにも含まれていない。',
        'stat_name': TestStatNameSerializer.input_data.copy(),
        'gov_org': TestGovOrgSerializer.input_data.copy(),
        'title': TestTitleSerializer.input_data.copy(),
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


class TestCategorySerializer(TestCase):
    """
    CategorySerializerのテストクラス
    """
    input_data = {
        'id': '0020504_00200_001_tab',
        'name': '総数，男及び女_時系列',
        'stats_code': TestStatsCodeSerializer.input_data.copy()
    }

    def test_input_valid(self):
        """入力データのバリデーション(OK)"""

        # シリアライザを作成
        input_data = self.input_data.copy()
        serializer = CategorySerializer(data=input_data)

        # バリデーションの結果を検証
        serializer.is_valid()
        self.assertEqual(serializer.is_valid(), True)

    def test_input_invalid_if_id_is_blank(self):
        """入力データのバリデーション(NG: idが空文字)"""

        # シリアライザを作成
        input_data = self.input_data.copy()
        input_data['id'] = ''
        serializer = CategorySerializer(data=input_data)

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
        input_data = self.input_data.copy()
        input_data['name'] = ''
        serializer = CategorySerializer(data=input_data)

        # バリデーションの結果を検証
        self.assertEqual(serializer.is_valid(), False)
        self.assertCountEqual(serializer.errors.keys(), ['name'])
        self.assertCountEqual(
            [e.code for e in serializer.errors['name']],
            ['blank'],
        )


class TestSubCategorySerializer(TestCase):
    """
    SubCategorySerializerのテストクラス
    """

    input_data = {
        'id': '00200521_00200_001_tab_020',
        'name': '人口',
        'unit': '人',
        'category': TestCategorySerializer.input_data.copy(),
    }

    def test_input_valid(self):
        """入力データのバリデーション(OK)"""

        # シリアライザを作成
        input_data = self.input_data.copy()
        serializer = SubCategorySerializer(data=input_data)

        # バリデーションの結果を検証
        serializer.is_valid()
        self.assertEqual(serializer.is_valid(), True)

    def test_input_invalid_if_id_is_blank(self):
        """入力データのバリデーション(NG: idが空文字)"""

        # シリアライザを作成
        input_data = self.input_data.copy()
        input_data['id'] = ''
        serializer = SubCategorySerializer(data=input_data)

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
            input_data = self.input_data.copy()
            input_data['name'] = ''
            serializer = SubCategorySerializer(data=input_data)

            # バリデーションの結果を検証
            self.assertEqual(serializer.is_valid(), False)
            self.assertCountEqual(serializer.errors.keys(), ['name'])
            self.assertCountEqual(
                [e.code for e in serializer.errors['name']],
                ['blank'],
            )


class TestAreaSerializer(TestCase):
    """
    AreaSerializerのテストクラス
    """
    input_data = {
        'id': '00000',
        'name': '全国',
    }

    def test_input_valid(self):
        """入力データのバリデーション(OK)"""

        # シリアライザを作成
        input_data = self.input_data.copy()

        serializer = AreaSerializer(data=input_data)

        # バリデーションの結果を検証
        self.assertEqual(serializer.is_valid(), True)

    def test_input_invalid_if_id_is_blank(self):
        """入力データのバリデーション(NG: idが空文字)"""

        # シリアライザを作成
        input_data = self.input_data.copy()
        input_data['id'] = ''
        serializer = AreaSerializer(data=input_data)

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
        input_data = self.input_data.copy()
        input_data['name'] = ''
        serializer = AreaSerializer(data=input_data)

        # バリデーションの結果を検証
        self.assertEqual(serializer.is_valid(), False)
        self.assertCountEqual(serializer.errors.keys(), ['name'])
        self.assertCountEqual(
            [e.code for e in serializer.errors['name']],
            ['blank'],
        )

    def test_output_data(self):
        """出力データの内容検証"""
        input_data = self.input_data.copy()
        # オブジェクトを作成
        area = Area.objects.create(
            id=input_data['id'],
            name=input_data['name'],
        )
        serializer = AreaSerializer(instance=area)

        # シリアライザの出力内容を検証
        expected_data = {
            'id': area.id,
            'name': area.name,
        }
        self.assertDictEqual(serializer.data, expected_data)


class TestTimeSerializer(TestCase):
    """
    TimeSerializerのテストクラス
    """
    input_data = {
        'id': '2015000000',
        'date': '20150000',
    }

    def test_input_valid(self):
        """入力データのバリデーション(OK)"""

        # シリアライザを作成
        input_data = self.input_data.copy()

        serializer = TimeSerializer(data=input_data)

        # バリデーションの結果を検証
        self.assertEqual(serializer.is_valid(), True)

    def test_input_invalid_if_id_is_blank(self):
        """入力データのバリデーション(NG: idが空文字)"""

        # シリアライザを作成
        input_data = self.input_data.copy()
        input_data['id'] = ''
        serializer = TimeSerializer(data=input_data)

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
        input_data = self.input_data.copy()
        input_data['date'] = ''
        serializer = TimeSerializer(data=input_data)

        # バリデーションの結果を検証
        self.assertEqual(serializer.is_valid(), False)
        self.assertCountEqual(serializer.errors.keys(), ['date'])
        self.assertCountEqual(
            [e.code for e in serializer.errors['date']],
            ['blank'],
        )

    def test_output_data(self):
        """出力データの内容検証"""
        input_data = self.input_data.copy()
        # オブジェクトを作成
        time = Time.objects.create(
            id=input_data['id'],
            date=input_data['date'],
        )
        serializer = TimeSerializer(instance=time)

        # シリアライザの出力内容を検証
        expected_data = {
            'id': time.id,
            'date': time.date,
        }
        self.assertDictEqual(serializer.data, expected_data)


class TestStatsDataSerializer(TestCase):
    """
    StatsDataSerializerのテストクラス
    """
    input_data = {
        'id': '00200521_00200_001_area_00000_cat01_100_tab_020_time_2015000000',
        'unit': '人',
        'value': '127094745',
        'area': TestAreaSerializer.input_data.copy(),
        'time': TestTimeSerializer.input_data.copy(),
        'stats_code': TestStatsCodeSerializer.input_data.copy(),
        'category': [TestCategorySerializer.input_data.copy()],
        'sub_category': [TestSubCategorySerializer.input_data.copy()],
    }

    def test_input_valid(self):
        """入力データのバリデーション(OK)"""

        # シリアライザを作成
        input_data = self.input_data.copy()
        serializer = StatsDataSerializer(data=input_data)

        serializer.is_valid()
        # バリデーションの結果を検証
        self.assertEqual(serializer.is_valid(), True)

    # def test_input_invalid_if_id_is_blank(self):
    #     """入力データのバリデーション(NG: idが空文字)"""

    #     # シリアライザを作成
    #     input_data = self.input_data.copy()
    #     input_data['id'] = ''

    #     serializer = StatsDataSerializer(data=input_data)

    #     # バリデーションの結果を検証
    #     self.assertEqual(serializer.is_valid(), False)
    #     self.assertCountEqual(serializer.errors.keys(), ['id'])
    #     self.assertCountEqual(
    #         [e.code for e in serializer.errors['id']],
    #         ['blank'],
    #     )

    # def test_input_invalid_if_statistics_name_is_blank(self):
    #     """入力データのバリデーション(NG: statistics_nameが空文字)"""

    #     # シリアライザを作成
    #     input_data = self.input_data.copy()
    #     input_data['statistics_name'] = ''
    #     serializer = StatsDataSerializer(data=input_data)

    #     # バリデーションの結果を検証
    #     self.assertEqual(serializer.is_valid(), False)
    #     self.assertCountEqual(serializer.errors.keys(), ['statistics_name'])
    #     self.assertCountEqual(
    #         [e.code for e in serializer.errors['statistics_name']],
    #         ['blank'],
    #     )
