from estat.models import (
    StatsCode,
)
from rest_framework.test import APITestCase


class TestStatsCodeListView(APITestCase):
    # """StatsCodeListViewのテストクラス"""
    fixtures = ['apiv1/fixtures/test_stats_code.json']
    TARGET_URL = '/api/v1/timeseries/statscode/'

    def test_get_success(self):
        """モデル取得APIへのPOSTリクエスト(正常系)"""
        """レスポンスデータに関する異常系のテストはTestStatsCodeSerializerで検証する"""

        response = self.client.get(
            self.TARGET_URL,
            format='json')

        expected_json_list = [{
            'id': stats_code.id,
            'table_name_alias': stats_code.table_name_alias,
            'explanation': stats_code.explanation,
        } for stats_code in StatsCode.objects.all()]

        # レスポンスの内容を検証
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_json_list)
