from rest_framework import serializers

from helpcenter import models


class ArticleSerializer(serializers.ModelSerializer):
    """ Serializer for the Article model """

    class Meta:
        fields = ('body', 'id', 'time_published', 'title')
        model = models.Article
        read_only_fields = ('id',)
