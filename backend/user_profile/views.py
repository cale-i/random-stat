from django.contrib.auth import get_user_model
from rest_framework import status, views
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from .models import UserProfile
from .serializers import UserProfileSerializer
from .helpers import (
    save_user_profile,
    get_default_image
)

User = get_user_model()


class UserAvaterAPIView(views.APIView):
    parser_classes = [MultiPartParser]
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):

        # ユーザーIDに応じたアバターURLを取得
        user_id = request.user.id
        queryset = UserProfile.objects.filter(pk=user_id)

        # default response data
        # 以下の場合はdefaultのdataを返す
        #  1. UserProfileオブジェクトが存在しない
        #  2. UserProfileのimageが存在しない
        data = {
            'is_default_image': True,
            'image_url': self.get_default_image(),
        }

        # アバターが登録されている場合
        if queryset:
        user_profile = queryset.get(pk=user_id)
        if user_profile.image:
                # user_profile.imageがNULLでない場合
            data['image_url'] = user_profile.image.url
                data['is_default_image'] = False

        return Response(data, status.HTTP_200_OK)

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

    def delete(self, request, *args, **kwargs):
        # ユーザーIDに応じたアバターURLを取得
        user_id = request.user.id
        queryset = UserProfile.objects.filter(pk=user_id)
        if queryset:
            # imageをNoneで上書き
            user_profile = queryset.get(pk=user_id)
            user_profile.image = None
            user_profile.save()

            return Response(status.HTTP_204_NO_CONTENT)
        else:
            # 削除するアバターが存在しない場合(不正なアクセス)
            return Response('不正な操作です', status.HTTP_405_METHOD_NOT_ALLOWED)
