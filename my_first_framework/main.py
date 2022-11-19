
class PageNotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


class Framework:

    """Class Framework - the basis of the framework"""

    def __init__(self, routes_obj, fronts_obj):
        self.routes_lst = routes_obj
        self.fronts_lst = fronts_obj

    def __call__(self, environ, start_response):
        # we get the address to which the transition was made
        path = environ['PATH_INFO']

        # adding a closing slash
        if not path.endswith('/'):
            path = f'{path}/'

        # finding the right controller
        # working out the page controller pattern
        if path in self.routes_lst:
            view = self.routes_lst[path]
        else:
            view = PageNotFound404()
        request = {}
        # filling the request dictionary with elements
        # all controllers will receive this dictionary
        # working out the front controller pattern
        for front in self.fronts_lst:
            front(request)
        # starting the controller with the transfer of the request object
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]
