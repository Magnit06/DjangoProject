from bboard.models import Bb, Rubric, Comment
from rest_framework.viewsets import ModelViewSet

from .serializers import *


class BbViewSet(ModelViewSet):
    serializer_class = BbSerializer
    queryset = Bb.objects.all()


class RubricViewSet(ModelViewSet):
    serializer_class = RubricSerializer
    queryset = Rubric.objects.all()


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
