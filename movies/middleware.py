from django.utils.deprecation import MiddlewareMixin

from .tasks import update_request_counter


class RequestCountMiddleware(MiddlewareMixin):
    def process_request(self, request):
        """ This method is called before the view (and later middleware) is called. """
        # Update the request count in background
        update_request_counter.delay()
