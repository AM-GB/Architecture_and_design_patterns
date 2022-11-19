# get requests
class GetRequests:

    @staticmethod
    def parse_input_data(data: str):
        result = {}
        if data:
            # we divide the parameters by &
            params = data.split('&')
            for item in params:
                # we divide the key and the value by =
                k, v = item.split('=')
                result[k] = v
        return result

    @staticmethod
    def get_request_params(environ):
        # getting the request parameters
        query_string = environ['QUERY_STRING']
        # turning parameters into a dictionary
        request_params = GetRequests.parse_input_data(query_string)
        return request_params


# post requests
class PostRequests:

    @staticmethod
    def parse_input_data(data: str):
        result = {}
        if data:
            # we divide the parameters by &
            params = data.split('&')
            for item in params:
                # we divide the key and the value by =
                k, v = item.split('=')
                result[k] = v
        return result

    @staticmethod
    def get_wsgi_input_data(env) -> bytes:
        # we get the length of the body
        content_length_data = env.get('CONTENT_LENGTH')
        # convert to the int type
        content_length = int(content_length_data) if content_length_data else 0
        # print(content_length)
        # we read the data, if there is any
        # env['wsgi.input'] -> <class '_io.BufferedReader'>
        # starting the reading mode

        data = env['wsgi.input'].read(content_length) \
            if content_length > 0 else b''
        return data

    def parse_wsgi_input_data(self, data: bytes) -> dict:
        result = {}
        if data:
            # decode the data
            data_str = data.decode(encoding='utf-8')
            # print(f'строка после декод - {data_str}')
            # we collect them in the dictionary
            result = self.parse_input_data(data_str)
        return result

    def get_request_params(self, environ):
        # getting the data
        data = self.get_wsgi_input_data(environ)
        # turning data into a dictionary
        data = self.parse_wsgi_input_data(data)
        return data
