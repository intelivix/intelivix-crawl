# -*- coding: utf-8 -*-

from scrapy import Request
from scrapy.spiders import Spider
from scrapy_venom import steps
from scrapy_venom import utils
from scrapy_venom import exceptions


__all__ = ['SpiderStep']


class SpiderStep(Spider):
    """
    Base class for all spiders. Implements the base functions
    and enforces the concept of steps

    Attributes:

        initial_step    The initial class that will process the response
        initial_url     The initial url that will be requested
        payload         The payload that will be the QueryStrings
        options         Options to be passed to the scrapy.Request

    """

    initial_step = None
    initial_url = ''
    payload = {}
    options = {}
    required_args = []

    def __init__(self, *args, **kwargs):
        try:
            super(SpiderStep, self).__init__(*args, **kwargs)

            assert self.initial_step and \
                issubclass(self.initial_step, steps.BaseStep), (
                    u'The initial_step attribute must be a subclass'
                    ' of scrapy_venom.steps.BaseStep')

        except AssertionError as e:
            raise exceptions.ArgumentError(reason=e.message)

        except Exception as e:
            raise exceptions.UnexpectedError(reason=e.message)

    def start_requests(self):

        # Get the initial_url
        url = self.get_initial_url()

        # Set's the referer_url in the headers and makes the request
        hdrs = {'referer': url}
        yield Request(
            callback=self.crawl,
            headers=hdrs,
            url=url, **self.get_options())

    def crawl(self, response):
        utils.validate_required_args(
            self.required_args, self)

        initial_step = self.get_initial_step()
        for item in initial_step(response):
            yield item

    def get_options(self):
        return self.options

    def get_payload(self):
        return self.payload

    def get_initial_step(self):
        return self.initial_step.as_func(spider=self)

    def get_initial_url(self):
        return utils.make_url(
            payload=self.payload,
            url=self.initial_url)


class AuthSpiderStep(SpiderStep):
    """
    Implementation to help scraping urls that require's authentication
    The arguments of SpiderBase remains

    Attributes:

        login_url           The login_url that will be requested
        login_step          The default step that will process the login
        credentials         The credentials to authenticate
        login_form_action   The url that credentials will be POSTED
            if not provided, the default will be the login_url

    """

    login_url = ''
    login_step = steps.LoginStep
    credentials = {}
    login_form_action = ''

    def login_was_successful(self, selector):
        """
        Returns if the login was successful by looking at
        the response html. Returns True or False.
        """
        return True

    def get_initial_url(self):
        return self.login_url

    def get_initial_step(self):
        return self.login_step.as_func(spider=self)

    def get_login_form_action(self):
        return self.login_form_action or self.login_url

    def get_credentials(self):
        return self.credentials
