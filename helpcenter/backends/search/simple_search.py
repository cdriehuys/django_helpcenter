from django.db.models import Q

from helpcenter import models


class SimpleSearch:
    """ Simple keyword search backend """

    def search(self, query):
        """ Search articles for given query """
        q_filter = None
        for word in query.split():
            if q_filter is None:
                q_filter = Q(title__icontains=word) | Q(body__icontains=word)
            else:
                q_filter = q_filter | Q(title__icontains=word)
                q_filter = q_filter | Q(body__icontains=word)

        return models.Article.objects.filter(q_filter)
