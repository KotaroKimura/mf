import ujson as json

from libs.home_class import HomeClass
from handlers.request_handler import RequestHandler

VALID_PARAMS = [
    's_d',
    't'
]

class HomeHandler(RequestHandler):

    def __init__(self, connection_pool):
        super(HomeHandler, self).__init__()
        self.__pool = connection_pool

    def __valid_params(self):
        _valid_params = {}
        for p in VALID_PARAMS:
            if p in self.query_string.keys():
                _valid_params[p] = self.query_string[p]

        return _valid_params

    def get(self):
        _home_cls        = HomeClass(self.__pool)
        _home_cls.params = self.__valid_params()
        _home_cls.build()

        self.status_code   = _home_cls.status_code
        self.contents_type = 'application/json'

        return json.dumps(
            {
                "response": _home_cls.response['result']
            },
            ensure_ascii=False
        )
