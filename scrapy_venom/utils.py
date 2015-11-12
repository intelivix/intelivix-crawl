# -*- coding: utf-8 -*-

import urllib


class StepContext(dict):
    """
    Subclass of dict discovered in Fabric
    instance = _StepContext({'ok': 'ok google'})
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


def make_url(payload, url):
    """
    Makes the url with the payload (QueryString)

    """
    if not payload:
        return url
    payload = urllib.urlencode(payload)
    url = url + '?' + payload
    return url


def get_hidden_fields(selector):
    """
    Get the hidden inputs in the response
    """
    hidden_fields = {}
    for item in selector.xpath('descendant::input[@type="hidden"]'):
        key = item.xpath('./@name').extract()[0]
        value = item.xpath('./@value').extract()[0]
        hidden_fields.update({key: value})
    return hidden_fields
