# -*- coding: utf-8 -*-

from .mixins import PipelineAllowedMixin
from .mixins import ItemAllowedMixin


__all__ = ['PipelineBase']


class PipelineBase(PipelineAllowedMixin, ItemAllowedMixin):

    def item_pipeline(self, item, spider):
        raise NotImplementedError(
            'BasePipeline requires an item_pipeline method.')

    def pre_item_pipeline(self, item, spider):
        pass

    def pos_item_pipeline(self, item, spider):
        pass

    def process_item(self, item, spider):

        if not self.pipeline_is_allowed(spider):
            return item

        if not self.item_is_allowed(item):
            return item

        self.pre_item_pipeline(item, spider)
        item = self.item_pipeline(item, spider)
        self.pos_item_pipeline(item, spider)

        return item
