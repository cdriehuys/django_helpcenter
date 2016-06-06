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
