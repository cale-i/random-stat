import factory

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


class StatNameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StatName


class GovOrgFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GovOrg


class TitleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Title


class StatsCodeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StatsCode
    stat_name = factory.SubFactory(StatNameFactory)
    gov_org = factory.SubFactory(GovOrgFactory)
    title = factory.SubFactory(TitleFactory)


class AreaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Area

    @factory.post_generation
    def stats_code(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for stat_code in extracted:
                self.stats_code.add(stat_code)


class TimeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Time
