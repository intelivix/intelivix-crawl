# -*- coding: utf-8 -*-

from scrapy.exceptions import CloseSpider


class Error(Exception):

    def __init__(self, reason):
        self.reason = reason
        self.message = reason


class ArgumentError(Exception):
    """
    Errors related with arguments

    """
    pass


class LoginError(CloseSpider):
    """
    Errors related to authentication

    """
    pass


class DoesNotExistError(CloseSpider):
    pass


class UnexpectedError(CloseSpider):
    pass
