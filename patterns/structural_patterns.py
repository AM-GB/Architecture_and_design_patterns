from time import time


routes = {}


# structural pattern Decorator
class AddUrl:
    def __init__(self, url):
        '''
        Saving the value of the passed parameter
        '''
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        self.routes[self.url] = cls()


# structural pattern Decorator
class Debug:

    def __init__(self, name):

        self.name = name

    def __call__(self, cls):

        def timeit(method):
            '''
            it is necessary for the decorator of the wrapper class to 
            wrap each method of the decorated class in timeit
            '''
            def timed(*args, **kw):
                timestart = time()
                result = method(*args, **kw)
                timeend = time()
                delta = timeend - timestart

                print(f'debug --> {self.name} выполнялся {delta:2.2f} ms')
                return result

            return timed

        return timeit(cls)
