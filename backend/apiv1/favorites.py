from django.contrib.auth import get_user_model
from django.core.paginator import (
    EmptyPage,
    PageNotAnInteger,
    Paginator,
)

from estat.models import Favorites
from rest_framework.exceptions import ValidationError

from apiv1.serializers import FavoritesSerializer
from apiv1.stat_hist import (
    paginate_queryset,
    get_params
)

User = get_user_model()


def get_favorites(request, page_size=3):
    user = request.user
    # Anonymous Userの場合は処理なし
    if not user.is_authenticated:
        return

    queryset = Favorites.objects.filter(user=user.id) \
        .prefetch_related('sub_category') \
        .order_by('-created_at')

    page_obj, page_data = paginate_queryset(request, queryset, page_size)

    params = get_params(page_obj)

    return params, page_data
