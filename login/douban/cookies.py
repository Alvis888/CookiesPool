import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class DouBanCookies():
    def __init__(self, username, password, browser):
        self.url = 'https://www.douban.com/'
        self.browser = browser
        self.wait = WebDriverWait(self.browser, 20)
        self.username = username
        self.password = password

    def open(self):
        """
        打开网页输入用户名密码并点击
        :return: None
        """
        self.browser.delete_all_cookies()
        self.browser.get(self.url)
        self.browser.maximize_window()
        self.browser.switch_to.default_content()

        iframe = self.wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@class="login"]//iframe[@frameborder="0"]')))
        self.browser.switch_to.frame(iframe)

        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//li[text()="密码登录"]'))).click()
        username = self.wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="username"]')))
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'password')))
        submit = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//a[text()="登录豆瓣"]')))

        username.clear()
        username.send_keys(self.username)

        password.clear()
        password.send_keys(self.password)

        time.sleep(1)
        submit.click()

    def password_error(self):
        """
        判断是否密码错误
        :return:
        """
        try:
            element = self.browser.find_element_by_xpath('//div[@class="account-form-error"]//span')
            print(element.get_text())
            err_msg = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(
                (By.XPATH, '//div[@class="account-form-error"]//span'))).text
            print(err_msg)
            return False if len(err_msg) > 0 else False
        except TimeoutException:
            return False

    def login_successfully(self):
        """
        判断是否登录成功
        :return:
        """
        try:
            return bool(
                WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH, '//a[text()="说句话"]'))))
        except TimeoutException:
            return False

    def get_cookies(self):
        """
        获取Cookies
        :return:
        """
        return self.browser.get_cookies()

    def main(self):
        """
        破解入口
        :return:
        """
        self.open()
        if self.password_error():
            return {
                'status': 2,
                'content': '用户名或密码错误'
            }
        # 如果不需要验证码直接登录成功
        if self.login_successfully():
            cookies = self.get_cookies()
            return {
                'status': 1,
                'content': cookies
            }

        if self.login_successfully():
            cookies = self.get_cookies()
            return {
                'status': 1,
                'content': cookies
            }
        else:
            return {
                'status': 3,
                'content': '登录失败'
            }


if __name__ == '__main__':
    from selenium import webdriver

    browser = webdriver.Chrome()
    result = DouBanCookies('jksdgf', 'xiesakjdgb', browser).main()
    print(result)
