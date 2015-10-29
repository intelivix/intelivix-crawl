# -*- coding: utf-8 -*-
from .query import get_all_collections


for collection in get_all_collections():
    globals()[collection.collection.name] = collection
