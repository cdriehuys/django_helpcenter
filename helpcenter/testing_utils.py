from helpcenter import models


# Default Values
ARTICLE_BODY = 'Test article body.'
ARTICLE_TITLE = 'Test Article'


def create_article(title=ARTICLE_TITLE, body=ARTICLE_BODY,
                   time_published=None):
    """ Create an article for testing with default values """
    data = {
        'title': title,
        'body': body,
    }

    if time_published is not None:
        data['time_published'] = time_published

    return models.Article.objects.create(**data)


def instance_to_queryset_string(instance):
    """ Return a django queryset representation of an instance """
    str_type = str(type(instance)).strip("<>'").split('.')[-1]

    return "<{}: {}>".format(str_type, str(instance))
