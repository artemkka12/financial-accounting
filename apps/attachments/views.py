from models import Attachment
from rest_framework import viewsets
from rest_framework.parsers import FormParser, MultiPartParser
from serializers import AttachmentSerializer


class AttachmentViewSet(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser, FormParser)
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
