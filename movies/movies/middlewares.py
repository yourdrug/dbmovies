from django.http import HttpResponseRedirect


class BlockApiMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request, *args, **kwargs):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        # block_list = ['/movie_short/', '/admin/']
        block_list = []
        if request.path in block_list:
            return HttpResponseRedirect('http://localhost:8080/')
        else:
            response = self.get_response(request, *args, **kwargs)
            return response
        # Code to be executed for each request/response after
        # the view is called.

