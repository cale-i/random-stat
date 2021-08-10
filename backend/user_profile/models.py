from django.db import models
# from accounts.models import CustomUser
from django.contrib.auth import get_user_model

import uuid
from django.core.validators import FileExtensionValidator, validate_image_file_extension

import os
IMAGE_EXTENSIONS = ['png', 'jpg', 'gif']

User = get_user_model()


def get_image_path(instance, filename):

    prefix = 'avatar'
    name = str(uuid.uuid4()).replace('-', '')
    extension = filename.split('.')[-1]
    filename = f'{name}.{extension}'
    return os.path.join(prefix, filename)


class UserProfile(models.Model):
    class Meta:
        db_table = 'user_profile'

    # specify User model
    user = models.OneToOneField(
        User,
        related_name='user_profile',
        on_delete=models.CASCADE,
        primary_key=True
    )

    image = models.ImageField(
        max_length=255,
        null=True,
        # upload_to="avatar/",
        upload_to=get_image_path,
        validators=[
            FileExtensionValidator(IMAGE_EXTENSIONS),
            validate_image_file_extension
        ]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
