from django.core.urlresolvers import reverse
from django.test import TestCase

from helpcenter import utils
from helpcenter.testing_utils import (
    create_article, create_category, instance_to_queryset_string)


class TestArticleDetailView(TestCase):
    """ Test cases for Article detail view """

    def test_invalid_pk(self):
        """ Test getting an article's detail view with an invalid pk.

        If the pk used for the detail view doesn't exist, the page
        should 404.
        """
        url = utils.article_detail(pk=1)
        response = self.client.get(url)

        self.assertEqual(404, response.status_code)

    def test_valid_pk(self):
        """ Test getting an article's detail view. """
        article = create_article()

        url = utils.article_detail(article)
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertEqual(article, response.context['article'])


class TestArticleListView(TestCase):
    """ Test cases for Article list view """
    url = reverse('article-list')

    def test_no_articles(self):
        """ Test the list view with no articles.

        If there are no articles, the list of articles should be empty.
        """
        response = self.client.get(self.url)

        self.assertEqual(200, response.status_code)
        self.assertQuerysetEqual(response.context['articles'], [])

    def test_article(self):
        """ Test the list view with an article.

        If there is an article, it should be contained in the list of
        articles passed to the page.
        """
        article = create_article()

        response = self.client.get(self.url)

        self.assertEqual(200, response.status_code)
        self.assertQuerysetEqual(
            response.context['articles'],
            [instance_to_queryset_string(article)])

    def test_ordering(self):
        """ Test the ordering of the article listing.

        The default ordering of the list view should be alphabetically
        by title.
        """
        a1 = create_article(title='bananas')
        a2 = create_article(title='clementines')
        a3 = create_article(title='apples')

        response = self.client.get(self.url)

        expected = [
            instance_to_queryset_string(a3),
            instance_to_queryset_string(a1),
            instance_to_queryset_string(a2),
        ]

        self.assertEqual(200, response.status_code)
        self.assertQuerysetEqual(
            response.context['articles'],
            expected)


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

        url = utils.category_detail(category)
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
        url = utils.category_detail(pk=1)
        response = self.client.get(url)

        self.assertEqual(404, response.status_code)

    def test_valid_pk(self):
        """ Test getting the detail view of a category.

        If there is a category with the given pk, its detail view should
        be shown.
        """
        category = create_category()

        url = utils.category_detail(category)
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertEqual(category, response.context['category'])


class TestIndexView(TestCase):
    """ Test cases for the index view """
    url = reverse('index')

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
