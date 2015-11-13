# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy_venom.admin import collections


def closed(spider, reason):
    print(spider.name + ' Closed!!')


def opened(spider):
    import ipdb; ipdb.set_trace()
    spider.collection_id = 1
    # spider = collections.Spider()
    # spider.name = spider.name
    # spider.started_at = datetime.now()
    # spider.state = 'in_progress'
    # spider.save()
    print(spider.name + ' Opened!!')


def error(failure, response, spider):
    print('oh no!, error')
    import ipdb; ipdb.set_trace()


dispatcher.connect(closed, signals.spider_closed)
dispatcher.connect(opened, signals.spider_opened)
dispatcher.connect(error, signals.spider_error)
