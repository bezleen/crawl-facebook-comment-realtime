import sys
sys.path.insert(0, '.')

import time

import pydash as py_
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

import src.config as Conf


class FacebookStreamingCrawl(object):
    def __init__(self, stream_url):
        self.service = Service(executable_path="chrome_drivers/chromedriver")
        self.driver = webdriver.Chrome(service=self.service)
        self.start_comment_index = 4
        self.stream_url = stream_url
        self.login_url = "https://www.facebook.com/login/"
        self.comment_xpath_not_login = "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[2]/div/div/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div/div/div[{index}]/div/div/div[2]/div/div[1]/div/div/div/div/div[2]/span/div/div"
        self.name_xpath_not_login = "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[2]/div/div/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div/div/div[{index}]/div/div/div[2]/div/div[1]/div/div/div/div/div[1]/span/span"
        self.comment_xpath_after_login = "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[2]/div/div/div[2]/div/div/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div/div/div[{index}]/div/div/div[2]/div/div[1]/div/div/div/div/div[2]/span/div/div"
        self.name_xpath_after_login = "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[2]/div/div/div[2]/div/div/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div/div/div[{index}]/div/div/div[2]/div/div[1]/div/div/div/div/div[1]/span/span"
        self.len_xpath_not_login = "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[2]/div/div/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div/div/div"
        self.len_xpath_after_login = "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[2]/div/div/div[2]/div/div/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div/div/div"
        self.cmt_id_xpath_not_login = "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[2]/div/div/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div/div/div[{index}]/div"
        self.cmt_id_xpath_after_login = "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[2]/div/div/div[2]/div/div/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div/div/div[{index}]/div"

    def login_facebook(self):
        self.redirect_site(self.login_url, delay=3)
        fb_email = Conf.FACEBOOK_EMAIL
        fb_password = Conf.FACEBOOK_PASSWORD
        if not fb_email or not fb_password:
            raise Exception("Missing facebook email or password")
        self.driver.find_element(By.CSS_SELECTOR, "#email").send_keys(fb_email)
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, "#pass").send_keys(fb_password)
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, "#loginbutton").click()
        time.sleep(3)
        return

    def redirect_site(self, url, delay=0):
        self.driver.get(url)
        time.sleep(delay)
        return

    def get_len_of_comment(self, is_login):
        len_xpath = self.len_xpath_not_login if is_login == False else self.len_xpath_after_login
        len_comment_obj = self.driver.find_elements(By.XPATH, len_xpath)
        len_comments = len(len_comment_obj)
        return len_comments

    def save_content(self, content):
        comment_name = py_.get(content, "comment_name")
        comment_content = py_.get(content, "comment_content")
        _print = f"{comment_name} : {comment_content}"
        # print(f"{comment_name} : {comment_content}")
        with open("data/cmt.txt", "a") as f:
            f.write(_print + "\n")
        return

    def exec_crawl(self, retry_on_failure=1, delay_per_comment=2, login=True):
        if login:
            self.login_facebook()
        self.redirect_site(self.stream_url, delay=3)
        retry_count = 0
        index = self.start_comment_index
        last_cmt_id = None
        while True:
            try:
                content, cmt_id = self.get_content_of_the_comment(index, login, last_cmt_id)
                if cmt_id != None:
                    last_cmt_id = cmt_id
                if content:
                    self.save_content(content)
            except:
                if retry_count < retry_on_failure:
                    retry_count += 1
                    continue
            len_comment = self.get_len_of_comment(login)
            if index == len_comment:
                time.sleep(delay_per_comment)
                continue
            index += 1
        return

    def clear_html_in_string(self, string):
        if "<span" in string:
            string = string.split("<span")[0]
        if "<div" in string:
            string = string.split("<div")[0]
        return string

    def get_content_of_the_comment(self, index, is_login, last_cmt_id):
        cmt_id_xpath = self.cmt_id_xpath_not_login if is_login == False else self.cmt_id_xpath_after_login
        cmt_id = self.driver.find_element(By.XPATH, cmt_id_xpath.format(index=index)).get_attribute('id')
        if cmt_id == last_cmt_id:
            return None, None
        comment_xpath = self.comment_xpath_not_login if is_login == False else self.comment_xpath_after_login
        name_xpath = self.name_xpath_not_login if is_login == False else self.name_xpath_after_login
        comment_content = self.driver.find_element(By.XPATH, comment_xpath.format(index=index)).get_attribute('innerHTML')
        comment_name = self.driver.find_element(By.XPATH, name_xpath.format(index=index)).get_attribute('innerHTML')
        comment_content = self.clear_html_in_string(comment_content)
        comment_name = self.clear_html_in_string(comment_name)
        content = {
            "comment_name": comment_name,
            "comment_content": comment_content
        }
        return content, cmt_id
