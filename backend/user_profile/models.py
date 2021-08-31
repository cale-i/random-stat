import os
import uuid

from django.contrib.auth import get_user_model
from django.core.validators import (FileExtensionValidator,
                                    validate_image_file_extension)
from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

ALLOWED_EXTENSIONS = ['png', 'jpg', 'gif']

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

    image = ProcessedImageField(
        max_length=255,
        null=True,
        blank=True,
        upload_to=get_image_path,
        processors=[ResizeToFill(300, 300)],  # (width, height)
        options={'quality': 60},
        validators=[
            FileExtensionValidator(ALLOWED_EXTENSIONS),
            validate_image_file_extension
        ]
    )
    social_image_url = models.URLField(
        max_length=255,
        null=True,
        blank=True,
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
