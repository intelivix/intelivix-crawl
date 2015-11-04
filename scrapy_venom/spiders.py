# -*- coding: utf-8 -*-

import urllib
from scrapy import Request
from scrapy.spiders.init import InitSpider
from .utils import StepContext


__all__ = ['SpiderStep']


class StepMixin(object):

    steps = []

    def crawl(self, response):
        next_step_context = {}
        steps = list(self.steps)
        while steps:
            step = steps.pop(0)
            func = step.as_func(
                spider=self,
                context=next_step_context)

            for item in func(response):
                if isinstance(item, StepContext):
                    next_step_context = item
                else:
                    yield item


class RequestMixin(object):

    @property
    def initial_url(self):
        return ''

    @property
    def payload(self):
        return {}

    def get_initial_url(self):
        if not self.payload:
            return self.initial_url

        payload = urllib.urlencode(self.payload)
        url = self.initial_url + '?' + payload
        return url


class SpiderStep(
        StepMixin, RequestMixin, InitSpider):

    def init_request(self):
        url = self.get_initial_url()
        hdrs = {'referer': url}
        return Request(url=url, callback=self.crawl, headers=hdrs)
