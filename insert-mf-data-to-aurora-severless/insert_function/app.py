import json
import datetime
from time import sleep

import parameter
import mf_scraping
import nikkei_scraping
import aurora_serverless

def lambda_handler(event, context):

    print('START EVENT')
    params = parameter.get(event)

    print('TOUCH AURORA SERVERLESS')
    try:
        aurora_serverless.execute(
            params['mf-db-cluster-arn'],
            params['mf-db-credentials-secrets-store-arn'],
            'SELECT 1;')
    except aurora_serverless.bad_request_exception_class() as e:
        print('catch BadRequestException:', e)
        sleep(60)

    print('GET PENSION DATA FROM MF')
    driver       = mf_scraping.login(params['mf-email'], params['mf-password'])
    driver       = mf_scraping.sync_finance_info(driver)
    pension_list = mf_scraping.dc_pension_list(driver)

    driver.close()
    driver.quit()

    print('INSERT PENSION DATA TO AURORA SERVERLESS')
    values_list   = []
    formated_date = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d')
    for i in pension_list:
        response = aurora_serverless.execute(
            params['mf-db-cluster-arn'],
            params['mf-db-credentials-secrets-store-arn'],
            '''
                SELECT
                    id
                FROM
                    dc
                WHERE
                    pension = '{}'
                LIMIT
                    1
                ;
            '''.format(i[0])
            )
            
        id = response['records'][0][0]['longValue']
        values_list.append(
            '({}, {}, {}, {}, {}, "{}")'.format(
                id,
                i[1],
                i[2],
                i[3],
                i[4],
                formated_date))

    response = aurora_serverless.execute(
        params['mf-db-cluster-arn'],
        params['mf-db-credentials-secrets-store-arn'],
        '''
            INSERT INTO dc_cost (
                dc_id,
                acquisition_cost,
                present_cost,
                valuation_gain_loss,
                valuation_profit_loss_ratio,
                date
            )
            VALUES {}
            ;
        '''.format(', '.join(values_list))
        )

    print('GET NIKKEI ACCESS RANKING')
    ranking = nikkei_scraping.get_access_ranking()

    print('INSERT NIKKEI ACCESS RANKING TO AURORA SERVERLESS')
    values_list = []
    for r in ranking:
        values_list.append(
            '({}, {}, {}, "{}")'.format(
                r[0],
                r[1],
                r[2],
                formated_date))

    response = aurora_serverless.execute(
        params['mf-db-cluster-arn'],
        params['mf-db-credentials-secrets-store-arn'],
        '''
            INSERT INTO nikkei_access_ranking (
                rank,
                article_title,
                article_url,
                date
            )
            VALUES {}
            ;
        '''.format(', '.join(values_list)))

    print('FINISH EVENT')
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": response,
        }),
    }
