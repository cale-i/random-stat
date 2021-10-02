from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class StatName(models.Model):
    """
    政府統計名
    eg.'人口推移'

    """

    class Meta:
        db_table = 'stat_name'

    id = models.CharField(
        verbose_name='政府統計コード',
        primary_key=True,
        max_length=8
    )
    name = models.CharField(
        verbose_name='政府統計名',
        null=False, max_length=255
    )


class GovOrg(models.Model):
    """
    担当機関
    eg.'内務省'
    """

    class Meta:
        db_table = 'gov_org'

    id = models.CharField(
        verbose_name='担当機関コード',
        primary_key=True,
        max_length=5
    )
    name = models.CharField(
        verbose_name='担当機関名',
        null=False,
        max_length=255
    )


class Title(models.Model):
    """
    表題
    eg.'年齢（各歳），男女別人口及び人口性比－総人口，日本人人口'
    """

    class Meta:
        db_table = 'title'

    id = models.CharField(
        verbose_name='統計コード',
        primary_key=True,
        max_length=255
    )
    name = models.CharField(
        verbose_name='統計コード名',
        null=False,
        max_length=255
    )


class StatsCode(models.Model):
    """統計表 表ID"""

    class Meta:
        db_table = 'stats_code'

    id = models.CharField(
        verbose_name='統計表ID {stat_name}_{gov_ort}_{title.zfill(3)}',
        primary_key=True,
        max_length=18
    )
    stat_name = models.ForeignKey(
        StatName,
        verbose_name='政府統計コード',
        on_delete=models.PROTECT
    )
    gov_org = models.ForeignKey(
        GovOrg,
        verbose_name='担当機関コード',
        on_delete=models.PROTECT
    )
    title = models.ForeignKey(
        Title,
        verbose_name='表題コード',
        on_delete=models.PROTECT
    )
    statistics_name = models.CharField(
        verbose_name='提供分類1',
        null=False,
        max_length=255
    )
    table_name = models.CharField(
        verbose_name='テーブル名',
        null=False,
        max_length=255
    )
    explanation = models.CharField(
        verbose_name='説明',
        null=False,
        max_length=255
    )


class Category(models.Model):
    """
    カテゴリ
    eg. '0020504_00200_001_cat1'
        '0020504_00200_001_tab'
    @cat1: {
        @code: '000',
        name: '男女計'
    }
    """

    class Meta:
        db_table = 'category'

    id = models.CharField(
        verbose_name='カテゴリコード',
        primary_key=True,
        max_length=25
    )
    stats_code = models.ForeignKey(
        StatsCode,
        verbose_name='統計表 表ID',
        on_delete=models.PROTECT,
    )
    name = models.CharField(
        verbose_name='カテゴリ名',
        null=False,
        max_length=255
    )
    # unit = models.CharField(
    #     verbose_name='表示単位',
    #     null=True,
    #     max_length=255
    # )


class SubCategory(models.Model):
    """
    サブカテゴリ
    @cat1: {
        @code: '000',
        name: '男女計'
    }
    """

    class Meta:
        db_table = 'sub_category'

    id = models.CharField(
        verbose_name='サブカテゴリコード',
        primary_key=True,
        max_length=255
    )
    category = models.ForeignKey(
        Category,
        verbose_name='カテゴリ',
        on_delete=models.PROTECT,
    )
    name = models.CharField(
        verbose_name='サブカテゴリ名',
        null=False,
        max_length=255
    )
    unit = models.CharField(
        verbose_name='表示単位',
        null=True,
        max_length=255
    )


class Area(models.Model):
    """
    統計データエリア
    id: 00000 - 47000
    eg.'全国', ... '沖縄県'
    """

    class Meta:
        db_table = 'area'

    id = models.CharField(
        verbose_name='地域コード', primary_key=True,
        max_length=5
    )

    name = models.CharField(
        verbose_name='地域名',
        null=False,
        max_length=255
    )
    stats_code = models.ManyToManyField(
        StatsCode,
        verbose_name='統計表 表ID',

    )


class Time(models.Model):
    """
    統計データ年度
    id: @code(max_length=10)
    date: 8桁の西暦表示(yyyymmdd)
    """

    class Meta:
        db_table = 'time'

    id = models.CharField(
        verbose_name='年度コード',
        primary_key=True,
        max_length=10
    )
    date = models.CharField(
        verbose_name='date',
        null=False,
        max_length=8
    )


class StatsData(models.Model):
    """
    統計データ
    """

    class Meta:
        db_table = 'stats_data'

    id = models.CharField(
        verbose_name='ID',
        primary_key=True,
        max_length=255
    )
    category = models.ManyToManyField(
        Category,
        verbose_name='カテゴリコード'
    )
    sub_category = models.ManyToManyField(
        SubCategory,
        verbose_name='サブカテゴリコード'
    )
    area = models.ForeignKey(
        Area,
        verbose_name='地域コード',
        on_delete=models.PROTECT
    )
    time = models.ForeignKey(
        Time,
        verbose_name='年度コード',
        on_delete=models.PROTECT

    )
    stats_code = models.ForeignKey(
        StatsCode,
        verbose_name='統計表 表ID',
        on_delete=models.PROTECT

    )
    unit = models.CharField(
        verbose_name='単位コード',
        null=True,
        max_length=10
    )
    value = models.CharField(
        verbose_name='統計データ数値',
        null=True,
        max_length=255
    )


class StatHistory(models.Model):
    """
    統計表示履歴
    """

    class Meta:
        db_table = 'stat_history'

    stats_code = models.ForeignKey(
        StatsCode,
        verbose_name='統計表 表ID',
        on_delete=models.PROTECT,
    )
    area = models.ForeignKey(
        Area,
        verbose_name='地域コード',
        on_delete=models.PROTECT
    )
    sub_category = models.ManyToManyField(
        SubCategory,
        verbose_name='サブカテゴリコード'
    )
    user = models.ForeignKey(
        User,
        verbose_name='ユーザー',
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        verbose_name='Attempt Time',
        auto_now_add=True,
    )
