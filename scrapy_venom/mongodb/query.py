# -*- coding: utf-8 -*-

import pymongo
from scrapy.conf import settings


__all__ = ['get_all_collections']


connection = pymongo.MongoClient(
    settings['MONGODB_SERVER'],
    settings['MONGODB_PORT']
)

db = connection[settings['MONGODB_DB']]


def db_getattr(cls, attr):
    try:
        return object.__getattribute__(cls, attr)
    except AttributeError:
        return getattr(cls.collection, attr)


class Meta(type):

    def __new__(cls, name, bases, dikt):
        fgetattr = dikt.get('__getattr__')
        if fgetattr is not None:
            setattr(cls, '__getattr__', db_getattr)
        return super(Meta, cls).__new__(cls, name, bases, dikt)


class MongoQuery(object):

    __metaclass__ = Meta
    collection = None

    @classmethod
    def find(cls, **query):
        results = []
        for item in cls.collection.find(query):
            results.append(item)
        return results

    @classmethod
    def find_one(cls, **query):
        return cls.collection.find_one(query)


def get_new_cls(collection):
    class_name = str(collection + 'Collection')
    base_classes = (MongoQuery,)
    attrs = {'__getattr__': db_getattr, 'collection': db[collection]}
    return type(class_name, base_classes, attrs)


def get_all_collections():
    collections = []
    for collection in db.collection_names():
        collections.append(get_new_cls(collection))
    return collections
