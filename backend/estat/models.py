from django.db import models


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
        max_length=8
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
        max_length=8
    )
    name = models.CharField(
        verbose_name='統計コード名',
        null=False,
        max_length=255
    )


class StatsCode(models.Model):
    """"""

    class Meta:
        db_table = 'stats_code'

    id = models.CharField(
        verbose_name='表題',
        primary_key=True,
        max_length=3
    )
    stat_name_id = models.ForeignKey(
        StatName,
        verbose_name='政府統計コード',
        on_delete=models.PROTECT
    )
    gov_org_id = models.ForeignKey(
        GovOrg,
        verbose_name='担当機関コード',
        on_delete=models.PROTECT
    )
    title_id = models.ForeignKey(
        Title,
        verbose_name='表題コード',
        on_delete=models.PROTECT
    )
    statics_name = models.CharField(
        verbose_name='提供分類1',
        null=False, max_length=255
    )


class Category(models.Model):
    """
    カテゴリ
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
        max_length=255
    )
    name = models.CharField(
        verbose_name='カテゴリ名',
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
    eg.'全国', '北海道'
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
        max_length=4
    )


class Time(models.Model):
    """
    統計データ年度
    """

    class Meta:
        db_table = 'time'

    id = models.CharField(
        verbose_name='年度コード',
        primary_key=True,
        max_length=255
    )
    name = models.CharField(
        verbose_name='表示名',
        null=False,
        max_length=255
    )


class StatsData(models.Model):
    """
    統計データ
    """

    class Meta:
        db_table = 'stats_data'

    id = models.CharField(
        verbose_name='データ',
        primary_key=True,
        max_length=10
    )
    category_id = models.ManyToManyField(
        Category,
        verbose_name='カテゴリコード'
    )
    area_id = models.ForeignKey(
        Area,
        verbose_name='地域コード'
    )
    time_id = models.ForeignKey(
        Time,
        verbose_name='年度コード'
    )
    stat_code_id = models.ForeignKey(
        StatCode,
        verbose_name='政府統計コード'
    )
    unit = models.CharField(
        verbose_name='単位コード',
        null=False,
        max_length=10
    )
    value = models.PositiveIntegerField(
        verbose_name='統計データ数値',
        null=False
    )
