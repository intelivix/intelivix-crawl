# -*- coding: utf-8 -*-

from scrapy import http
from scrapy import selector as scrapy_selector
from scrapy_venom import utils
from scrapy_venom import exceptions
from scrapy_venom.steps import base


class LoginStep(base.BaseStep):
    """
    Generic step to help in authentication

    """

    def crawl(self, selector):

        # Get's the credentials from the spider
        payload = self.spider.get_credentials()

        # Fill the payload with the hidden fields in the html
        hidden_payload = utils.get_hidden_fields(selector)
        payload.update(hidden_payload)

        # Makes a POST request to the login_form_action
        yield http.FormRequest(
            url=self.spider.login_form_action or self.spider.login_url,
            formdata=payload,
            callback=self.handle_response
        )

    def handle_response(self, response):
        selector = scrapy_selector.Selector(response)

        # Checks if the login was successful
        if not self.spider.login_was_successful(selector):
            raise exceptions.LoginError(
                u'Ocorreram problemas com o login')

        url = self.get_initial_url()

        # If not exists the url, uses the url
        # from the response of login
        if not url:
            step = self.get_initial_step()
            for item in step(response):
                yield item
        else:
            # Else, send's a GET request to the initial_url
            yield http.Request(
                url=url,
                headers={'referer': url},
                callback=self.get_initial_step())

    def get_initial_url(self):

        # Makes the url with the payload
        # If the initial_url was defined in the spider
        initial_url = self.spider.initial_url or self.spider.get_initial_url()
        payload = self.spider.get_payload()

        if not initial_url:
            return None

        return utils.make_url(url=initial_url, payload=payload)

    def get_initial_step(self):
        initial_step = self.spider.initial_step
        return initial_step.as_func(spider=self.spider)
