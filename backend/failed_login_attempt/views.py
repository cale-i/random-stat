from django.contrib.auth import user_login_failed
from rest_framework import status, views
from rest_framework.response import Response


class FailedLoginAttemptAPIView(views.APIView):

    def post(self, request, *args, **kwargs):
        user_login_failed.send(
            sender=__name__, credentials=None, request=request)

        return Response(status.HTTP_204_NO_CONTENT)
