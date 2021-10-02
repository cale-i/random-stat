from django.contrib.auth import get_user_model
from django.core.paginator import (
    EmptyPage,
    PageNotAnInteger,
    Paginator,
)

from estat.models import StatHistory
from rest_framework.exceptions import ValidationError

from apiv1.serializers import StatHistorySerializer

User = get_user_model()


def persist_stat_history(params, user=None):
    # Anonymous Userの場合は処理なし
    if not user.is_authenticated:
        return

    serializer = StatHistorySerializer(data={**params, 'user': user.id})

    try:
        serializer.is_valid(raise_exception=True)
        serializer.save()
    except ValidationError as e:
        raise ValidationError(e.args[0])


def get_stat_history(request, page_size=3):
    user = request.user
    # Anonymous Userの場合は処理なし
    if not user.is_authenticated:
        return

    queryset = StatHistory.objects.filter(user=user.id) \
        .prefetch_related('sub_category') \
        .order_by('-created_at')

    page_obj, page_data = paginate_queryset(request, queryset, page_size)

    params = get_params(page_obj)

    return params, page_data


def paginate_queryset(request, queryset, count):
    paginator = Paginator(queryset, count)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    page_data = get_page_data(queryset, page_obj)

    return page_obj, page_data


def get_page_data(queryset, page_obj):

    return {
        # 'prev': page_obj.previous_page_number(),
        'current': page_obj.number,
        'count': queryset.count(),
        # 'next': page_obj.next_page_number(),
    }


def get_params(page_obj):
    params = {}
    for query in page_obj.object_list:
        params = {
            'stats_code': query.stats_code.id,
            'area': query.area.id,
            'sub_category': [e.id for e in query.sub_category.all()]
        }
    return params
