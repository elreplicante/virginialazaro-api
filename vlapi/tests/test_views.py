import pytest

from vlapi.models import Article, Category, Image


@pytest.fixture
def culture_article():
    image = Image.objects.create(url='http://culture-image.url')
    category = Category.objects.get(name='culture')
    return Article.objects.create(
        title='Culture Article',
        excerpt='The excerpt',
        media_title='The link title',
        media_link='http://link.title',
        category=category,
        publication_date='2020-12-13',
        image=image,
    )


@pytest.fixture
def newest_culture_article():
    image = Image.objects.create(url='http://newest-culture-image.url')
    category = Category.objects.get(name='culture')
    return Article.objects.create(
        title='Newest Culture Article',
        excerpt='The excerpt',
        media_title='The link title',
        media_link='http://link.title',
        category=category,
        publication_date='2020-12-14',
        image=image,
    )


@pytest.fixture
def pixels_article():
    category = Category.objects.get(name='pixels')
    image = Image.objects.create(url='http://pixels-image.url')
    return Article.objects.create(
        title='Pixels Article',
        excerpt='The excerpt',
        media_title='The link title',
        media_link='http://link.title',
        category=category,
        publication_date='2020-12-13',
        image=image,
    )


@pytest.fixture
def newest_pixels_article():
    image = Image.objects.create(url='http://newest-pixels-image.url')
    category = Category.objects.get(name='pixels')
    return Article.objects.create(
        title='Newest Pixels Article',
        excerpt='The excerpt',
        media_title='The link title',
        media_link='http://link.title',
        category=category,
        publication_date='2020-12-14',
        image=image,
    )


@pytest.mark.django_db
class TestArticlesView:

    @pytest.mark.usefixtures(
        'culture_article', 'newest_culture_article', 'pixels_article', 'newest_pixels_article')
    def test_returns_articles_grouped_by_category(self, client, settings):
        settings.LIST_ARTICLES_BY_CATEGORY = {
            'culture': 2,
            'pixels': 1,
            'interviews': 3,
        }
        response = client.get('/categories/')

        assert response.status_code == 200
        assert response.json() == {
            'culture': [
                {
                    'title': 'Newest Culture Article',
                    'excerpt': 'The excerpt',
                    'media_link': 'http://link.title',
                    'media_title': 'The link title',
                    'publication_date': '2020-12-14',
                    'image_url': 'http://newest-culture-image.url',
                },
                {
                    'title': 'Culture Article',
                    'excerpt': 'The excerpt',
                    'media_link': 'http://link.title',
                    'media_title': 'The link title',
                    'publication_date': '2020-12-13',
                    'image_url': 'http://culture-image.url'
                }
            ],
            'interviews': [],
            'pixels': [
                {
                    'title': 'Newest Pixels Article',
                    'excerpt': 'The excerpt',
                    'media_link': 'http://link.title',
                    'media_title': 'The link title',
                    'publication_date': '2020-12-14',
                    'image_url': 'http://newest-pixels-image.url'
                }
            ]
        }

    @pytest.mark.usefixtures('culture_article', 'pixels_article', 'newest_culture_article')
    def test_returns_articles_for_a_category(self, client):
        response = client.get('/categories/culture/')

        assert response.status_code == 200
        assert response.json() == [
                {
                    'title': 'Newest Culture Article',
                    'excerpt': 'The excerpt',
                    'media_link': 'http://link.title',
                    'media_title': 'The link title',
                    'publication_date': '2020-12-14',
                    'image_url': 'http://newest-culture-image.url',
                },
                {
                    'title': 'Culture Article',
                    'excerpt': 'The excerpt',
                    'media_link': 'http://link.title',
                    'media_title': 'The link title',
                    'publication_date': '2020-12-13',
                    'image_url': 'http://culture-image.url',
                }
            ]
