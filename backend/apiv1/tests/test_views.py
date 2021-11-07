from django.contrib.auth import get_user_model
from estat.models import (
    StatsCode,
    Area,
    Category,
)
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


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


class TestCategoryListView(APITestCase):
    # """CategoryListViewのテストクラス"""
    fixtures = ['apiv1/fixtures/test_category.json']
    TARGET_URL = '/api/v1/timeseries/category/'

    def test_get_success(self):
        """モデル取得APIへのGETリクエスト(正常系)"""
        params = {'stats_code': '0003410379'}

        response = self.client.get(
            self.TARGET_URL,
            params,
            format='json')

        # レスポンスの内容を検証
        self.assertEqual(response.status_code, 200)

    def test_get_bad_request_if_no_params(self):
        """
        モデル取得APIへのGETリクエスト(異常系)
        stats_codeを指定していない場合
        """
        response = self.client.get(
            self.TARGET_URL,
            format='json')

        # レスポンスの内容を検証
        self.assertEqual(response.status_code, 400)

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

        expected_json_list = []

        # レスポンスの内容を検証
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_json_list)


class TestFavoritesView(APITestCase):
    # """FavoritesViewのテストクラス"""
    TARGET_URL = '/api/v1/timeseries/favorites/'

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = get_user_model().objects.create_user(
            username='user',
            email='example1@example.com',
            password='password',
        )

    def test_get_success_when_no_record_exist(self):
        """モデル取得APIへのGETリクエスト 登録件数が0の場合 (正常系)"""
        token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        params = {'page': 1}

        response = self.client.get(
            self.TARGET_URL,
            params,
            format='json')

        expected_json_dict = {
            'current': params['page'],
            'count': 0
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_json_dict)

    def test_get_success(self):
        """モデル取得APIへのGETリクエスト(正常系)"""
        token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        params = {'page': 1}

        response = self.client.get(
            self.TARGET_URL,
            params,
            format='json')

        expected_json_dict = {
            'current': params['page'],
            'count': 0
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_json_dict)

    def test_get_not_authenticated(self):
        """未ログインGET(異常系)"""
        response = self.client.get(
            self.TARGET_URL,
            format='json')
        self.assertEqual(response.status_code, 401)

    def test_post_not_authenticated(self):
        """未ログインPOST(異常系)"""
        response = self.client.post(
            self.TARGET_URL,
            format='json')
        self.assertEqual(response.status_code, 401)

    def test_delete_not_authenticated(self):
        """未ログインDELETE(異常系)"""
        response = self.client.delete(
            self.TARGET_URL,
            format='json')
        self.assertEqual(response.status_code, 401)

    def test_delete_bad_request(self):
        token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        response = self.client.delete(
            self.TARGET_URL,
            format='json')

        self.assertEqual(response.status_code, 400)
