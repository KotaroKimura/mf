import datetime as _datetime
from libs.base_class import BaseClass

class HomeClass(BaseClass):

    @property
    def status_code(self):
        return self.__status_code

    @property
    def response(self):
        return self.__response

    @property
    def params(self):
        return self.__params

    @params.setter
    def params(self, v):
        self.__params = v

    def __init__(self, pool):
        self.__status_code = None
        self.__response    = None

        super(HomeClass, self).__init__(pool)

    def build(self):
        _p_s_d = self.params.get('s_d', None)
        _p_t   = self.params.get('t', '6')

        if _p_s_d is None:
            _s_d = _datetime.datetime.now()
        else:
            _s_d = _datetime.datetime.strptime(_p_s_d, '%Y-%m-%d')

        _e_d = _s_d - _datetime.timedelta(days=int(_p_t))

        _cursor = self.execute_query('''
            SELECT
                d.pension AS p,
                d_c.acquisition_cost AS ac,
                d_c.present_cost AS pc,
                d_c.valuation_gain_loss AS vgl,
                d_c.valuation_profit_loss_ratio AS vplr,
                d_c.date AS d
            FROM
                dc AS d
            INNER JOIN
                dc_cost AS d_c
            ON
                d.id = d_c.dc_id
            WHERE
                d_c.date BETWEEN '{}' AND '{}'
            ORDER BY
                d.id ASC,
                d_c.date ASC
            ;
        '''.format(
            _e_d.strftime('%Y-%m-%d'),
            _s_d.strftime('%Y-%m-%d')
        ))

        self.__status_code = 200
        if _cursor is None:
            self.__response = {
                'result': 'None',
            }
        else:
            _records = []
            for _ele in _cursor.fetchall():
                _records.append({
                    "pension": _ele["p"],
                    "acquisition_cost": _ele["ac"],
                    "present_cost": _ele["pc"],
                    "valuation_gain_loss": _ele["vgl"],
                    "valuation_profit_loss_ratio": _ele["vplr"],
                    "date": _ele["d"],
                })

            self.close_cursor(_cursor)
            self.__response = {
                'result': _records,
            }
