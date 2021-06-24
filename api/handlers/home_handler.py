import ujson as json

from libs.home_class import HomeClass
from handlers.request_handler import RequestHandler

class HomeHandler(RequestHandler):

    def __init__(self, connection_pool):
        super(HomeHandler, self).__init__()
        self.__pool = connection_pool

    def get(self):
        _home_cls = HomeClass(self.__pool)
        _home_cls.build()

        self.set_status_code(_home_cls.status_code)
        self.set_contents_type('application/json')

        return json.dumps(
            {
                "response": _home_cls.response['result']
            },
            ensure_ascii=False
        )
