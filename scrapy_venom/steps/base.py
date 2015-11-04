# -*- coding: utf-8 -*-

from functools import update_wrapper
from scrapy.selector import Selector
from scrapy.selector import SelectorList
from ..utils import StepContext


__all__ = ['Step']


class ExtractItemMixin(object):

    def extract_item(self, selector):
        return selector.extract()

    def clean_item(self, extraction):
        return extraction or {}

    def build_item(self, cleaned_data):
        return self.item_class(**cleaned_data)

    def process_item(self, selector):
        extraction = self.extract_item(selector)
        cleaned_data = self.clean_item(extraction)
        return self.build_item(cleaned_data or {})


class Step(ExtractItemMixin):

    def __init__(self, spider, context={}):
        self.spider = spider
        self.context = context

    @classmethod
    def as_func(cls, context, spider):

        def step(response, **kwargs):
            self = cls(spider=spider, context=context)
            selector = Selector(response)
            for item in self.catch_items(selector, **context):
                yield item

            yield StepContext(self.get_next_step_context())

        update_wrapper(step, cls, updated=())
        return step

    def catch_items(self, selector, **kwargs):
        for item in self.crawl(selector, **kwargs) or []:
            if item and isinstance(item, Selector):
                yield self.process_item(item)
            elif item and isinstance(item, SelectorList):
                for selector in item:
                    yield self.process_item(selector)

    def response_to_file(self, name, response):
        with open(name, 'wb') as f:
            f.write(response.body)

    def crawl(self, selector):
        raise NotImplementedError(
            u'É necessário implementar o método crawl')

    def get_next_step_context(self):
        return {}
