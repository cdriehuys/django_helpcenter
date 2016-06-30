import json

from django.test import TestCase

from rest_framework.test import APIRequestFactory

from helpcenter import models
from helpcenter.api import serializers
from helpcenter.api.testing_utils import full_url
from helpcenter.testing_utils import create_article, create_category


class TestArticleSerializer(TestCase):
    """ Test cases for the Article serializer """

    def setUp(self):
        """ Create request factory for hyperlinked serializer """
        factory = APIRequestFactory()
        self.request = factory.get('helpcenter:helpcenter-api:article-list')

    def test_deserialize(self):
        """ Test deserializing an Article.

        Passing valid data to the serializer should allow the serializer
        to construct a new Article from the data.
        """
        data = {
            'title': 'Test Article',
            'body': '<p>Rich <strong>text</strong></p>',
            'category_id': None,
        }
        serializer = serializers.ArticleSerializer(data=data)

        self.assertTrue(serializer.is_valid())

        article = serializer.save()

        self.assertEqual(data['title'], article.title)
        self.assertEqual(data['body'], article.body)

    def test_serialize(self):
        """ Test serializing an article """
        article = create_article()
        serializer = serializers.ArticleSerializer(
            article, context={'request': self.request})

        expected_dict = {
            'body': article.body,
            'category': article.category,
            'category_id': None,
            'url': full_url('help:api:article-detail',
                            kwargs={'pk': article.pk}),
            'id': article.id,
            'time_published': article.time_published.isoformat(),
            'title': article.title,
        }
        expected = json.dumps(expected_dict)

        self.assertJSONEqual(expected, serializer.data)

    def test_serialize_with_category(self):
        """ Test serializing an article with a category.

        If an article has a category, that category's url should be
        contained in the serializer.
        """
        category = create_category()
        article = create_article(category=category)
        serializer = serializers.ArticleSerializer(
            article, context={'request': self.request})

        expected_dict = {
            'body': article.body,
            'category': full_url(
                'helpcenter:helpcenter-api:category-detail',
                kwargs={'pk': category.pk}),
            'category_id': article.category.id,
            'id': article.id,
            'time_published': article.time_published.isoformat(),
            'title': article.title,
            'url': full_url('help:api:article-detail',
                            kwargs={'pk': article.pk}),
        }
        expected = json.dumps(expected_dict)

        self.assertJSONEqual(expected, serializer.data)

    def test_update(self):
        """ Test updating an existing Article.

        If data is passed to an already existing Article, it should
        update the existing Article.
        """
        article = create_article()
        data = {
            'title': 'New Awesome Title',
        }
        serializer = serializers.ArticleSerializer(
            article, data=data, partial=True)

        self.assertTrue(serializer.is_valid())

        updated = serializer.save()

        self.assertEqual(1, models.Article.objects.count())
        self.assertEqual(data['title'], updated.title)


class TestCategorySerializer(TestCase):
    """ Test cases for the Category serializer """

    def setUp(self):
        """ Create request factory for hyperlinked serializer """
        factory = APIRequestFactory()
        self.request = factory.get('helpcenter:helpcenter-api:category-list')

    def test_deserialize(self):
        """ Test deserializing data into a Category instance.

        Passing valid data to the serializer should allow the serializer
        to construct a new Category instance.
        """
        data = {
            'title': 'Test Category',
            'parent_id': None,
        }
        serializer = serializers.CategorySerializer(data=data)

        self.assertTrue(serializer.is_valid())

        category = serializer.save()

        self.assertEqual(data['title'], category.title)
        self.assertEqual(data['parent_id'], category.parent)

    def test_deserialize_with_parent(self):
        """ Test deserializing a Category with a parent Category.

        The serializer should be able to create a Category with a
        parent if the parent's id is given.
        """
        parent = create_category(title='Parent Category')
        data = {
            'title': 'Test Category',
            'parent_id': parent.id,
        }
        serializer = serializers.CategorySerializer(data=data)

        self.assertTrue(serializer.is_valid(), msg=serializer.errors)

        category = serializer.save()

        self.assertEqual(parent, category.parent)

    def test_serialize(self):
        """ Test serializing a Category instance.

        Serializing a Category instance should return a JSON
        representation of the instance.
        """
        parent = create_category(title='Parent Category')
        category = create_category(parent=parent)
        serializer = serializers.CategorySerializer(
            category, context={'request': self.request})

        expected_dict = {
            'id': category.id,
            'parent': full_url(
                'helpcenter:helpcenter-api:category-detail',
                kwargs={'pk': parent.pk}),
            'parent_id': parent.id,
            'title': category.title,
            'url': full_url('help:api:category-detail',
                            kwargs={'pk': category.pk}),
        }
        expected = json.dumps(expected_dict)

        self.assertJSONEqual(
            expected,
            serializer.data,
            msg='\nExpected: {}\n  Actual: {}'.format(
                expected, serializer.data))

    def test_update(self):
        """ Test updating an existing Category.

        If data is passed to an existing Category, it should update the
        existing instance's data.
        """
        category = create_category()
        data = {
            'title': 'Better Title'
        }
        serializer = serializers.CategorySerializer(
            category, data=data, partial=True)

        self.assertTrue(serializer.is_valid())

        updated = serializer.save()

        self.assertEqual(1, models.Category.objects.count())
        self.assertEqual(data['title'], updated.title)
