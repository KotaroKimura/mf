from logging import StreamHandler, getLogger, DEBUG

from wsgi.application import WSGIApplication
from handlers.home_handler import HomeHandler

from mysql import ConnectionPool
from config import SETTINGS

_pool = ConnectionPool(
    host=SETTINGS['mysql']['host'],
    db=SETTINGS['mysql']['db'],
    user=SETTINGS['mysql']['user'],
    passwd=SETTINGS['mysql']['passwd'],
    connect_timeout=SETTINGS['mysql']['connect_timeout'],
    env=SETTINGS['env']
)

_logger = getLogger('mf_api')
_logger.setLevel(DEBUG)

_handler = StreamHandler()
_handler.setLevel(DEBUG)

_logger.addHandler(_handler)

_urls = {
    '/': HomeHandler(_pool)
}

application = WSGIApplication(
    _urls,
    _logger
)
