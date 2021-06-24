from wsgi.application import WSGIApplication
from handlers.home_handler import HomeHandler

from mysql import ConnectionPool
from config import SETTINGS

pool = ConnectionPool(
    host=SETTINGS['mysql']['host'],
    db=SETTINGS['mysql']['db'],
    user=SETTINGS['mysql']['user'],
    passwd=SETTINGS['mysql']['passwd'],
    connect_timeout=SETTINGS['mysql']['connect_timeout'],
    env=SETTINGS['env']
)

_urls = {
    '/': HomeHandler(pool)
}

application = WSGIApplication(
    _urls
)
