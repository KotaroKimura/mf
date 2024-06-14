from selenium import webdriver
from time import sleep

import os

CHROME_DRIVER_PATH     = "/opt/chrome/chromedriver"
HEADLESS_CHROMIUM_PATH = "/opt/chrome/headless-chromium"
ID_LOGIN_URL           = "https://id.moneyforward.com/sign_in"
LOGIN_URL              = "https://moneyforward.com/sign_in"

def login(email, password):

    options = webdriver.ChromeOptions()
    options.binary_location = HEADLESS_CHROMIUM_PATH
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--single-process')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--ignore-certificate-errors")
    options.add_argument(
        f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36')

    driver = webdriver.Chrome(
        executable_path = CHROME_DRIVER_PATH,
        chrome_options = options)

    driver.implicitly_wait(10)
    driver.get(ID_LOGIN_URL)

    elem_idLoginMethod = driver.find_element_by_xpath(
        '/html/body/main/div/div/div[2]/div/section/div/form/div/div/input')
    elem_idLoginMethod.send_keys(email)

    elem_IdLogin = driver.find_element_by_xpath(
        '/html/body/main/div/div/div[2]/div/section/div/form/div/button')
    elem_IdLogin.click()
    sleep(3)

    elem_password = driver.find_element_by_xpath(
        '/html/body/main/div/div/div[2]/div/section/div/form/div/div[2]/input')
    elem_password.send_keys(password)

    elem_IdLogin = driver.find_element_by_xpath(
        '/html/body/main/div/div/div[2]/div/section/div/form/div/button')
    elem_IdLogin.click()
    sleep(3)

    driver.get(LOGIN_URL)

    elem_auth = driver.find_element_by_xpath(
        '/html/body/main/div/div/div[2]/div/section/div/div/form/button')
    elem_auth.click()
    sleep(10)

    return driver

def sync_finance_info(driver):

    driver.get("https://moneyforward.com/accounts")
    sleep(3)

    elem = driver.find_element_by_css_selector(".aggregation-queue-all")
    elem.click()

    sleep(60 * 8)
    driver.refresh()

    return driver

def dc_pension_list(driver):
    _result = []
    driver.get("https://moneyforward.com/bs/portfolio")

    _portfolio_section = driver.find_elements_by_css_selector(".table.table-bordered.table-pns")[0]
    _theader = _portfolio_section.find_element_by_tag_name("thead").find_elements_by_tag_name("th")
    _tbody   = _portfolio_section.find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")
    _header  = [t.text for t in _theader]

    for _item in [ { _header[_i]: _content.text for _i, _content in enumerate(_t.find_elements_by_tag_name("td"))} for _t in _tbody]:
        if not _item['名称'] in ['国民年金', '厚生年金(一般)', '厚生年金(公務員)', '厚生年金(私学共済)']:
            _brand_info = []

            _brand_info.append(_item['名称'])
            _brand_info.append(int(_item['取得価額'].replace(",", "").replace("円", "") or "0"))
            _brand_info.append(int(_item['現在価値'].replace(",", "").replace("円", "") or "0"))
            _brand_info.append(int(_item['評価損益'].replace(",", "").replace("円", "") or "0"))
            _brand_info.append(float(_item['評価損益率'].replace("%", "") or "0"))

            _result.append(_brand_info)

    driver.refresh()

    return _result

def financial_instrument_list(driver):
    _result = []
    driver.get("https://moneyforward.com/bs/portfolio")

    for _portfolio_section in [
        driver.find_elements_by_css_selector(".table.table-bordered.table-mf")[0],
        driver.find_elements_by_css_selector(".table.table-bordered.table-eq")[0],
    ]:
        _theader = _portfolio_section.find_element_by_tag_name("thead").find_elements_by_tag_name("th")
        _tbody   = _portfolio_section.find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")
        _header  = [t.text for t in _theader]

        for _item in [ { _header[_i]: _content.text for _i, _content in enumerate(_t.find_elements_by_tag_name("td"))} for _t in _tbody]:
            if not _item['銘柄名'] in []:
                _brand_info = []

                _brand_info.append(_item['銘柄名'])
                _brand_info.append('株式（現物）' if _item.get('銘柄コード') else '投資信託')
                _brand_info.append(int(_item['保有数'].replace(",", "") or "0"))
                _brand_info.append(int(_item['平均取得単価'].replace(",", "") or "0"))
                _brand_info.append(int((_item.get('現在値') or _item['基準価額']).replace(",", "") or "0"))
                _brand_info.append(int(_item['評価額'].replace(",", "").replace("円", "") or "0"))
                _brand_info.append(int(_item['前日比'].replace(",", "").replace("円", "") or "0"))
                _brand_info.append(int(_item['評価損益'].replace(",", "").replace("円", "") or "0"))
                _brand_info.append(float(_item['評価損益率'].replace("%", "") or "0"))
                _brand_info.append(_item['保有金融機関'])

                _result.append(_brand_info)

    driver.refresh()

    return _result
