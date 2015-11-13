
import logging
import importlib
from scrapy import signals

logger = logging.getLogger(__name__)


def import_handler(func_path):
    function = func_path.split('.')[-1]
    module = '.'.join(func_path.split('.')[:-1])
    module = importlib.import_module(module)
    return getattr(module, function)


class SignalHandler(object):

    def __init__(self, crawler):
        self.crawler = crawler

    @classmethod
    def from_crawler(cls, crawler):
        # get the handlers of the spider events
        handlers = crawler.settings.get('SIGNAL_HANDLERS')

        ext = cls(crawler)

        ext.spider_opened = import_handler(handlers['opened'])
        ext.spider_closed = import_handler(handlers['closed'])
        ext.spider_error = import_handler(handlers['error'])

        # connect the extension object to signals
        crawler.signals.connect(
            ext.spider_opened, signal=signals.spider_opened)

        crawler.signals.connect(
            ext.spider_closed, signal=signals.spider_closed)

        crawler.signals.connect(
            ext.spider_error, signal=signals.spider_error)

        return ext
