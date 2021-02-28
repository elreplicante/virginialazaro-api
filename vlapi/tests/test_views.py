import pytest

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
        publication_date='2020-12-14',
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
                },
                {
                    'title': 'Artículo de cultura',
                    'excerpt': 'El extracto',
                    'media_link': 'http://link.titulo',
                    'media_title': 'El título del link',
                    'publication_date': '2020-12-13',
                    'image_url': 'http://culture-image.url'
                }
            ],
            'interviews': [],
            'pixels': [
                {
                    'title': 'Nuevo Artículo de Pixels',
                    'excerpt': 'El extracto',
                    'media_link': 'http://link.titulo',
                    'media_title': 'El título del link',
                    'publication_date': '2020-12-14',
                    'image_url': 'http://newest-pixels-image.url'
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
                },
                {
                    'title': 'Artículo de cultura',
                    'excerpt': 'El extracto',
                    'media_link': 'http://link.titulo',
                    'media_title': 'El título del link',
                    'publication_date': '2020-12-13',
                    'image_url': 'http://culture-image.url',
                }
            ]

