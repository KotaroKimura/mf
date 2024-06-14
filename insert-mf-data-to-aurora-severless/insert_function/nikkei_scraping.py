from selenium import webdriver

CHROME_DRIVER_PATH     = "/opt/chrome/chromedriver"
HEADLESS_CHROMIUM_PATH = "/opt/chrome/headless-chromium"
URL                    = "https://www.nikkei.com/access"

def get_access_ranking():

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

    access_ranking_list = driver.find_elements_by_xpath(
        '/html/body/div[8]/div/div/div/div[3]/div[1]/ul/li')

    count   = 1
    results = []
    for element in access_ranking_list:
        news = element.find_element_by_xpath('h3/span[2]/span[1]/a')
        results.append([
            count,
            news.text,
            news.get_attribute("href")
        ])
        count += 1

    driver.close()
    driver.quit()

    return results
