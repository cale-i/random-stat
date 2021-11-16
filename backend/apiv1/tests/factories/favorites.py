import factory

from estat.models import Favorites
from apiv1.tests.factories.estat import (
    StatsCodeFactory,
    AreaFactory,
)


class FavoritesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Favorites

    stats_code = factory.SubFactory(StatsCodeFactory, id='0003412176')
    area = factory.SubFactory(AreaFactory, id='00000')

    @factory.post_generation
    def sub_category(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for sub_category in extracted:
                self.sub_category.add(sub_category)
