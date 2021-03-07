from unittest.mock import Mock

from vlapi.middleware import LanguageMiddleware


class TestLanguageMiddleware:

    def test_sets_language_when_present_in_headers(self, rf):
        request = Mock()
        headers = {'HTTP_X_LANGUAGE': 'es'}
        request.META = headers
        request.path = '/admin/'
        middelware = LanguageMiddleware(Mock())

        middelware(request)

        assert request.language == 'es'

    def test_does_not_set_language_when_present_in_headers(self, rf):
        request = Mock()
        request.path = '/admin/'
        request.META = {}
        middelware = LanguageMiddleware(Mock())

        middelware(request)

        assert request.language is None
