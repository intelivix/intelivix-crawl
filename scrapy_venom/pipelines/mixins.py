# -*- coding: utf-8 -*-


__all__ = ['PipelineAllowedMixin', 'ItemAllowedMixin']


class PipelineAllowedMixin(object):

    def get_pipeline_allowed(self):
        pipeline_name = self.__class__.__name__
        pipeline_app = self.__class__.__module__.split('.')[-2]
        return '{}.{}'.format(pipeline_app, pipeline_name)

    def pipeline_is_allowed(self, spider):
        pipeline_allowed = self.get_pipeline_allowed()
        spider_pipelines = getattr(spider, 'pipelines_allowed', [])
        return pipeline_allowed in spider_pipelines


class ItemAllowedMixin(object):

    items_allowed = []

    def item_is_allowed(self, item):
        for allowed in self.items_allowed:
            if isinstance(item, allowed):
                return True
        return False
