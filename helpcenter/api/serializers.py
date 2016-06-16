from rest_framework import serializers

from helpcenter import models


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    """ Serializer for the Article model """

    class Meta:
        extra_kwargs = {
            'category': {
                'view_name': 'api:category-detail',
            },
            'url': {
                'view_name': 'api:article-detail',
            },
        }
        fields = (
            'body', 'category', 'id', 'time_published', 'title', 'url'
        )
        model = models.Article
        read_only_fields = ('id',)


class CategorySerializer(serializers.ModelSerializer):
    """ Serializer for the Category model """

    class Meta:
        fields = ('id', 'parent', 'title')
        model = models.Category
        read_only_fields = ('id',)
