from django.conf import settings
from django.db import models


class ArticleQuerySet(models.QuerySet):

    def publication_descending(self):
        return self.all().order_by('-publication_date')

    def for_homepage(self, category_name):
        return self.publication_descending()[:settings.LIST_ARTICLES_BY_CATEGORY[category_name]]
