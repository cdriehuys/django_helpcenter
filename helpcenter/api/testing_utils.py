from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory


_factory = APIRequestFactory()


def full_url(view_name, kwargs=None):
    """ Return the full url of the given view """
    url = reverse(view_name, kwargs=kwargs)
    request = _factory.get(url)

    return request.build_absolute_uri()
