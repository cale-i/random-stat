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
        #  3. UserProfileのsocial_image_urlが存在しない
        data = {
            'is_default_image': True,
            'image_url': get_default_image(),
        }

        # UserProfileが存在しない場合
        if not queryset:
            return Response(data, status.HTTP_200_OK)

        # UserProfileが存在する場合

        user_profile = queryset.get(pk=user_id)
        data['image_url'] = None
        # if user_profile.image
        if user_profile.image:
            # ユーザーがイメージを登録している場合
            data['is_default_image'] = False
            data['image_url'] = user_profile.image.url

        if user_profile.social_image_url:
            # ソーシャルアカウントのイメージが存在する場合
            data['social_image_url'] = user_profile.social_image_url

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
        user_profile = save_user_profile(
            user_id=request.user.id,
            image=serializer.validated_data.get('image')
        )
        data = {
            'image_url': user_profile.image.url,
            'social_image_url': user_profile.social_image_url,
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
