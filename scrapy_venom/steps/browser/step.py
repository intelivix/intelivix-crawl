# -*- coding: utf-8 -*-

from scrapy_venom import utils
from scrapy_venom.steps import base
from scrapy_venom.steps.browser import manager
from selenium import webdriver


class BrowserStep(base.BaseStep):
    """
    Generic step for using selenium

    """

    initial_url = ''
    payload = {}
    webdriver = webdriver.Firefox

    def _crawl(self, selector):
        initial_url = self.get_initial_url()
        with manager.BrowserManager(webdriver=self.webdriver) as browser:
            browser.get(initial_url)
            browser.set_cookies(self.get_cookies())
            browser.get(initial_url)
            for item in self.crawl(browser):
                yield item

    def get_initial_url(self):
        initial_url = self.initial_url or self.spider.get_initial_url()
        payload = self.get_payload()
        return utils.make_url(url=initial_url, payload=payload)

    def get_payload(self):
        return self.payload

    def get_cookies(self):
        return {}
