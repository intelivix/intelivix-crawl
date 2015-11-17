# -*- coding: utf-8 -*-

from scrapy_venom import utils
from scrapy_venom.steps import base
from scrapy_venom.steps.browser import manager
from pyvirtualdisplay.smartdisplay import SmartDisplay


class BrowserStep(base.BaseStep):
    """
    Generic step for using selenium

    """

    initial_url = ''
    payload = {}
    use_smartdisplay = True

    def _crawl(self, selector):
        initial_url = self.get_initial_url()

        if self.use_smartdisplay:
            with SmartDisplay(visible=0, bgcolor='black'):
                with manager.BrowserManager() as browser:
                    browser.get(initial_url)
                    browser.set_cookies(self.get_cookies())
                    browser.get(initial_url)
                    for item in self.crawl(browser):
                        yield item
        else:
            with manager.BrowserManager() as browser:
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
