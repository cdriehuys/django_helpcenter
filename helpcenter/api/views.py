from rest_framework import viewsets

from helpcenter import models
from helpcenter.api import serializers


class ArticleViewSet(viewsets.ModelViewSet):
    """ View set for the Article model """
    queryset = models.Article.objects.all()
    serializer_class = serializers.ArticleSerializer
