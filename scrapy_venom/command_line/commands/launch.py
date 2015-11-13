# -*- coding: utf-8 -*-

from scrapyd_api import ScrapydAPI


def get_project_name():
    from scrapy.utils.project import get_project_settings
    settings = get_project_settings()
    return settings.attributes.get('PROJECT_NAME').value


def execute(*args):
    args = list(args)
    assert len(args) >= 1, u'É necessário informar pelo menos a spider'

    spider_name = args.pop(0)
    scrapy_url = 'http://localhost:6800'
    if args:
        scrapy_url = args.pop(0)

    scrapyd = ScrapydAPI(scrapy_url)
    scrapyd.schedule(
        get_project_name(), spider_name)


def help():
    return u'launch <spider_name> - Lanca uma spider no Scrapyd'
