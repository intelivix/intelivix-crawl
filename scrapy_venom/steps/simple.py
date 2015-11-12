# -*- coding: utf-8 -*-

import functools
from scrapy import selector as scrapy_selector
from scrapy import items
from scrapy_venom import exceptions
from scrapy_venom.steps import base


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


class ItemStep(base.BaseStep, ExtractItemMixin):

    """
    Generic step to help when extracting items from the response

    To use this class, you need to yield at least one selector
    which will be processed through the methods:

        * extract_item - extracts the selector received
        * clean_item   - clean the extraction from previous method into a dict
        * build_item   - build the item_class with the cleaned_item dict

    Attributes

        item_class: The item class that will be instantiated
        by the build_item method

    """

    item_class = None

    def __init__(self, *args, **kwargs):
        try:
            assert self.item_class, (
                u'You must define an item_class attribute')

            assert isinstance(self.item_class, items.Item), (
                u'The item_class must be a instance of scrapy.Item')

        except AssertionError as e:
            raise exceptions.ArgumentError(e.message)

    @classmethod
    def as_func(cls, spider):

        def step(response, **kwargs):
            self = cls(spider=spider)
            selector = scrapy_selector.Selector(response)
            for item in self.catch_items(selector):
                yield item

        functools.update_wrapper(step, cls, updated=())
        return step

    def catch_items(self, selector):
        for item in self.crawl(selector) or []:
            if item:
                if isinstance(item, scrapy_selector.Selector):
                    yield self.process_item(item)
                elif isinstance(item, scrapy_selector.SelectorList):
                    for selector in item:
                        yield self.process_item(selector)
