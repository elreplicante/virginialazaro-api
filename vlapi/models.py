from django.db import models

from vlapi.querysets import ArticleQuerySet


class Article(models.Model):
    title = models.CharField(null=False, blank=False, max_length=100)
    excerpt = models.TextField(blank=True)
    media_title = models.CharField(null=False, blank=False, max_length=100)
    media_link = models.URLField(blank=False)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='articles')
    publication_date = models.DateField()
    image = models.OneToOneField('Image', on_delete=models.PROTECT)

    objects = ArticleQuerySet.as_manager()

    class Meta:
        db_table = 'articles'

    def __str__(self):
        return f'{self.title}'


class Category(models.Model):
    name = models.CharField(null=False, blank=False, max_length=100)

    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f'{self.name}'


class Image(models.Model):
    url = models.URLField(blank=False)

    class Meta:
        db_table = 'images'
        verbose_name_plural = 'Images'

    def __str__(self):
        return f'{self.article} {self.url}'
