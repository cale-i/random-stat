from estat.models import (
    StatsCode,
    Area,
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


class TestAreaListView(APITestCase):
    # """StatsCodeListViewのテストクラス"""
    fixtures = ['apiv1/fixtures/test_area.json']
    TARGET_URL = '/api/v1/timeseries/area/'

    def test_get_success(self):
        """モデル取得APIへのGETリクエスト(正常系)"""
        params = {'stats_code': '0003410379'}

        response = self.client.get(
            self.TARGET_URL,
            params,
            format='json')

        expected_json_list = [{
            'id': area.id,
            'name': area.name,
        } for area in Area.objects.filter(stats_code=params['stats_code'])]

        # レスポンスの内容を検証
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_json_list)

    def test_get_bad_request_if_no_params(self):
        """
        モデル取得APIへのGETリクエスト(異常系)
        stats_codeを指定していない場合
        """
        response = self.client.get(
            self.TARGET_URL,
            format='json')

        expected_json_list = []

        # レスポンスの内容を検証
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_json_list)

    def test_get_bad_request_if_invalid_params(self):
        """
        モデル取得APIへのGETリクエスト(異常系)
        存在しないstats_codeを指定した場合
        """
        params = {'stats_code': '1234567890'}

        response = self.client.get(
            self.TARGET_URL,
            params,
            format='json')

        expected_json_list = [{
            'id': area.id,
            'name': area.name,
        } for area in Area.objects.filter(stats_code=params['stats_code'])]

        # レスポンスの内容を検証
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_json_list)

