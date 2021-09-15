from estat.models import StatHistory
from apiv1.serializers import (
    StatHistorySerializer,
    SubCategorySerializer,
)
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

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
