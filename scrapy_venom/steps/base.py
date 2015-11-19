# -*- coding: utf-8 -*-

import functools

__all__ = ['BaseStep']


class BaseStep(object):
    """
    Base class for all steps. Implements the base functions
    and enforces the use for the BaseStep.crawl()

    """
    next_step = None

    def __init__(self, spider, *args, **kwargs):
        self.spider = spider
        self.parent_step = kwargs.pop('parent_step', None)
        self.next_step = kwargs.pop('next_step', None)
        super(BaseStep, self).__init__(*args, **kwargs)

    def call_next_step(self, selector, **context):
        """
        Calls the next step. the context argument
        will be passed to the next step.

        """
        # Transforms the next step class into a function
        # Passing the references to the spider and te previous step
        func = self.next_step.as_func(
            spider=self.spider, parent_step=self)

        # I'ts necessary yield every item that the next step returns
        for item in func(selector, **context):
            yield item

    def _crawl(self, selector):
        """
        Method for execute before the main implementation
        (like "pre_crawl")

        """
        for result in self.crawl(selector) or []:
            yield result

    @classmethod
    def as_func(cls, spider, parent_step=None, next_step=None):
        """
        Transforms the entire class into a function

        """
        def step(response, **kwargs):
            self = cls(
                spider=spider, parent_step=parent_step, next_step=next_step)

            for result in self._crawl(response):
                yield result

        functools.update_wrapper(step, cls, updated=())
        return step

    def response_to_file(self, path, response):
        """
        An util method for print the actual response page to
        a file specified at "path" argument

        """
        with open(path, 'wb') as f:
            f.write(response.body)

    def crawl(self, selector):
        """
        The main method of the spider. This needs to be implemented
        by childs classes.

        """
        raise NotImplementedError(
            u'É necessário implementar o método crawl')
