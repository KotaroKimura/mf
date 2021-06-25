# coding: UTF-8
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep
import os

def login(user, password):
    _surl = "https://moneyforward.com/sign_in"

    _options = Options()
    _options.add_argument('-headless')
    _driver = webdriver.Firefox(executable_path="/bin/geckodriver", log_path=os.path.devnull, firefox_options=_options)

    _driver.implicitly_wait(10)
    _driver.get(_surl)

    # login
    _elem = _driver.find_element_by_css_selector("._2sZu7ciR.ssoText")
    _elem.click()
    _elem = _driver.find_element_by_css_selector("._2mGdHllU.inputItem")
    _elem.clear()
    _elem.send_keys(user)

    _elem = _driver.find_element_by_css_selector(".zNNfb322.submitBtn.homeDomain")
    _elem.click()
    _elem = _driver.find_element_by_css_selector("._1vBc2gjI.inputItem")

    _elem.clear()
    _elem.send_keys(password)
    _elem = _driver.find_element_by_css_selector(".zNNfb322.submitBtn.homeDomain")
    _elem.click()
    sleep(3)

    return _driver

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
            _brand_info.append(int(_item['取得価額'].replace(",", "").replace("円", "")))
            _brand_info.append(int(_item['現在価値'].replace(",", "").replace("円", "")))
            _brand_info.append(int(_item['評価損益'].replace(",", "").replace("円", "")))
            _brand_info.append(float(_item['評価損益率'].replace("%", "")))

            _result.append(_brand_info)

    return _result
