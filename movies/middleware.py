from django.utils.deprecation import MiddlewareMixin
from .tasks import update_request_counter

class RequestCountMiddleware(MiddlewareMixin):
    def process_request(self, request):
        update_request_counter.delay()

    def process_response(self, request, response):
        return response