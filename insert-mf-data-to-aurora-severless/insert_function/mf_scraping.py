from selenium import webdriver
from time import sleep

import os

CHROME_DRIVER_PATH     = "/opt/chrome/chromedriver"
HEADLESS_CHROMIUM_PATH = "/opt/chrome/headless-chromium"
URL                    = "https://id.moneyforward.com/sign_in/email"

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
    driver.get(URL)

    elem_loginMethod = driver.find_element_by_xpath(
        '/html/body/main/div/div/div/div/div[1]/section/form/div[2]/div/input')
    elem_loginMethod.send_keys(email)

    elem_login = driver.find_element_by_xpath(
        '/html/body/main/div/div/div/div/div[1]/section/form/div[2]/div/div[3]/input')
    elem_login.click()
    sleep(3)

    elem_password = driver.find_element_by_xpath(
        '/html/body/main/div/div/div/div/div[1]/section/form/div[2]/div/input[2]')
    elem_password.send_keys(password)

    elem_login = driver.find_element_by_xpath(
        '/html/body/main/div/div/div/div/div[1]/section/form/div[2]/div/div[3]/input')
    elem_login.click()
    sleep(3)

    elem_auth = driver.find_element_by_xpath(
        '/html/body/main/div/div/div/div[1]/div/ul/li[3]/a')
    elem_auth.click()
    sleep(3)

    elem_choose_account = driver.find_element_by_xpath(
        '/html/body/main/div/div/div/div/div[1]/section/form/div[2]/div/div[2]/input')
    elem_choose_account.click()
    sleep(3)

    return driver

def sync_finance_info(driver):

    driver.get("https://moneyforward.com/accounts")
    sleep(3)

    elem = driver.find_element_by_css_selector(".aggregation-queue-all")
    elem.click()

    sleep(60 * 2)
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

    return _result
