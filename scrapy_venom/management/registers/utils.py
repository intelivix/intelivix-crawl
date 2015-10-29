# -*- coding: utf-8 -*-


def get_project_name():
    from scrapy.utils.project import get_project_settings
    settings = get_project_settings()
    return settings.attributes.get('PROJECT_NAME').value
