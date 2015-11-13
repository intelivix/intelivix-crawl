# -*- coding: utf-8 -*-

import mongoengine as mongo

mongo.connect('scrapy_venom_admin')


class Spider(mongo.Document):
    name = mongo.StringField()
    started_at = mongo.DateTimeField()
    finished_at = mongo.DateTimeField()
    state = mongo.StringField()  # scheduled, in_progress, finished, error
    error_message = mongo.StringField()
    arguments = mongo.DictField()
    result = mongo.StringField()
