from django.core.urlresolvers import reverse
from django.test import TestCase

from helpcenter import models
from helpcenter.testing_utils import (
    AuthTestMixin, create_article, create_category,
    instance_to_queryset_string)


class TestArticleCreateView(AuthTestMixin, TestCase):
    """ Test cases for the Article creation view """
    url = reverse('helpcenter:article-create')

    def test_initial(self):
        """ Test the initial GET request to the view.

        On the first GET request, the view should have a blank, unbound
        form as context.
        """
        self.add_permission('add_article')
        self.login()

        response = self.client.get(self.url)

        self.assertEqual(200, response.status_code)
        self.assertFalse(response.context['form'].is_bound)

    def test_no_permission(self):
        """ Test the view with no permission to create articles.

        If the current user doesn't have permission to create articles,
        they shouldn't be allowed to access the view.
        """
        self.login()

        response = self.client.get(self.url)

        self.assertEqual(403, response.status_code)

    def test_post_blank(self):
        """ Test submitting blank data as a POST request.

        If an empty POST request is submitted, the form should be bound
        and shown to the user with errors for the required fields.
        """
        self.add_permission('add_article')
        self.login()

        response = self.client.post(self.url, {})

        expected_errors = {
            'body': ['This field is required.'],
            'title': ['This field is required.'],
        }

        self.assertEqual(200, response.status_code)
        self.assertTrue(response.context['form'].is_bound)
        self.assertEqual(expected_errors, response.context['form'].errors)

    def test_post_valid_data(self):
        """ Test submitting valid data as a POST request.

        If valid data is submitted as a POST request, a new Article
        instance should be created with the validated data.
        """
        self.add_permission('add_article')
        self.login()

        category = create_category()
        data = {
            'body': 'Test body text.',
            'category': category.pk,
            'title': 'Test Title',
        }

        response = self.client.post(self.url, data)

        article = models.Article.objects.get(title=data['title'])

        self.assertRedirects(response, article.get_absolute_url())
        self.assertEqual(1, models.Article.objects.count())
        self.assertEqual(data['body'], article.body)
        self.assertEqual(category, article.category)


class TestArticleDeleteView(AuthTestMixin, TestCase):
    """ Test cases for Article delete view """

    def test_get(self):
        """ Test a GET request to the Article delete view.

        A GET request should display a page that has the instance to be
        deleted as context.
        """
        self.add_permission('delete_article')
        self.login()

        article = create_article()

        url = article.get_delete_url()
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertEqual(article, response.context['object'])

    def test_no_permission(self):
        """ Test delete view as a user with no delete permission.

        If the user requesting the view has no permission to delete
        articles, the view should return a 403 response.
        """
        article = create_article()

        url = article.get_delete_url()
        response = self.client.get(url)

        self.assertEqual(403, response.status_code)

    def test_post(self):
        """ Test a POST request to the Article delete view.

        A POST request to the view should delete the instance and
        redirect to the instance's parent's detail url.
        """
        self.add_permission('delete_article')
        self.login()

        article = create_article()
        redirect_url = article.get_parent_url()

        url = article.get_delete_url()
        response = self.client.post(url)

        self.assertRedirects(response, redirect_url)
        self.assertEqual(0, models.Article.objects.count())


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


class TestArticleUpdateView(AuthTestMixin, TestCase):
    """ Test cases for the Article update view """

    def test_initial(self):
        """ Test the initial GET request to the view.

        The initial GET request to the view should have a form that is
        unbound, but its initial data should be that of the Article
        instance being updated.
        """
        self.add_permission('change_article')
        self.login()

        category = create_category()
        data = {
            'title': 'Test Title',
            'body': 'Test body text.',
            'category': category,
        }
        article = create_article(**data)

        url = article.get_update_url()
        response = self.client.get(url)

        form = response.context['form']

        self.assertEqual(200, response.status_code)
        self.assertFalse(form.is_bound)
        self.assertEqual(data['title'], form.initial['title'])
        self.assertEqual(data['body'], form.initial['body'])
        self.assertEqual(data['category'].pk, form.initial['category'])

    def test_no_permission(self):
        """ Test accessing the view with no permission.

        If a user who doesn't have permission to change articles tries
        to access the view, they should not be able to.
        """
        self.login()

        article = create_article()

        url = article.get_update_url()
        response = self.client.get(url)

        self.assertEqual(403, response.status_code)

    def test_valid_data(self):
        """ Test submitting valid data with a POST request.

        If valid data is submitted in a POST request, the Article
        instance should be updated with the new data.
        """
        self.add_permission('change_article')
        self.login()

        category = create_category()
        article = create_article()
        data = {
            'title': 'My Awesome Title',
            'body': 'New Awesome Body Text',
            'category': category.id,
        }

        url = article.get_update_url()
        response = self.client.post(url, data)

        article.refresh_from_db()

        self.assertRedirects(response, article.get_absolute_url())
        self.assertEqual(1, models.Article.objects.count())
        self.assertEqual(data['title'], article.title)
        self.assertEqual(data['body'], article.body)
        self.assertEqual(category, article.category)


class TestCategoryCreateView(AuthTestMixin, TestCase):
    """ Test cases for the Category creation view """
    url = reverse('helpcenter:category-create')

    def test_initial(self):
        """ Test the first GET request to the view.

        The first get request to the view should pass a blank
        CategoryForm to the template as context.
        """
        self.add_permission('add_category')
        self.login()

        response = self.client.get(self.url)

        self.assertEqual(200, response.status_code)
        self.assertFalse(response.context['form'].is_bound)

    def test_no_permission(self):
        """ Test the view with no permission to create categories.

        If the user making the request has no permission to add
        categories, the view should 403.
        """
        self.login()

        response = self.client.get(self.url)

        self.assertEqual(403, response.status_code)

    def test_post_blank(self):
        """ Test submitting blank data with a POST request.

        If a blank request is submitted, the form should be shown to the
        user again with errors. Any data they submitted should be
        retained.
        """
        self.add_permission('add_category')
        self.login()

        parent = create_category()
        data = {
            'parent': parent.id,
        }

        response = self.client.post(self.url, data)

        expected_errors = {
            'title': ['This field is required.'],
        }

        self.assertEqual(200, response.status_code)
        self.assertTrue(response.context['form'].is_bound)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(expected_errors, response.context['form'].errors)

    def test_post_valid_data(self):
        """ Test submitting valid data through a POST request.

        If valid data is submitted, a new category should be created and
        the user should be redirected to the detail view for the new
        category.
        """
        self.add_permission('add_category')
        self.login()

        parent = create_category(title='Parent Category')
        data = {
            'parent': parent.id,
            'title': 'Test Category',
        }

        response = self.client.post(self.url, data)

        category = models.Category.objects.get(title=data['title'])

        self.assertRedirects(response, category.get_absolute_url())
        self.assertEqual(parent, category.parent)


class TestCategoryDeleteView(AuthTestMixin, TestCase):
    """ Test cases for the Category delete view """

    def test_get(self):
        """ Test a GET request to the Category delete view.

        A GET request to this view should show a page that has the
        instance to be deleted as context.
        """
        self.add_permission('delete_category')
        self.login()

        category = create_category()

        url = category.get_delete_url()
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertEqual(category, response.context['object'])

    def test_no_permission(self):
        """ Test requesting the view with no delete permission.

        If the view is requested by a user who does not have permission
        to delete a Category instance, the view should return a 403
        response code.
        """
        category = create_category()

        url = category.get_delete_url()
        response = self.client.get(url)

        self.assertEqual(403, response.status_code)

    def test_post(self):
        """ Test a POST request to the Category delete view.

        A POST request to the view should delete the instance and
        redirect to the instances parent object.
        """
        self.add_permission('delete_category')
        self.login()

        category = create_category()
        redirect_url = category.get_parent_url()

        url = category.get_delete_url()
        response = self.client.post(url)

        self.assertRedirects(response, redirect_url)
        self.assertEqual(0, models.Category.objects.count())


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


class TestCategoryUpdateView(AuthTestMixin, TestCase):
    """ Test cases for the category update view """

    def test_initial_get(self):
        """ Test the initial GET request to the view.

        The initial GET request to the view should have a form that is
        pre-populated with the category's data.
        """
        self.add_permission('change_category')
        self.login()

        category = create_category(
            title='Cool Category', parent=create_category())

        url = category.get_update_url()
        response = self.client.get(url)

        form = response.context['form']

        self.assertEqual(200, response.status_code)
        self.assertEqual(category.title, form.initial['title'])
        self.assertEqual(category.parent.pk, form.initial['parent'])

    def test_no_permission(self):
        """ Test the view with no permission to change categories.

        If a user who doesn't have permission to change categories tries
        to access the view, they should be denied access.
        """
        self.login()

        category = create_category()

        url = category.get_update_url()
        response = self.client.get(url)

        self.assertEqual(403, response.status_code)

    def test_valid_data(self):
        """ Test sending valid data through a POST request.

        If valid data is submitted to the form, the category's data
        should be updated.
        """
        self.add_permission('change_category')
        self.login()

        parent = create_category()
        category = create_category(title='Category', parent=parent)
        new_parent = create_category(title='New Parent')
        data = {
            'title': 'New Title',
            'parent': new_parent.pk,
        }

        url = category.get_update_url()
        response = self.client.post(url, data)

        category.refresh_from_db()

        self.assertRedirects(response, category.get_absolute_url())
        self.assertEqual(3, models.Category.objects.count())
        self.assertEqual(data['title'], category.title)
        self.assertEqual(new_parent, category.parent)


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
