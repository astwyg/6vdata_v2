'''
不好搞, 现在搜狗的接口已经很难直接用爬虫爬取公众号链接了, 因此使用selenium驱动浏览器.
'''
import os, time
import selenium.common
from selenium import webdriver

import sys
sys.path.extend([os.path.join(os.path.dirname(__file__), '..'),])
from conf.conf import get_env

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
    c = Content(
        code = stock["code"],
        title = "[{}]{}".format(stock["name"], title),
        info = content,
        url = url[:255]
    )
    server_logger.debug("{} saved.".format(title))
    c.save()

def get_wechat_msg(stock, article=10, sleep=3):
    '''
    
    :param stock: name and code
    :param article: 文章数量
    :param sleep: 等待时间, 秒
    :return: 
    '''
    if get_env() == "debug":
        chrome_options = webdriver.ChromeOptions()
        browser = webdriver.Chrome(os.path.join(os.path.dirname(__file__), 'driver', "chromedriver.exe"))
    else:
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless') # 对于sogou来说, 这样需要输入验证码
        chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument("--disable-extensions")
        # chrome_options.add_argument("--disable-gpu")
        # chrome_options.add_argument("--disable-dev-shm-usage")
        browser = webdriver.Chrome(os.path.join(os.path.dirname(__file__), 'driver', "chromedriver"), chrome_options=chrome_options)
        # browser = webdriver.PhantomJS(os.path.join(os.path.dirname(__file__), 'driver', "phantomjs")) # chrome has kinds of problems under cli only linux
        # browser.set_window_size(1024, 768)

    try:
        browser.get("https://weixin.sogou.com/weixin?type=2&query={}".format(stock["name"]))
        browser.find_element_by_link_text("搜索工具").click()
        browser.find_element_by_link_text("全部时间").click()
        browser.find_element_by_link_text("一天内").click()

        article_links = browser.find_elements_by_xpath("//h3/a")
        for article_link in article_links:
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
                pass
            browser.close()
            windows = browser.window_handles
            browser.switch_to.window(windows[0])

        browser.quit()
    except selenium.common.exceptions.WebDriverException:
        server_logger.warning("chrome failed")
        pass

if __name__ == "__main__":
    all_stocks = get_stocks()
    for stock in all_stocks:
        get_wechat_msg(stock)
