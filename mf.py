# coding: UTF-8
import sys
import os
import utils
import mysql

if __name__ == '__main__':
    user     = os.environ["MF_ID"]
    password = os.environ["MF_PASSWORD"]
    driver   = utils.login(user, password)
    _list    = utils.dc_pension_list(driver)

    mysql_host     = os.environ["MYSQL_HOST"]
    mysql_db       = os.environ["MYSQL_DB"]
    mysql_user     = os.environ["MYSQL_USER"]
    mysql_password = os.environ["MYSQL_PASSWORD"]
    con            = mysql.con(mysql_host, mysql_db, mysql_user, mysql_password)
    mysql.insert_dc_pension_list(con, _list)

    driver.quit()
    sys.exit()
