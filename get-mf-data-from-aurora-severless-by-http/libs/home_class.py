import datetime as _datetime
import aurora_serverless

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

    def __init__(self, db_params):
        self.__status_code = None
        self.__response    = None

        super(HomeClass, self).__init__(db_params)

    def build(self):
        p_s_d = self.params.get('s_d', None)
        p_t   = self.params.get('t', '6')

        if p_s_d is None:
            s_d = _datetime.datetime.now(_datetime.timezone(_datetime.timedelta(hours=9)))
        else:
            s_d = _datetime.datetime.strptime(p_s_d, '%Y-%m-%d')

        e_d = s_d + _datetime.timedelta(days=int(p_t))

        sql = '''
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
                d_c.dc_id ASC,
                d_c.date ASC
            ;
        '''.format(
            s_d.strftime('%Y-%m-%d'),
            e_d.strftime('%Y-%m-%d'))

        response = aurora_serverless.execute(
            self.db_params.get('mf-db-cluster-arn', None),
            self.db_params.get('mf-db-credentials-secrets-store-arn', None),
            sql)

        labels = []
        for metadata in response['columnMetadata']:
            labels.append(metadata['label'])

        results_tmp = []
        for record in response['records']:
            tmp = {}
            for i, data in enumerate(record):
                tmp[labels[i]] = list(data.values())[0]

            results_tmp.append(tmp)

        results = {}
        for tmp in results_tmp:
            date_key = tmp['d']
            if results.get(date_key) is None:
                results[date_key] = {'pension': [], 'nikkei-access-ranking': []}

            del(tmp['d'])
            results[date_key]['pension'].append(tmp)

        sql = '''
            SELECT
                rank,
                article_title,
                article_url,
                date
            FROM
                nikkei_access_ranking
            WHERE
                date BETWEEN '{}' AND '{}'
            ;
        '''.format(
            s_d.strftime('%Y-%m-%d'),
            e_d.strftime('%Y-%m-%d'))

        response = aurora_serverless.execute(
            self.db_params.get('mf-db-cluster-arn', None),
            self.db_params.get('mf-db-credentials-secrets-store-arn', None),
            sql)

        for record in response['records']:
            tmp = []
            for data in record:
                tmp.append(list(data.values())[0])

            date_key = tmp[3]
            tmp.pop(3)

            if results.get(date_key) is not None:
                results[date_key]['nikkei-access-ranking'].append(tmp)

        self.__status_code = 200
        self.__response = {
            'result': results,
        }
