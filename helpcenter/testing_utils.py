from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

from helpcenter import models


# Default Values
ARTICLE_BODY = 'Test article body.'
ARTICLE_TITLE = 'Test Article'

CATEGORY_TITLE = 'Test Category'


def create_article(title=ARTICLE_TITLE, body=ARTICLE_BODY,
                   time_published=None, category=None):
    """ Create an article for testing with default values """
    data = {
        'title': title,
        'body': body,
    }

    if time_published is not None:
        data['time_published'] = time_published

    if category is not None:
        data['category'] = category

    return models.Article.objects.create(**data)


def create_category(title=CATEGORY_TITLE, parent=None):
    """ Create a category for testing with default values """
    data = {
        'title': title,
    }

    if parent is not None:
        data['parent'] = parent

    return models.Category.objects.create(**data)


def instance_to_queryset_string(instance):
    """ Return a django queryset representation of an instance """
    str_type = str(type(instance)).strip("<>'").split('.')[-1]

    return "<{}: {}>".format(str_type, str(instance))


class AuthTestMixin(object):
    """ Mixin to make authentication in test cases easier """
    username = 'testuser'
    password = 'password'

    def add_permission(self, permission_name):
        """ Give the test user the given permission """
        perm = Permission.objects.get(codename=permission_name)
        self.user.user_permissions.add(perm)

    def login(self):
        """ Log in the client for the current test """

        # Use force_login which was introduced in Django 1.9 because
        # it's faster for testing purposes. Otherwise fall back to
        # standard login.

        if hasattr(self.client, 'force_login'):
            self.client.force_login(self.user)
        else:
            self.client.login(username=self.username, password=self.password)

    def setUp(self, *args, **kwargs):
        """ Create user for testing """
        super(AuthTestMixin, self).setUp(*args, **kwargs)

        self.user = get_user_model().objects.create_user(
            username=self.username, password=self.password)

    def tearDown(self, *args, **kwargs):
        """ Logout the current client """
        self.client.logout()

        super(AuthTestMixin, self).tearDown(*args, **kwargs)
