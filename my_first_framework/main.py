from quopri import decodestring
from my_first_framework.request_handler import PostRequests, GetRequests

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
        
        request = {}
        # Getting all the request data
        request_method = environ['REQUEST_METHOD']
        request['request_method'] = request_method

        if request_method == 'POST':
            data = PostRequests().get_request_params(environ)
            request['data'] = Framework.decode_value(data)
            print(f"Нам пришёл post-запрос: {request['data']}")
        if request_method == 'GET':
            params = GetRequests().get_request_params(environ)
            request['params'] = Framework.decode_value(params)
            print(f"Нам пришли GET-параметры: {request['params']}")
            
        # finding the right controller
        # working out the page controller pattern
        if path in self.routes_lst:
            view = self.routes_lst[path]
        else:
            view = PageNotFound404()
        
        # filling the request dictionary with elements
        # all controllers will receive this dictionary
        # working out the front controller pattern
        for front in self.fronts_lst:
            front(request)
        # starting the controller with the transfer of the request object
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    
    @staticmethod
    def decode_value(data):
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = decodestring(val).decode('UTF-8')
            new_data[k] = val_decode_str
        return new_data

if __name__ == '__main__':
    print('main')