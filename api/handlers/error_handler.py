from handlers.request_handler import RequestHandler

class NotFoundHandler(RequestHandler):

    def get(self):
        self.set_status_code(404)
        self.set_contents_type('text/plain')

        return '404 NotFound'
