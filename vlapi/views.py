from django.conf import settings
from rest_framework import viewsets
from rest_framework.response import Response

from vlapi.models import Category
from vlapi.serializers import ArticleSerializer


class CategoriesViewSet(viewsets.ViewSet):

    def list(self, request):
        categories = Category.objects.all()
        payload = {
            category.name: ArticleSerializer(
                category.articles.publication_descending()[:settings.LIST_ARTICLES_BY_CATEGORY[category.name]],
                many=True
            ).data
            for category in categories
        }

        return Response(payload)

    def get(self, request, *args, **kwargs):
        category = Category.objects.get(name=kwargs['name'])
        payload = ArticleSerializer(category.articles.publication_descending(), many=True).data

        return Response(payload)

