import traceback
from urllib.parse import parse_qs

HTTP_STATUS = {
    200: '200 OK',
    404: '404 NotFound',
    405: '405 Method Not Allowed',
    500: '500 Internal Server Error'
}

class RequestHandler(object):

    @property
    def contents_type(self):
        return self.__contents_type

    @property
    def status_code(self):
        return self.__status_code

    @property
    def query_string(self):
        return self.__query_strings

    @contents_type.setter
    def contents_type(self, v):
        self.__contents_type = v

    @status_code.setter
    def status_code(self, v):
        self.__status_code = v

    def __init__(self):
        self.__environ       = None
        self.__status_code   = None
        self.__query_strings = None
        self.__contents_type = 'text/plain'

    def __params_init(self):
        self.__query_strings = {}

        _params = self.__environ.get('QUERY_STRING', None)
        for _k, _v in parse_qs(_params).items():
            self.__query_strings[_k] = _v[0]

    def get(self, *args, **kwargs):
        return "405 Method Not Allowed"

    def entry(self, environ, start_response, logger=None):
        self.__environ = environ
        _http_method   = environ['REQUEST_METHOD']

        self.__params_init()

        try:
            if _http_method == 'GET':
                _contents = self.get()

            else:
                self.status_code = 405
                _contents = HTTP_STATUS[405]

        except Exception as e:
            self.status_code = 500
            _contents = HTTP_STATUS[500]

            if logger:
                logger.error(traceback.format_exc())

        _bcontent = bytes(_contents, encoding='UTF-8')
        _headers  = [
            ('Content-Type', self.contents_type)
        ]

        start_response(
            HTTP_STATUS.get(self.status_code, 'UNKNOWN STATUS'),
            _headers
        )

        return [_bcontent]
