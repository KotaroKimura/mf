import MySQLdb
import MySQLdb.cursors
import datetime

def con(host, db, user, passwd):
    return MySQLdb.connect(
        host=host,
        db=db,
        user=user,
        passwd=passwd,
        charset='utf8',
        cursorclass=MySQLdb.cursors.DictCursor
    )

def insert_dc_pension_list(con, pension_list):
    _values_list = []
    _cursor      = con.cursor()

    for _item in pension_list:
        _cursor.execute('''
            SELECT
                id
            FROM
                dc
            WHERE
                pension = '{}'
            LIMIT
                1
            ;
        '''.format(_item[0]))

        _row = _cursor.fetchone()
        _id  = _row['id']

        _value_list = []
        _value_list.append(_id)
        _value_list.append(_item[1])
        _value_list.append(_item[2])
        _value_list.append(_item[3])
        _value_list.append(_item[4])

        _values_list.append(_value_list)

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
    """.format(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d'))

    _cursor.executemany(_query, _values_list)
    con.commit()
