from rest_framework import viewsets
from rest_framework.parsers import FormParser, MultiPartParser

from .models import Attachment
from .serializers import AttachmentSerializer

__all__ = ["AttachmentViewSet"]


class AttachmentViewSet(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser, FormParser)
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
