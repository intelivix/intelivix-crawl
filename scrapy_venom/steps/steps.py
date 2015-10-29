# -*- coding: utf-8 -*-

from functools import update_wrapper
from scrapy.selector import Selector
from scrapy.selector import SelectorList


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

    next_step_cls = None

    @classmethod
    def as_func(cls, **initkwargs):
        def step(response, **kwargs):
            self = cls(**initkwargs)
            selector = Selector(response)
            for item in (self.crawl(selector, **kwargs) or []):
                if item and isinstance(item, Selector):
                    yield self.process_item(item)
                elif item and isinstance(item, SelectorList):
                    for selector in item:
                        yield self.process_item(selector)
                else:
                    yield item

        step.step_class = cls
        step.step_initkwargs = initkwargs
        update_wrapper(step, cls, updated=())
        return step

    def get_next_step(self):
        return self.next_step_cls.as_func()

    def next_step(self, selector, **kwargs):
        next_step = self.get_next_step()
        return next_step(selector.response, **kwargs)

    def response_to_file(self, name, response):
        with open(name, 'wb') as f:
            f.write(response.body)

    def crawl(self, selector):
        raise NotImplementedError(
            u'É necessário implementar o método crawl')
