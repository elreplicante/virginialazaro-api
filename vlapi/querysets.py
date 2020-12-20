from django.conf import settings
from django.db import models


class ArticleQuerySet(models.QuerySet):

    def publication_descending(self):
        return self.all().order_by('-publication_date')
