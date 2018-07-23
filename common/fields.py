from __future__ import unicode_literals

import base64
import imghdr
import uuid

from django.core.files.base import ContentFile
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

DEFAULT_CONTENT_TYPE = 'application/octet-stream'
ALLOWED_IMAGE_TYPES = ('gif', 'png', 'jpeg', 'jpg')


class Base64ImageField(serializers.ImageField):
    """
    A django-rest-framework field for handling image-uploads through raw post
    data. It uses base64 for en-/decoding the contents of the file.
    """

    def to_internal_value(self, base64_data):
        # Check if this is a base64 string
        if isinstance(base64_data, basestring):
            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(base64_data)
            except TypeError:
                raise serializers.ValidationError(
                    _('Please upload a valid image.')
                )

            # Generate file name:
            # 12 characters are more than enough.
            file_name = str(uuid.uuid4())[:12]

            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)
            if file_extension not in ALLOWED_IMAGE_TYPES:
                raise serializers.ValidationError(
                    _('The type of the image couldn\'t been determined.')
                )
            complete_file_name = file_name + "." + file_extension
            data = ContentFile(decoded_file, name=complete_file_name)
        else:
            data = base64_data

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, filename, decoded_file):
        extension = imghdr.what(filename, decoded_file)
        return 'jpg' if extension == 'jpeg' else extension
