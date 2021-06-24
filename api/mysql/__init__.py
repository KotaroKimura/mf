import MySQLdb
import MySQLdb.cursors

class ConnectionPool(object):

    def __init__(self, host, db, user, passwd, connect_timeout=None, env=None):
        if env is 'pi':
            self.__pool = MySQLdb.connect(
                host=host,
                db=db,
                user=user,
                passwd=passwd,
                connect_timeout=connect_timeout,
                charset='utf8',
                cursorclass=MySQLdb.cursors.DictCursor
            )
        else:
            self.__pool = None

    def get(self, query):
        if self.__pool is None:
            print(query)
            return None
        else:
            cursor = self.__pool.cursor()
            cursor.execute(query)
            return cursor

    def close_cursor(self, cursor):
        cursor.close()
        self.__pool.commit()
