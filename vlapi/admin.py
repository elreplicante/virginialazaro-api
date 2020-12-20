from django.contrib import admin

from vlapi.models import Article, Category


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'media_title', 'category', 'publication_date']
    list_filter = ['category', 'media_title']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
