# -*- coding: utf-8

import unicodedata


def normalize_ascii(value):
    return unicodedata.normalize('NFKD', unicode(value))\
        .encode('ascii', 'ignore')


def to_unicode(string):
    if isinstance(string, str):
        string = string.decode('utf-8')
    return string


def compare_strings(str1, str2):
    str1 = to_unicode(str1).upper().strip()
    str2 = to_unicode(str2).upper().strip()
    if normalize_ascii(str1) == normalize_ascii(str2):
        return True
    else:
        return False
