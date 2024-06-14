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

    print('GET PENSION AND FINANCIAL INSTRUMENT DATA FROM MF')
    driver                    = mf_scraping.login(params['mf-email'], params['mf-password'])
    driver                    = mf_scraping.sync_finance_info(driver)
    pension_list              = mf_scraping.dc_pension_list(driver)
    financial_instrument_list = mf_scraping.financial_instrument_list(driver)

    driver.close()
    driver.quit()

    print('TOUCH AURORA SERVERLESS')
    try:
        aurora_serverless.execute(
            params['mf-db-cluster-arn'],
            params['mf-db-credentials-secrets-store-arn'],
            'SELECT 1;')
    except aurora_serverless.bad_request_exception_class() as e:
        print('catch BadRequestException:', e)
        sleep(60)

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

    if len(values_list) == 0:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "pension data is empty.",
            }),
        }

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

    print('INSERT FINANCIAL INSTRUMENT DATA TO AURORA SERVERLESS')
    values_list = []
    for i in financial_instrument_list:
        response = aurora_serverless.execute(
            params['mf-db-cluster-arn'],
            params['mf-db-credentials-secrets-store-arn'],
            '''
                SELECT
                    id
                FROM
                    financial_instrument
                WHERE
                    name = '{}'
                LIMIT
                    1
                ;
            '''.format(i[0])
            )

        id = response['records'][0][0]['longValue']
        values_list.append(
            '({}, "{}", {}, {}, {}, {}, {}, {}, {}, "{}", "{}")'.format(
                id,
                '投資信託',
                i[1],
                i[2],
                i[3],
                i[4],
                i[5],
                i[6],
                i[7],
                i[8],
                formated_date))

    if len(values_list) == 0:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "financial instrument data is empty.",
            }),
        }

    response = aurora_serverless.execute(
        params['mf-db-cluster-arn'],
        params['mf-db-credentials-secrets-store-arn'],
        '''
            INSERT INTO financial_instrument_cost (
                financial_instrument_id,
                financial_instrument_type,
                unit,
                average_acquisition_cost,
                base_cost,
                valuation,
                one_day_difference,
                valuation_gain_loss,
                valuation_profit_loss_ratio,
                financial_institution,
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
            '({}, "{}", "{}", "{}")'.format(
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
