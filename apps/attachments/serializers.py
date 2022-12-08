from rest_framework import serializers

from .models import Attachment

__all__ = ["AttachmentSerializer", "ShortAttachmentSerializer"]


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = "__all__"


class ShortAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ["url"]
