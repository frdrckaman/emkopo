from django.utils.deprecation import MiddlewareMixin


class CacheRequestBodyMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.method in ('POST', 'PUT', 'PATCH'):
            # Read the body only once
            request.body_cache = request.body
