import re
import datetime
import uuid
import psycopg2
from settings import DSN
import os
import json


import argparse

# e-Stat APIを使用し、統計データを取得する

# TODO
# 統計表情報を取得

# 統計表情報の統計コードに基づき、個別統計データを取得

# 取得した個別統計データを加工してDBに格納(テストでは、csv形式で保存)


def read_file(arg):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    name = f'{arg}'
    file_name = os.path.join(base_dir, 'data', name)
    with open(file_name, 'r', encoding='utf-8') as f:
        return json.load(f)


def write_json(name, data):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    name = f'{name}.json'
    file_name = os.path.join(base_dir, 'output', name)
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def get_title_code(json_data):
    """各タイトル名とコードを取得"""

    items = json_data['GET_STATS_LIST']['DATALIST_INF']['TABLE_INF']
    res = {}
    population = {}
    for item in items:
        res[item['TITLE']['@no']
            ] = res.get(item['TITLE']['@no'], []) + [item['TITLE']['$']]
        population[item['TITLE']['@no']
                   ] = population.get(item['TITLE']['@no'], []) + [item['@id']]
    return res, population
    base_dir = os.path.dirname(os.path.abspath(__file__))


class InsertData():

    def __init__(self, file_name):

        self.dsn = DSN
        self.connection = psycopg2.connect(self.dsn)
        self.cursor = self.connection.cursor()

        self.read_file(file_name)

    def read_file(self, arg):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        name = f'{arg}'
        file_name = os.path.join(base_dir, 'data', name)
        with open(file_name, 'r', encoding='utf-8') as f:
            self.json_data = json.load(f)

    def select(self, tbl):
        query = f"SELECT * FROM {tbl}"

        self.cursor.execute(query)
        return self.cursor.fetchall()

    def insert_into(self, tbl, col, values):

        # check existence
        ph = []
        for c in col:
            ph.append(f"{c}=%s")
        ph = ' AND '.join(ph)
        query = f"SELECT COUNT('id') FROM {tbl} WHERE {ph}"

        self.cursor.execute(query, values)
        cnt = self.cursor.fetchone()
        if cnt[0]:
            # DBに存在している場合はなにもしない
            print(f"{query}は存在します")
            return

        # insertion
        col = ','.join(col)
        ph = ', '.join(['%s'] * len(values))
        query = f"INSERT INTO {tbl} ({col}) VALUES({ph})"

        try:
            self.cursor.execute(query, values)
            print(f'{query} :{values}: をコミットしました｡')
        except Exception as e:
            print(e)
            print(f'{query} :{values}: は実行されませんでした｡')
        finally:
            self.connection.commit()

    def format_date(self, e):
        """受け取ったe['@name'] を元に yyyymmdd形式にフォーマットしたデータを返す関数"""

        # 和暦の場
        jp_calendar = {
            '大正': 1911,
            '昭和': 1925,
            '平成': 1988,
            '令和': 2018,
        }
        if any([key in e['@name'] for key in jp_calendar.keys()]):
            mo = re.search(
                r'(大正|昭和|平成|令和)(\d{1,2})年((\d{1,2})月)?((\d{1,2})日)?',
                e['@name']
            )

            year = str(int(mo.group(2)) +
                       int(jp_calendar[mo.group(1)]))
            month = mo.group(4) if mo.group(4) else '00'
            day = mo.group(6) if mo.group(6) else '00'

            values = [
                e['@code'],
                f"{year}{month}{day}",
            ]

        # 西暦の場合
        else:
            mo = re.search(
                r'()(\d{4})年((\d{1,2})月)?((\d{1,2})日)?',
                e['@name'],
            )
            year = str(int(mo.group(2)))
            month = mo.group(4) if mo.group(4) else '00'
            day = mo.group(6) if mo.group(6) else '00'

            values = [
                e['@code'],
                f"{year}{month}{day}",
            ]

        return values

    def insert_into_area(self, class_el, class_obj_id):
        table_name = class_obj_id
        columns = [
            'id',
            'name',
        ]
        values = [
            class_el['@code'],
            class_el['@name'],
        ]
        # area をDBにINSERT
        self.insert_into(
            tbl=table_name,
            col=columns,
            values=values,
        )

    def insert_into_area_stats_code(self, class_el, statscode):
        table_name = 'area_stats_code'
        # stats_data と area の交差テーブルに INSERT
        col = [
            'statscode_id',
            'area_id',
        ]

        values = [
            statscode,
            class_el['@code'],
        ]
        self.insert_into(
            tbl=table_name,
            col=col,
            values=values,
        )

    def insert_into_time(self, class_el, class_obj_id):

        table_name = class_obj_id
        columns = [
            'id',
            'date',
        ]
        # @name を元に yyyymmdd形式にフォーマット

        values = self.format_date(class_el)

        # time をDBにINSERT
        self.insert_into(
            tbl=table_name,
            col=columns,
            values=values,
        )

    def insert_into_sub_category(self, class_el, class_prefix):
        table_name = 'sub_category'
        columns = [
            'id',
            'category_id',
            'name',
            'unit',
        ]
        values = [
            f"{class_prefix}_{class_el['@code']}",
            class_prefix,
            class_el['@name'],
            class_el.get('@unit', None),
        ]

        self.insert_into(
            tbl=table_name,
            col=columns,
            values=values
        )

    def insert_data(self):
        # init db
        connection = psycopg2.connect(DSN)
        cursor = connection.cursor()
        # 統計コード
        # STATS_CODE_ID = self.json_data['GET_STATS_DATA']['STATISTICAL_DATA']['TABLE_INF']['@id']

        STAT_NAME = {
            'table': 'stat_name',
            'id': self.json_data['GET_STATS_DATA']['STATISTICAL_DATA']['TABLE_INF']['STAT_NAME']['@code'],
            'name': self.json_data['GET_STATS_DATA']['STATISTICAL_DATA']['TABLE_INF']['STAT_NAME']['$']
        }
        GOV_ORG = {
            'table': 'gov_org',
            'id': self.json_data['GET_STATS_DATA']['STATISTICAL_DATA']['TABLE_INF']['GOV_ORG']['@code'],
            'name': self.json_data['GET_STATS_DATA']['STATISTICAL_DATA']['TABLE_INF']['GOV_ORG']['$']
        }
        TITLE = {
            'table': 'title',
            'id': str(self.json_data['GET_STATS_DATA']['STATISTICAL_DATA']['TABLE_INF']['TITLE']['@no']).zfill(3),
            'name': self.json_data['GET_STATS_DATA']['STATISTICAL_DATA']['TABLE_INF']['TITLE']['$']
        }
        # CATEGORY_PREFIX = f"{STAT_NAME['id']}_{GOV_ORG['id']}_{TITLE['id']}"
        CATEGORY_PREFIX = self.json_data[
            'GET_STATS_DATA']['STATISTICAL_DATA']['TABLE_INF']['@id']

        # マスタ作成
        # stat_name, gov_org, title
        for el in [STAT_NAME, GOV_ORG, TITLE]:

            self.insert_into(
                tbl=el['table'],
                col=['id', 'name'],
                values=[
                    el['id'],
                    el['name']
                ]
            )

        # stats_code

        self.insert_into(
            tbl='stats_code',
            col=[
                'id',
                'stat_name_id',
                'gov_org_id',
                'title_id',
                'statistics_name',
                'table_name',
                'explanation',
            ],
            values=[
                CATEGORY_PREFIX,
                STAT_NAME['id'],
                GOV_ORG['id'],
                TITLE['id'],
                self.json_data['GET_STATS_DATA']['STATISTICAL_DATA']['TABLE_INF']['STATISTICS_NAME'],
                self.json_data['GET_STATS_DATA']['STATISTICAL_DATA']['TABLE_INF']['TITLE_SPEC']['TABLE_NAME'],
                self.json_data['GET_STATS_DATA']['STATISTICAL_DATA']['TABLE_INF']['TITLE_SPEC']['TABLE_EXPLANATION'],
            ]
        )

        # category, area, time
        for class_obj in self.json_data['GET_STATS_DATA']['STATISTICAL_DATA']['CLASS_INF']['CLASS_OBJ']:

            class_obj_id = class_obj['@id']
            class_prefix = f"{CATEGORY_PREFIX}_{class_obj_id}"

            # areaの場合
            if class_obj_id == 'area':

                if type(class_obj['CLASS']) == dict:
                    # areaが一つしか存在しない場合(listでなくdictで入ってくる場合)
                    self.insert_into_area(
                        class_obj['CLASS'], class_obj_id)

                    self.insert_into_area_stats_code(
                        class_obj['CLASS'], CATEGORY_PREFIX)
                else:
                    for class_el in class_obj['CLASS']:
                        self.insert_into_area(class_el, class_obj_id)

                        self.insert_into_area_stats_code(
                            class_el, CATEGORY_PREFIX)

            # timeの場合
            elif class_obj_id == 'time':
                for class_el in class_obj['CLASS']:
                    self.insert_into_time(class_el, class_obj_id)

                # 上記以外の場合
            else:
                # categoryデータ
                table_name = 'category'
                category_id = class_prefix
                columns = [
                    'id',
                    'name',
                    'stats_code_id'
                ]
                values = [
                    category_id,
                    class_obj['@name'],
                    CATEGORY_PREFIX,
                ]
                self.insert_into(
                    tbl=table_name,
                    col=columns,
                    values=values
                )
                # stats_data_category 交差テーブルに INSERT
                exclude = {'@code': ['1120', '1240'],
                           '@name': ['人口性比', '労働力率']}
                for class_el in class_obj['CLASS']:
                    # 人口性比の場合を除外
                    if class_el['@code'] in exclude['@code'] and class_el['@name'] in exclude['@name']:
                        # if (class_el['@code'] == '1120' and class_el['@name'] == '人口性比') or (class_el['@code'] == '1240' and class_el['@name'] == '労働力率'):
                        continue

                    self.insert_into_sub_category(class_el, class_prefix)

        # 統計データ部
        for el in self.json_data['GET_STATS_DATA']['STATISTICAL_DATA']['DATA_INF']['VALUE']:

            # 各統計データ固有のIDを作成
            # 命名規則: STAT_DATA_ID + 各カテゴリの'key_value'を辞書順ソートして'_'で結合したもの('@unit', '$'を除く)
            is_invalid = False

            category_list = []
            exclude = {'@id': ['@tab'],
                       '@code': ['1120', '1240']}
            for key, value in el.items():
                # 日本語の入る'@unit'と数値である'$'を除く

                if key not in ['@unit', '$']:
                    # 人口性比 @tab: 1120を除外
                    if key in exclude['@id'] and value in exclude['@code']:
                        is_invalid = True
                        break

                    category_list.append(f"{key.replace('@', '')}_{value}")

            # 無効なデータの場合次のループ
            if is_invalid:
                continue

            ID_SUFFIX = '_'.join(sorted(category_list))
            STATS_DATA_ID = f"{CATEGORY_PREFIX}_{ID_SUFFIX}"

            # STATS_DATA テーブルにINSERT
            self.insert_into(
                tbl='stats_data',
                col=[
                    'id',
                    'area_id',
                    'time_id',
                    'stats_code_id',
                    'unit',
                    'value',
                ],
                values=[
                    STATS_DATA_ID,
                    el['@area'],
                    el['@time'],
                    CATEGORY_PREFIX,
                    el.get('@unit', None),
                    el['$'] if el['$'].isdecimal() else "0",
                    # int(el['$']) if el['$'].isdecimal() else 0,
                ]
            )
            # stats_data と category の交差テーブルに INSERT
            for key, value in el.items():
                if key not in ['@unit', '$', '@area', '@time']:
                    # category_idを生成
                    category_id = f"{CATEGORY_PREFIX}_{key.replace('@', '')}"
                    # sub_category_idを生成
                    sub_category_id = f"{category_id}_{value}"
                    self.insert_into(
                        tbl='stats_data_category',
                        col=[
                            'statsdata_id',
                            'category_id',
                        ],
                        values=[
                            STATS_DATA_ID,
                            category_id,
                        ]
                    )
                    self.insert_into(
                        tbl='stats_data_sub_category',
                        col=[
                            'statsdata_id',
                            'subcategory_id',
                        ],
                        values=[
                            STATS_DATA_ID,
                            sub_category_id,
                        ]
                    )

        # close db
        cursor.close()
        connection.close()
        # return data


def post_api():
    import requests
    url = 'http://localhost:8000/api/v1/test2/'
    data = {
        'category': [
            '00200521_00200_1_tab_020',
            # '00200521_00200_1_cat01_120'
        ],
        "area": "00000",
        # "area": "00200521_00200_1_area_00000",
        # 'time': '00200521_00200_1_time_1920000000'
    }
    res = requests.post(url, data)
    print(res)
    name = 'test'
    json_data = json.loads(res.content)
    write_json(name=name, data=json_data)
    # for el in json_data:
    #     [print(f"{key}:{value}") for key, value in el.items()]


def main():

    # parse arguments
    parser = argparse.ArgumentParser()
    # parser.add_argument("endpoint_url", type=str)
    subparsers = parser.add_subparsers(dest="command")

    sp1 = subparsers.add_parser("insert_data")
    # sp1.add_argument("num", type=int)

    sp2 = subparsers.add_parser("post_api")

    sp3 = subparsers.add_parser("get_title_code")

    sp4 = subparsers.add_parser("estat_api")

    args = parser.parse_args()
    # for test
    # args.command =
    if args.command == "insert_data":

        # file_name = '時系列人口推移0003410379.json'
        # file_name = '人口の労働力状態，就業者の産業・職業0003412175.json'

        file_name = [
            '時系列人口推移0003410379.json',
            '人口の労働力状態，就業者の産業・職業0003412175.json',
            '人口の労働力状態，就業者の産業・職業0003412176.json',
        ]

        for f in file_name:

            data = InsertData(f)
            data.insert_data()
            # post_many_haiku(args.endpoint_url, int(args.num))

    elif args.command == "post_api":
        post_api()

        # clear_database(args.endpoint_url)

    elif args.command == "get_title_code":
        json_data = read_file()
        res, pop = get_title_code(json_data)
        print(res)
        print(pop)


if __name__ == "__main__":
    main()
