# -*- coding: utf-8 -*-

import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log

from ..pipelines import PipelineBase


__all__ = ['MongoDBPipeline']


class MongoDBPipeline(PipelineBase):

    '''
        collections = {
            Item: {
                'model': 'ItemModel',
                'unique_key': 'pk',
            }
        }
    '''

    collections = {}

    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.items_allowed = []
        self._update_collections(db)

    def _update_collections(self, db):
        for key, value in self.collections.iteritems():
            self.items_allowed.append(key)
            self.collections[key]['db'] = db[value['model']]

    def item_pipeline(self, item, spider):
        for data in item:
            if not data:
                raise DropItem("Missing data!")

        self.create_or_update(item)
        log.msg("added to MongoDB database!", level=log.DEBUG, spider=spider)
        return item

    def create_or_update(self, item):
        collection = self.get_collection(item)
        collection['db'].update(
            {collection['unique_key']: item[collection['unique_key']]},
            dict(item),
            upsert=True)

    def get_collection(self, item):
        return self.collections[type(item)]
