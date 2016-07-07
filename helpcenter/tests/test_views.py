from django.core.urlresolvers import reverse
from django.test import TestCase

from helpcenter.testing_utils import (
    create_article, create_category, instance_to_queryset_string)


class TestArticleDetailView(TestCase):
    """ Test cases for Article detail view """

    def test_invalid_pk(self):
        """ Test getting an article's detail view with an invalid pk.

        If the pk used for the detail view doesn't exist, the page
        should 404.
        """
        url = reverse('helpcenter:article-detail', kwargs={'pk': 1})
        response = self.client.get(url)

        self.assertEqual(404, response.status_code)

    def test_valid_pk(self):
        """ Test getting an article's detail view. """
        article = create_article()

        url = article.get_absolute_url()
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertEqual(article, response.context['article'])


class TestCategoryDetailView(TestCase):
    """ Test cases for the Category detail view """

    def test_context_data(self):
        """ Test adding additional context data.

        The category detail view should add additional context to the
        response such as the articles and categories that are children
        of the current category.
        """
        category = create_category()
        article = create_article(category=category)
        create_article(title='No Category')
        child = create_category(parent=category, title='child category')
        create_category(title='No Parent')

        url = category.get_absolute_url()
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertQuerysetEqual(
            response.context['categories'],
            [instance_to_queryset_string(child)])
        self.assertQuerysetEqual(
            response.context['articles'],
            [instance_to_queryset_string(article)])

    def test_invalid_pk(self):
        """ Test getting the detail view with an invalid pk.

        If no Category with the given pk exists, the page should 404.
        """
        url = reverse('helpcenter:category-detail', kwargs={'pk': 1})
        response = self.client.get(url)

        self.assertEqual(404, response.status_code)

    def test_valid_pk(self):
        """ Test getting the detail view of a category.

        If there is a category with the given pk, its detail view should
        be shown.
        """
        category = create_category()

        url = category.get_absolute_url()
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertEqual(category, response.context['category'])


class TestIndexView(TestCase):
    """ Test cases for the index view """
    url = reverse('helpcenter:index')

    def test_article_listing(self):
        """ Test which articles are listed in the index view.

        Only articles with no category should be listed in this view.
        """
        article = create_article()
        create_article(title='categorized', category=create_category())

        response = self.client.get(self.url)

        self.assertEqual(200, response.status_code)
        self.assertQuerysetEqual(
            response.context['articles'],
            [instance_to_queryset_string(article)])

    def test_category_listing(self):
        """ Test which categories are listed in the index view.

        Only categories with no parent category should be listed in this
        view.
        """
        category = create_category()
        create_category(parent=category, title='child category')

        response = self.client.get(self.url)

        self.assertEqual(200, response.status_code)
        self.assertQuerysetEqual(
            response.context['categories'],
            [instance_to_queryset_string(category)])


class TestSearchView(TestCase):
    """ Test cases for the search view """
    url = reverse('helpcenter:search')

    def test_get(self):
        """ Test submitting a plain GET request.

        The initial GET request to the page should display a search box.
        """
        response = self.client.get(self.url)

        self.assertEqual(200, response.status_code)
        self.assertFalse(response.context['articles'].exists())
        self.assertIsNone(response.context['query'])

    def test_get_with_query(self):
        """ Test submitting a GET request with a search query.

        If there is a search query in the url, the response should
        contain context objects with the query and its results.
        """
        article = create_article(title='Test Article')

        url = '{}?q={}'.format(self.url, 'test')
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertEqual('test', response.context['query'])
        self.assertQuerysetEqual(
            response.context['articles'],
            [instance_to_queryset_string(article)])
