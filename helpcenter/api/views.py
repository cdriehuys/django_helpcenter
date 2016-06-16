from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from helpcenter import models
from helpcenter.api import serializers


class ArticleViewSet(viewsets.ModelViewSet):
    """ View set for the Article model """
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)
    queryset = models.Article.objects.all()
    serializer_class = serializers.ArticleSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """ View set for the Category model """
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
