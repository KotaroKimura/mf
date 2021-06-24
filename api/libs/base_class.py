class BaseClass(object):

    def __init__(self, pool=None):
        self.__pool = pool

    def execute_query(self, query):
        return self.__pool.get(query)

    def close_cursor(self, cursor):
        return self.__pool.close_cursor(cursor)
