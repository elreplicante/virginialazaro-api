from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from vlapi.models import Article, Category
from vlapi.serializers import ArticleSerializer


class CategoriesViewSet(viewsets.ViewSet):

    def list(self, request):
        categories = Category.objects.all()
        payload = {
            category.name: ArticleSerializer(
                (
                    category.
                    articles.
                    select_related('image').
                    filter(language=request.language).
                    for_homepage(category.name)
                ),
                many=True
            ).data
            for category in categories
        }

        return Response(payload)

    def get(self, request, *args, **kwargs):
        category = Category.objects.get(name=kwargs['name'])
        articles = (
            category.
            articles.
            select_related('image').
            publication_descending().
            filter(language=request.language)
        )
        payload = ArticleSerializer(articles, many=True).data

        return Response(payload)


class ArticlesView(APIView):

    def get(self, request, *args, **kwargs):
        articles = (
            Article.objects.select_related('category', 'image').
            filter(language=request.language)
            .all()
            .publication_descending()
        )
        payload = ArticleSerializer(articles, many=True).data

        return Response(payload)
