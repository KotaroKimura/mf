# coding: UTF-8
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep
import os

def login(user, password):
    surl = "https://moneyforward.com/sign_in"

    options = Options()
    options.add_argument('-headless')
    driver = webdriver.Firefox(executable_path="/bin/geckodriver", log_path=os.path.devnull, firefox_options=options)

    driver.implicitly_wait(10)
    driver.get(surl)

    # login
    elem = driver.find_element_by_css_selector("._2sZu7ciR.ssoText")
    elem.click()
    elem = driver.find_element_by_css_selector("._2mGdHllU.inputItem")
    elem.clear()
    elem.send_keys(user)

    elem = driver.find_element_by_css_selector(".zNNfb322.submitBtn.homeDomain")
    elem.click()
    elem = driver.find_element_by_css_selector("._1vBc2gjI.inputItem")

    elem.clear()
    elem.send_keys(password)
    elem = driver.find_element_by_css_selector(".zNNfb322.submitBtn.homeDomain")
    elem.click()
    sleep(3)

    return driver

def dc_pension_list(driver):
    result = []
    driver.get("https://moneyforward.com/bs/portfolio")

    portfolio_section = driver.find_elements_by_css_selector(".table.table-bordered.table-pns")[0]
    theader = portfolio_section.find_element_by_tag_name("thead").find_elements_by_tag_name("th")
    tbody   = portfolio_section.find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")
    header  = [t.text for t in theader]

    for item in [ { header[i]: content.text for i, content in enumerate(t.find_elements_by_tag_name("td"))} for t in tbody]:
        if not item['名称'] in ['国民年金', '厚生年金(一般)', '厚生年金(公務員)', '厚生年金(私学共済)']:
            brand_info = []

            brand_info.append(item['名称'])
            brand_info.append(int(item['取得価額'].replace(",", "").replace("円", "")))
            brand_info.append(int(item['現在価値'].replace(",", "").replace("円", "")))
            brand_info.append(int(item['評価損益'].replace(",", "").replace("円", "")))
            brand_info.append(float(item['評価損益率'].replace("%", "")))

            result.append(brand_info)

    return result
