from rest_framework import status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import LoginRecord
from .guest import get_serializer


class RecordAPIView(views.APIView):
    '''
    ユーザーに紐付いたログイン履歴を返す
    returnのフォーマット:[{},{},{}...]
    pagenationは行わず､最新10件のみを返す
    '''
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):

        user = request.user
        records = LoginRecord.objects.filter(user=user)[:10]
        serializer = get_serializer(instance=records, user=user)
        return Response(serializer.data, status.HTTP_200_OK)
