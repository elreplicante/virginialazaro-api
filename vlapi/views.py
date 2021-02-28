from rest_framework import viewsets
from rest_framework.response import Response

from vlapi.models import Category
from vlapi.serializers import ArticleSerializer


class CategoriesViewSet(viewsets.ViewSet):

    def list(self, request):
        language = request.META['HTTP_X_LANGUAGE']
        categories = Category.objects.all()
        payload = {
            category.name: ArticleSerializer(
                category.articles.select_related('image').filter(language=language).for_homepage(category.name),
                many=True
            ).data
            for category in categories
        }

        return Response(payload)

    def get(self, request, *args, **kwargs):
        language = request.META['HTTP_X_LANGUAGE']
        category = Category.objects.get(name=kwargs['name'])
        articles = category.articles.select_related('image').publication_descending().filter(language=language)
        payload = ArticleSerializer(articles, many=True).data

        return Response(payload)

