# -*- coding: utf-8 -*-

from scrapy.spiders.init import InitSpider


__all__ = ['SpiderBase']


class SpiderBase(InitSpider):

    def extractor(self, xpathselector, selector):
        """
        Helper function that extract info from xpathselector object
        using the selector constrains.
        """
        val = xpathselector.xpath(selector).extract()
        return val[0] if val else ''

    def response_to_file(self, name, response):
        with open(name, 'wb') as f:
            f.write(response.body)
