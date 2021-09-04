from djoser.compat import get_user_email
from djoser.conf import settings
from rest_framework import status, views
from rest_framework.response import Response

from .serializers import SendEmailResetSerializer


class setPasswordView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = SendEmailResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.get_user()

        if user:
            context = {"user": user}
            to = [get_user_email(user)]
            settings.EMAIL.password_reset(self.request, context).send(to)

        return Response(status=status.HTTP_204_NO_CONTENT)
