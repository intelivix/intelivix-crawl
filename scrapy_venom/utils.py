# -*- coding: utf-8 -*-


class _AttributeDict(dict):
    """
    Subclasse de dicionario encontrada em Fabric
    instance = _AttributeDict({'ok': 'ok google'})
    instance.ok
        > ok google
    """
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        self[key] = value
