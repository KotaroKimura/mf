from handlers.error_handler import NotFoundHandler

class WSGIApplication(object):

    def __init__(self, urls, logger=None, **kwargs):
        self.__urls   = urls
        self.__logger = logger

    def __call__(self, environ, start_response):
        _path = environ['PATH_INFO']
        _h    = self.__urls.get(_path, NotFoundHandler())

        _h.__new__
        return _h.entry(environ, start_response, self.__logger)
