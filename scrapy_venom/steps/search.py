# -*- coding: utf-8 -*-

from scrapy import http
from scrapy import selector as scrapy_selector
from scrapy_venom import utils
from scrapy_venom import exceptions
from scrapy_venom.steps import base


ALLOWED_METHODS = ('GET', 'POST')


class SearchStep(base.BaseStep):
    """
    Generic step to help make search in pages

    Attributes

        action_url: The url that will be requested with http method
        method: The http method to request the url
        payload: Dict with values to be passed in QueryStrings or FormData

    """

    action_url = ''
    http_method = 'GET'
    payload = {}

    def __init__(self, *args, **kwargs):
        super(SearchStep, self).__init__(*args, **kwargs)
        try:

            assert self.action_url, (
                u'You must define an action_url or get_action_url()')

            assert self.http_method in ALLOWED_METHODS, (
                u'This http_method is not allowed')

            assert isinstance(self.payload, dict), (
                u'The payload must be a dict instance')

        except AssertionError as e:
            raise exceptions.ArgumentError(e.message)

    def _crawl(self, selector):

        # Get's the payload to be searched
        payload = self.get_payload()

        # Get's the url to receive the request
        action_url = self.get_action_url()

        # Get's the http method handler (GET or POST)
        handler = getattr(self, self.http_method.lower())
        yield handler(selector, action_url, payload)

    def get(self, selector, action_url, payload):

        # Get the url with the QuerySrings informed by payload
        url = utils.make_url(url=action_url, payload=payload)

        # Makes a GET request
        return http.Request(url=url, callback=self.wrap_response)

    def post(self, selector, action_url, payload):

        hidden_fields = utils.get_hidden_fields(selector)

        # Update's the payload with hidden fields
        hidden_fields.update(payload)

        # Makes a POST request with the payload defined
        return http.FormRequest(
            url=action_url,
            formdata=hidden_fields,
            callback=self.wrap_response
        )

    def wrap_response(self, response):

        # Wraps the response with a scrapy.Selector instance
        selector = scrapy_selector.Selector(response)
        for item in self.crawl(selector):
            yield item

    def get_action_url(self):
        return self.action_url

    def get_payload(self):
        return self.payload
