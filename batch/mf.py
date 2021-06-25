# coding: UTF-8
import sys
import utils
import mysql

from config import SETTINGS

if __name__ == '__main__':
    _user     = SETTINGS['mf']['id']
    _password = SETTINGS['mf']['passwd']
    _driver   = utils.login(_user, _password)
    _list     = utils.dc_pension_list(_driver)

    _mysql_host     = SETTINGS['mysql']['host']
    _mysql_db       = SETTINGS['mysql']['db']
    _mysql_user     = SETTINGS['mysql']['user']
    _mysql_password = SETTINGS['mysql']['passwd']
    _con            = mysql.con(_mysql_host, _mysql_db, _mysql_user, _mysql_password)
    mysql.insert_dc_pension_list(_con, _list)

    _driver.quit()
    sys.exit()
