from rest_framework import serializers

from vlapi.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    image_url = serializers.CharField(source='image.url')
    category = serializers.CharField(source='category.name')

    class Meta:
        model = Article
        exclude = ['id', 'image', 'language']
