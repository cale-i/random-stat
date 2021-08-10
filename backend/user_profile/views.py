from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers, status, views
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import UserProfile
from .serializers import UserProfileSerializer

User = get_user_model()


class UserAvaterAPIView(views.APIView):
    parser_classes = [MultiPartParser]
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()

    # @login_required(login_url='/')
    def get(self, request, *args, **kwargs):
        # TODO
        # ユーザーIDに応じたアバターURLを取得
        pass

    def post(self, request, *args, **kwargs):
        '''
        "request.FILES"は DRF3.0から非推奨となったため､
        上記の代わりに"request.data"にてimageを取得する
        request.FILES: MultiValueDict
        request.data:  QueryDict
        request.FILES['image'] === request.data['image']
        request.FILES['image'].size === request.data['image'].size
        '''

        serializer = UserProfileSerializer(
            instance=request.POST,
            data=request.data)

        if serializer.is_valid() is False:
            # Validation Error
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(pk=request.user.id)
        image = serializer.validated_data.get('image', None)

        user_profile, created = UserProfile.objects.update_or_create(
            user=user,
            defaults={
                'user': user,
                'image': image,
            },
        )

        # TODO
        #
        # file保存
        # S3のPATHを取得
        # S3_BASE_URL = ''
        # UPLOAD_URL = f'{S3_BASE_URL}/{file.name}'
        # UPLOAD_URL = settings.BASE_DIR
        # path = os.path.join(UPLOAD_URL, file.name)

        # # S3にimg本体を保存

        return Response('uploaded', status.HTTP_200_OK)