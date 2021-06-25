from handlers.request_handler import RequestHandler

class NotFoundHandler(RequestHandler):

    def get(self):
        self.status_code = 404
        return '404 NotFound'
