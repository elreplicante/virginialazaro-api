from django.contrib import admin

from vlapi.models import Article, Category, Image


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'media_title', 'category', 'publication_date']
    list_filter = ['category', 'language']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass
