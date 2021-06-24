# coding: UTF-8
import sys
import utils
import mysql

from config import SETTINGS

if __name__ == '__main__':
    user     = SETTINGS['mf']['id']
    password = SETTINGS['mf']['passwd']
    driver   = utils.login(user, password)
    _list    = utils.dc_pension_list(driver)

    mysql_host     = SETTINGS['mysql']['host']
    mysql_db       = SETTINGS['mysql']['db']
    mysql_user     = SETTINGS['mysql']['user']
    mysql_password = SETTINGS['mysql']['passwd']
    con            = mysql.con(mysql_host, mysql_db, mysql_user, mysql_password)
    mysql.insert_dc_pension_list(con, _list)

    driver.quit()
    sys.exit()
