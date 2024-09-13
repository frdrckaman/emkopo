from django.utils.deprecation import MiddlewareMixin


class CacheRequestBodyMiddleware(MiddlewareMixin):
    @staticmethod
    def process_request(request):
        if request.method in ('POST', 'PUT', 'PATCH'):
            # Read the body only once and cache it
            request.body_cache = request.body
