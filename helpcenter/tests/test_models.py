from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

from helpcenter import models
from helpcenter.testing_utils import create_article, create_category


class TestArticleModel(TestCase):
    """ Test cases for the Article model """

    def test_create(self):
        """ Test creating an article with all its fields.

        If arguments are passed to an article, it should be created with
        those parameters already set.
        """
        category = create_category()
        title = 'Test Article'
        body = 'This is a test article only for <em>testing</em>.'
        time = timezone.now()

        article = models.Article.objects.create(
            category=category,
            title=title,
            body=body,
            time_published=time)

        self.assertEqual(1, models.Article.objects.count())
        self.assertEqual(category, article.category)
        self.assertEqual(title, article.title)
        self.assertEqual(body, article.body)
        self.assertEqual(time, article.time_published)

    def test_defaults(self):
        """ Test the default values when creating an article.

        If an article is created with only the necessary values, certain
        defaults should automatically be filled in.
        """
        title = 'Test Article'
        body = 'Test body.'

        start = timezone.now()
        article = models.Article.objects.create(
            title=title,
            body=body)
        end = timezone.now()

        self.assertIsNone(article.category)
        self.assertTrue(start <= article.time_published <= end)

    def test_get_absolute_url(self):
        """ Test getting an Article instance's url.

        This method should return the URL of the instance's detail view.
        """
        article = create_article()

        url = reverse('helpcenter:article-detail', kwargs={'pk': article.pk})

        self.assertEqual(url, article.get_absolute_url())

    def test_get_parent_url(self):
        """ Test getting the url of an Article's parent page.

        If an article has a Category, this method should return the url
        of the detail view for the parent Category.
        """
        category = create_category()
        article = create_article(category=category)

        expected = category.get_absolute_url()

        self.assertEqual(expected, article.get_parent_url())

    def test_get_parent_url_no_parent(self):
        """ Test getting the url of an Article's parent page.

        If an article does not have a Category, this method should
        return the url of the index view.
        """
        article = create_article()

        expected = reverse('helpcenter:index')

        self.assertEqual(expected, article.get_parent_url())

    def test_string_conversion(self):
        """ Test converting an Article to a string.

        Converting an Article instance to a string should return a
        string with the article's title.
        """
        article = models.Article(title='Test Article', body='body')

        self.assertEqual(article.title, str(article))


class TestCategoryModel(TestCase):
    """ Test cases for the Category model """

    def test_create(self):
        """ Test creating a Category with all its fields.

        Any arguments passed to a Category should affect the created
        instance's attributes.
        """
        title = 'Test Category'
        parent = create_category(title='Parent Category')

        category = models.Category.objects.create(title=title, parent=parent)

        self.assertEqual(title, category.title)
        self.assertEqual(parent, category.parent)

    def test_delete_parent(self):
        """ Test deleting a parent category.

        If a parent category is deleted, its child categories should
        have their parent set to NULL rather than being deleted.
        """
        parent = create_category(title='parent')
        create_category(title='child', parent=parent)

        parent.delete()

        self.assertEqual(1, models.Category.objects.count())
        self.assertEqual('child', models.Category.objects.get().title)

    def test_get_absolute_url(self):
        """ Test getting a Category instance's absolute url.

        This method should return the url of the instance's detail view.
        """
        category = create_category()

        url = reverse('helpcenter:category-detail', kwargs={'pk': category.pk})

        self.assertEqual(url, category.get_absolute_url())

    def test_get_parent_url(self):
        """ Test getting the url of a Category's parent container.

        If the Category has a parent Category, the url of the parent
        Category's detail view should be returned.
        """
        parent = create_category()
        category = create_category(parent=parent)

        expected = parent.get_absolute_url()

        self.assertEqual(expected, category.get_parent_url())

    def test_get_parent_url_no_parent(self):
        """ Test getting the url of a Category's parent container.

        If a Category has no parent Category, this method should return
        the url of the index view.
        """
        category = create_category()

        expected = reverse('helpcenter:index')

        self.assertEqual(expected, category.get_parent_url())

    def test_num_articles(self):
        """ Test num_articles property with articles in category.

        This property should return the number of articles in a
        Category.
        """
        category = create_category()
        create_article(category=category)

        self.assertEqual(1, category.num_articles)

    def test_num_articles_nested(self):
        """ Test num_articles property with nested categories.

        The property should loop through all the instance's child
        categories and include the number of articles in each of them.
        """
        category = create_category()
        child = create_category(title='child', parent=category)
        create_article(category=child)

        self.assertEqual(1, category.num_articles)

    def test_string_conversion(self):
        """ Test converting a Category instance to a string.

        Converting a Category instance to a string should return the
        instance's title.
        """
        category = models.Category(title='Test Category')

        self.assertEqual(category.title, str(category))
