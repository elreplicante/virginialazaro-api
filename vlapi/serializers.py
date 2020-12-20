from rest_framework import serializers

from vlapi.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    image_url = serializers.CharField(source='image.url')

    class Meta:
        model = Article
        exclude = ['id', 'category', 'image']
