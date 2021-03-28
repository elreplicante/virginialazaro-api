from unittest.mock import patch

import pytest
from django.db import connections

from vlapi.models import Article, Category, Image, Language


@pytest.fixture
def spanish():
    return Language.objects.get(name='es')


@pytest.fixture
def english():
    return Language.objects.get(name='en')


@pytest.fixture
def spanish_culture_article(spanish):
    image = Image.objects.create(url='http://culture-image.url')
    category = Category.objects.get(name='culture')
    return Article.objects.create(
        language=spanish,
        title='Artículo de cultura',
        excerpt='El extracto',
        media_title='El título del link',
        media_link='http://link.titulo',
        category=category,
        publication_date='2020-12-13',
        image=image,
    )


@pytest.fixture
def english_culture_article(english):
    image = Image.objects.create(url='http://culture-image.url')
    category = Category.objects.get(name='culture')
    return Article.objects.create(
        language=english,
        title='Culture article',
        excerpt='The excerpt',
        media_title='The link title',
        media_link='http://link.title',
        category=category,
        publication_date='2020-12-13',
        image=image,
    )


@pytest.fixture
def newest_spanish_culture_article(spanish):
    image = Image.objects.create(url='http://newest-culture-image.url')
    category = Category.objects.get(name='culture')
    return Article.objects.create(
        language=spanish,
        title='Nuevo Artículo de cultura',
        excerpt='El extracto',
        media_title='El título del link',
        media_link='http://link.titulo',
        category=category,
        publication_date='2020-12-14',
        image=image,
    )


@pytest.fixture
def spanish_pixels_article(spanish):
    category = Category.objects.get(name='pixels')
    image = Image.objects.create(url='http://pixels-image.url')
    return Article.objects.create(
        language=spanish,
        title='Artículo de pixels',
        excerpt='El extracto',
        media_title='El título del link',
        media_link='http://link.titulo',
        category=category,
        publication_date='2020-12-13',
        image=image,
    )


@pytest.fixture
def newest_spanish_pixels_article(spanish):
    image = Image.objects.create(url='http://newest-pixels-image.url')
    category = Category.objects.get(name='pixels')
    return Article.objects.create(
        language=spanish,
        title='Nuevo Artículo de Pixels',
        excerpt='El extracto',
        media_title='El título del link',
        media_link='http://link.titulo',
        category=category,
        publication_date='2020-12-15',
        image=image,
    )


@pytest.mark.django_db
class TestArticlesView:

    @pytest.mark.usefixtures(
        'english_culture_article',
        'spanish_culture_article',
        'newest_spanish_culture_article',
        'spanish_pixels_article',
        'newest_spanish_pixels_article'
    )
    def test_returns_articles_grouped_by_category(self, client, settings, django_assert_num_queries):
        settings.LIST_ARTICLES_BY_CATEGORY = {
            'culture': 2,
            'pixels': 1,
            'interviews': 3,
        }
        with django_assert_num_queries(4):
            headers = {'HTTP_X_LANGUAGE': 'es'}
            response = client.get('/categories/', **headers)

        assert response.status_code == 200
        assert response.json() == {
            'culture': [
                {
                    'title': 'Nuevo Artículo de cultura',
                    'excerpt': 'El extracto',
                    'media_link': 'http://link.titulo',
                    'media_title': 'El título del link',
                    'publication_date': '2020-12-14',
                    'image_url': 'http://newest-culture-image.url',
                    'category': 'culture',
                },
                {
                    'title': 'Artículo de cultura',
                    'excerpt': 'El extracto',
                    'media_link': 'http://link.titulo',
                    'media_title': 'El título del link',
                    'publication_date': '2020-12-13',
                    'image_url': 'http://culture-image.url',
                    'category': 'culture',
                }
            ],
            'interviews': [],
            'pixels': [
                {
                    'title': 'Nuevo Artículo de Pixels',
                    'excerpt': 'El extracto',
                    'media_link': 'http://link.titulo',
                    'media_title': 'El título del link',
                    'publication_date': '2020-12-15',
                    'image_url': 'http://newest-pixels-image.url',
                    'category': 'pixels',
                }
            ]
        }

    @pytest.mark.usefixtures(
        'english_culture_article',
        'spanish_culture_article',
        'spanish_pixels_article',
        'newest_spanish_culture_article'
    )
    def test_returns_articles_for_a_category(self, client, django_assert_num_queries):
        with django_assert_num_queries(2):
            headers = {'HTTP_X_LANGUAGE': 'es'}
            response = client.get('/categories/culture/', **headers)

        assert response.status_code == 200
        assert response.json() == [
                {
                    'title': 'Nuevo Artículo de cultura',
                    'excerpt': 'El extracto',
                    'media_link': 'http://link.titulo',
                    'media_title': 'El título del link',
                    'publication_date': '2020-12-14',
                    'image_url': 'http://newest-culture-image.url',
                    'category': 'culture',
                },
                {
                    'title': 'Artículo de cultura',
                    'excerpt': 'El extracto',
                    'media_link': 'http://link.titulo',
                    'media_title': 'El título del link',
                    'publication_date': '2020-12-13',
                    'image_url': 'http://culture-image.url',
                    'category': 'culture',
                }
            ]


@pytest.mark.django_db
class TestCategoryView:

    @pytest.mark.usefixtures(
        'english_culture_article',
        'spanish_culture_article',
        'spanish_pixels_article',
        'newest_spanish_culture_article',
        'newest_spanish_pixels_article'
    )
    def test_returns_all_articles_ordered_by_date(self, client, django_assert_num_queries):
        headers = {'HTTP_X_LANGUAGE': 'es'}
        with django_assert_num_queries(1):
            response = client.get('/articles/', **headers)

        assert response.status_code == 200
        assert response.json() == [
            {
                'title': 'Nuevo Artículo de Pixels',
                'excerpt': 'El extracto',
                'media_link': 'http://link.titulo',
                'media_title': 'El título del link',
                'publication_date': '2020-12-15',
                'image_url': 'http://newest-pixels-image.url',
                'category': 'pixels',
            },
            {
                'title': 'Nuevo Artículo de cultura',
                'excerpt': 'El extracto',
                'media_link': 'http://link.titulo',
                'media_title': 'El título del link',
                'publication_date': '2020-12-14',
                'image_url': 'http://newest-culture-image.url',
                'category': 'culture',
            },
            {
                'title': 'Artículo de cultura',
                'excerpt': 'El extracto',
                'media_link': 'http://link.titulo',
                'media_title': 'El título del link',
                'publication_date': '2020-12-13',
                'image_url': 'http://culture-image.url',
                'category': 'culture',
            },
            {
                'title': 'Artículo de pixels',
                'excerpt': 'El extracto',
                'media_link': 'http://link.titulo',
                'media_title': 'El título del link',
                'publication_date': '2020-12-13',
                'image_url': 'http://pixels-image.url',
                'category': 'pixels',
            },
        ]


@pytest.mark.django_db
class TestSystemHealth:

    @pytest.fixture
    def default_db(self):
        with patch.object(connections['default'], 'is_usable', return_value=True) as mock:
            yield mock

    @pytest.fixture
    def default_db_error(self):
        with patch.object(connections['default'], 'is_usable', return_value=False) as mock:
            yield mock

    @pytest.mark.usefixtures('default_db')
    def test_returns_200_with_ok_status(self, client):
        res = client.get('/health/')

        assert res.status_code == 200

    @pytest.mark.usefixtures('default_db_error')
    def test_returns_teapot_status_and_ko_when_database_check_is_unsuccessful(self, client):
        response = client.get('/health/')

        assert response.status_code == 418
        assert response.json() == {
            'status': 'ko',
        }
