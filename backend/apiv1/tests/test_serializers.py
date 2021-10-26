from django.test import TestCase
from django.utils.timezone import localtime


from apiv1.serializers import (
    StatsCodeSerializer,
)

from apiv1.tests.factories.estat import (
    StatsCodeFactory,
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
