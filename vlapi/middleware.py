class LanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.language = request.META['HTTP_X_LANGUAGE']
        response = self.get_response(request)

        return response
