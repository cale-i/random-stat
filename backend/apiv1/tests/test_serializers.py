from django.test import TestCase
from django.utils.timezone import localtime


from apiv1.serializers import (
    StatsCodeSerializer,
)


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


class TestStatsCodeSerializer(TestCase):
    """
    StatsCodeSerializerのテストクラス
    """

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
