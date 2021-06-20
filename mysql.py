import MySQLdb
import MySQLdb.cursors
from datetime import datetime

def con(host, db, user, passwd):
    return MySQLdb.connect(
        host=host,
        db=db,
        user=user,
        passwd=passwd,
        charset='utf8',
        cursorclass=MySQLdb.cursors.DictCursor
    )

def insert_dc_pension_list(con, _list):
    values_list = []
    cursor      = con.cursor()

    for item in _list:
        cursor.execute('''
            SELECT
                id
            FROM
                dc
            WHERE
                pension = '{}'
            LIMIT
                1
            ;
        '''.format(item[0]))

        _row = cursor.fetchone()
        _id  = _row['id']

        value_list = []
        value_list.append(_id)
        value_list.append(item[1])
        value_list.append(item[2])
        value_list.append(item[3])
        value_list.append(item[4])

        values_list.append(value_list)

    _query = """
        INSERT INTO dc_cost (
            dc_id,
            acquisition_cost,
            present_cost,
            valuation_gain_loss,
            valuation_profit_loss_ratio,
            date
        )
        VALUES (
            %s,
            %s,
            %s,
            %s,
            %s,
            '{}'
        );
    """.format(datetime.now().strftime('%Y-%m-%d'))

    cursor.executemany(_query, values_list)
    con.commit()
