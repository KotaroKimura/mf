HTTP_STATUS = {
    200: '200 OK',
    404: '404 NotFound',
    405: '405 Method Not Allowed',
    500: '500 Internal Server Error'
}

class RequestHandler(object):

    def __init__(self):
        self.__environ       = None
        self.__contents_type = None
        self.__status_code   = None

    def set_contents_type(self, val):
        self.__contents_type = val

    def set_status_code(self, val):
        self.__status_code = val

    def get(self, *args, **kwargs):
        return "405 Method Not Allowed"

    def entry(self, environ, start_response, logger=None):
        self.__environ = environ
        _http_method   = environ['REQUEST_METHOD']

        try:
            if _http_method == 'GET':
                _contents = self.get()

            else:
                self.set_status_code(405)
                _contents = HTTP_STATUS[405]

        except Exception as e:
            self.set_status_code(500)
            _contents = HTTP_STATUS[500]

        bcontent = bytes(_contents, encoding='UTF-8')
        headers = [
            ('Content-Type', self.__contents_type)
        ]

        start_response(
            HTTP_STATUS.get(self.__status_code, 'UNKNOWN STATUS'),
            headers
        )

        return [bcontent]
