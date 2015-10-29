# -*- coding: utf-8 -*-

import urllib
from scrapy import Request
from ..base import SpiderBase

__all__ = ['SpiderStep', 'URLSpiderStep']


class SpiderStep(SpiderBase):

    initial_url = None
    initial_step_cls = None
    initial_step_kwargs = {}

    def init_request(self):
        url = self.get_initial_url()
        hdrs = {'referer': url}
        return Request(url=url, callback=self.crawl, headers=hdrs)

    def crawl(self, response):
        initial_step = self.get_initial_step()
        for result in initial_step(response):
            yield result

    def get_initial_step(self):
        kwargs = self.get_initial_step_kwargs()
        return self.initial_step_cls.as_func(**kwargs)

    def get_initial_step_kwargs(self):
        return self.initial_step_kwargs

    def get_initial_url(self):
        return self.initial_url


class URLSpiderStep(SpiderStep):

    def prepare_payload(self):
        raise NotImplementedError(
            'É necessário informar o Payload')

    def make_url(self):
        prepare = self.prepare_payload()
        payload = urllib.urlencode(prepare)
        url = self.initial_url + '?' + payload
        return url

    def get_initial_url(self):
        return self.make_url()
