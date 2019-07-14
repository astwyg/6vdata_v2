'''
不好搞, 现在搜狗的接口已经很难直接用爬虫爬取公众号链接了, 因此使用selenium驱动浏览器.
'''
import os, time, traceback, random, datetime
import selenium.common
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import sys
sys.path.extend([os.path.join(os.path.dirname(__file__), '..'),])
from conf.conf import get_env

if get_env() != "debug":
    import pymysql
    pymysql.install_as_MySQLdb()

from server.stocks import get_stocks

# load django env
import sys
from django.core.wsgi import get_wsgi_application
sys.path.extend([os.path.join(os.path.dirname(__file__), '..', "webserver"),])
os.environ.setdefault("DJANGO_SETTINGS_MODULE","webserver.settings")
application = get_wsgi_application()
from wechat_msg.models import Content

# load logger
from conf.log import server_logger


def save_wechat_msg(stock, title, content, url):
    if get_env() == "debug":
        server_logger.info("{} fetched".format(title))
    else:
        c = Content(
            code = stock["code"],
            title = "[{}]{}".format(stock["name"], title),
            info = content,
            url = url[:255]
        )
        server_logger.debug("{} saved.".format(title))
        c.save()

browser = None # 尝试一下不换浏览器
if get_env() == "debug":
    browser = webdriver.Chrome(os.path.join(os.path.dirname(__file__), 'driver', "chromedriver.exe"))
else:
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless') # 对于sogou来说, 这样需要输入验证码
    chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument("--disable-extensions")
    # chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument("--disable-dev-shm-usage")

    caps = DesiredCapabilities.CHROME
    caps['loggingPrefs'] = {'performance': 'ALL'}

    browser = webdriver.Chrome(os.path.join(os.path.dirname(__file__), 'driver', "chromedriver1")
                               , chrome_options=chrome_options
                               , desired_capabilities=caps)

    # browser.delete_all_cookies() # 2019-7-14 17:05:46 删cookies不好用了
    browser.get("https://weixin.sogou.com/")
    time.sleep(1)
    cookies = {
        #'ABTEST': '7|1558860870|v1',
        #'IPLOC': 'CN8100',
        #'SUID' : 'BC01DE9A771A910A000000005CEA5447',
        #'PHPSESSID' : 'kg0lsvv09l2rjolj09o0mu9pa5',
        #'SUV':'003F33BE9ADE01BC5CEA544765246715',
        'SNUID':'1AC04A67771A910A000000005D2AEFBF',  # 已明确, 这个id是最重要的, 判断用户是否输入过验证码
        'successCount':'1|{}'.format(datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")),
        'weixinIndexVisited':'1',
        'seccodeRight':'success'
        #'JSESSIONID':'aaa-gk1GKzZ51dNVN9fRw'
    }
    for name, value in cookies.items():
        browser.add_cookie({
            'name': name,
            'value': value
        })



def get_wechat_msg(stock, article=1, sleep=30):
    '''
    
    :param stock: name and code
    :param article: 文章数量
    :param sleep: 等待时间, 秒
    :return: 
    '''

    try:
        browser.get("https://weixin.sogou.com/weixin?type=2&query={}".format(stock["name"]))
        browser.find_element_by_link_text("搜索工具").click()
        browser.find_element_by_link_text("全部时间").click()
        browser.find_element_by_link_text("一天内").click()

        article_links = browser.find_elements_by_xpath("//h3/a")
        for article_link in article_links[:article]:
            article_link.click()
            windows = browser.window_handles
            browser.switch_to.window(windows[-1])
            time.sleep(sleep) # wait js finish
            try:
                title = browser.find_element_by_xpath("//h2[@id='activity-name']").text
                content = browser.find_element_by_xpath("//div[@id='js_content']").get_attribute('innerHTML')
                save_wechat_msg(stock, title, content, browser.current_url)
            except selenium.common.exceptions.NoSuchElementException:
                server_logger.warning("{} met a NoSuchElementException")
                server_logger.error(traceback.format_exc())
                server_logger.info(browser.page_source)
                server_logger.debug("browser log")
                server_logger.debug(browser.get_log('browser'))
                pass
            browser.close()
            windows = browser.window_handles
            browser.switch_to.window(windows[0])

        # browser.quit()
    except selenium.common.exceptions.WebDriverException:
        server_logger.warning("chrome failed")
        server_logger.error(traceback.format_exc())
        server_logger.info(browser.page_source)
        server_logger.debug("browser log")
        server_logger.debug(browser.get_log('performance'))
        pass

if __name__ == "__main__":
    all_stocks = get_stocks()
    for stock in all_stocks:
        try:
            # if get_env() == "product":
            #     os.system("ps -ef | grep chrom | awk '{print $2}' | xargs kill -9 ")
            get_wechat_msg(stock)
        except Exception:
            server_logger.warning("unknown error")
            server_logger.error(traceback.format_exc())
