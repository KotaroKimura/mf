class BaseClass(object):

    @property
    def db_params(self):
        return self.__db_params

    def __init__(self, db_params=None):
        self.__db_params = db_params
