# from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import status, views
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import UserProfile
from .serializers import UserProfileSerializer

User = get_user_model()


class UserAvaterAPIView(views.APIView):
    parser_classes = [MultiPartParser]
    permission_classes = (IsAuthenticated,)

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
            data=request.data
        )

        if serializer.is_valid() is False:
            # Validation Error
            return Response(serializer.errors, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

        '''
        サムネイル画像をユーザーIDに紐づけて保存
        画像の縮小加工等はdjango-imagekitによりmodels内で処理される
        同時にExifも削除される
        '''
        user_profile = self.save_user_profile(
            user_id=request.user.id,
            image=serializer.validated_data.get('image')
        )
        data = {
            'image_url': user_profile.image.url
        }

        return Response(data, status.HTTP_200_OK)

    def save_user_profile(self, user_id, image):
        '''
        user_idとimageを渡して保存し､UserProfileオブジェクトを返す
        '''
        user = User.objects.get(pk=user_id)

        user_profile, created = UserProfile.objects.update_or_create(
            user=user,
            defaults={
                'user': user,
                'image': image,
            },
        )
        return user_profile
