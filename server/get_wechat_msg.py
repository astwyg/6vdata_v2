'''
不好搞, 现在搜狗的接口已经很难直接用爬虫爬取公众号链接了, 因此使用selenium驱动浏览器.
'''
import os, time
import selenium
from selenium import webdriver

import sys
sys.path.extend([os.path.join(os.path.dirname(__file__), '..'),])
from conf.conf import get_env

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
        url = url
    )
    server_logger.debug("{} saved.".format(title))
    print("success")
    c.save()

def get_wechat_msg(stock, article=10, sleep=3):
    '''
    
    :param stock: name and code
    :param article: 文章数量
    :param sleep: 等待时间, 秒
    :return: 
    '''
    if get_env() == "debug":
        browser = webdriver.Chrome(os.path.join(os.path.dirname(__file__), 'driver', "chromedriver.exe"))
    else:
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        browser = webdriver.Chrome(os.path.join(os.path.dirname(__file__), 'driver', "chromedriver"), chrome_options=chrome_options)

    browser.get("https://weixin.sogou.com/weixin?type=2&query={}".format(stock["name"]))
    print(browser.page_source.encode("utf-8"))
    browser.find_element_by_link_text("搜索工具").click()
    browser.find_element_by_link_text("全部时间").click()
    browser.find_element_by_link_text("一天内").click()

    article_links = browser.find_elements_by_xpath("//h3/a")
    for article_link in article_links:
        article_link.click()
        windows = browser.window_handles
        browser.switch_to.window(windows[-1])
        time.sleep(sleep) # wait js finish
        title = browser.find_element_by_xpath("//h2[@id='activity-name']").text
        content = browser.find_element_by_xpath("//div[@id='js_content']").get_attribute('innerHTML')
        save_wechat_msg(stock, title, content, browser.current_url)
        browser.close()
        windows = browser.window_handles
        browser.switch_to.window(windows[0])

    browser.quit()

if __name__ == "__main__":
    get_wechat_msg({
        "name":"深科技",
        "code":"000021"
    })
