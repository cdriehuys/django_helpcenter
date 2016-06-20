from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from helpcenter import models
from helpcenter.api import serializers


class ArticleViewSet(viewsets.ModelViewSet):
    """ View set for the Article model """
    permission_classes = (
        permissions.DjangoModelPermissionsOrAnonReadOnly,
    )
    queryset = models.Article.objects.all()
    serializer_class = serializers.ArticleSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """ View set for the Category model """
    permission_classes = (
        permissions.DjangoModelPermissionsOrAnonReadOnly,
    )
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer


class PermissionsView(APIView):
    """ View for user permissions in the help center """
    permission_classes = (permissions.IsAuthenticated,)
    permissions_to_check = [
        'add_article',
        'add_category',
        'change_article',
        'change_category',
        'delete_article',
        'delete_category',
    ]

    def get(self, request, *args, **kwargs):
        """ Handle GET requests """
        r = {}

        for perm in self.permissions_to_check:
            r[perm] = request.user.has_perm(perm)

        return Response(r)
