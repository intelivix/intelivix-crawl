Tutorial - Starting a new project
===================================


Clone our project template
-------------------------------

Our project template uses a lib called `cookiecutter <http://cookiecutter.readthedocs.org/en/latest/>`_, so the first step is to install it using the pip.

.. code-block:: bash
    
    $ pip install cookiecutter


Now, use the cookiecutter command line to clone our project template and boot a new project. Questions will be made to config your project during this process.

.. code-block:: bash
    
    $ cookiecutter gh:intelivix/scrapy-venom


.. note::
    It's strongly recommended to use `Virtualenv <https://virtualenv.readthedocs.org/en/latest/>`_ and `Virtualenvwrapper <https://virtualenvwrapper.readthedocs.org/en/latest/>`_


Create the first SpiderStep
-------------------------------

It's very important to have a well-defined objective for the implementation of a spider. So let us contextualize our problem:


    *John is a student in computing and need to get as much information about social networks as he can. So john decided to get all links and images about social networks in google.*

Okay, now our goal is defined, we need to **get all links and images about social networks in google**.
For achieve this goal, we need to execute some steps:

* Request the search page to get all links
* Request the images page to get all images

Now that we know what we should do, let's have some fun! 
To create our first spider, use the scrapy-venom command-line :func:`start_spider`

.. code-block:: bash

    $ venom startspider google


The new app was created at ``project.spiders.google`` with the following files:

* ``__init__.py``
* ``items.py``
* ``pipelines.py``
* ``spiders.py``
* ``steps.py``
* ``models.py``

The files ``items.py``, ``pipelines.py``, ``spiders.py`` are defined at `Scrapy documentation <http://doc.scrapy.org/en/latest/>`_. The file ``models.py`` defines our tables of database. The most diferent file is ``steps.py`` which defines the steps to achieve the goal of the current spider. After create the new spider, set the spider name into settings.

.. code-block:: python
    
    # ADD THE NEW APP

    SPIDER_MODULES = register_spiders(
        'sample',
        'google'
    )

Our spider was created with some basic attributes in ``spiders.py``. The ``name`` attribute defines how we call this spider in command line. ``initial_url`` defines the url which this spider will request when executed. The property ``steps`` defines the sequence of steps for process the response from ``initial_url``.

.. code-block:: python

    # -*- coding: utf-8 -*-

    from scrapy_venom.spiders import SpiderStep


    class GoogleSpider(SpiderStep):

        name = 'google-spider'
        initial_url = ''

        @property
        def steps(self):
            return ()


First, define the ``initial_url`` with value ``https://www.google.com`` and determine the params to be searched with the property ``payload``. The spider will make a GET request in url ``https://www.google.com?q=social+network``

.. code-block:: python

    # -*- coding: utf-8 -*-

    from scrapy_venom.spiders import SpiderStep


    class GoogleSpider(SpiderStep):

        name = 'google-spider'
        initial_url = 'https://www.google.com'

        @property
        def steps(self):
            return ()

        @property
        def payload(self):
            return {'q': 'social network'}


Get all links from Google
--------------------------

As we had set in our context, first we need to get all links of the search page. With the response from ``https://www.google.com?q=social+network``, we need to define our first step.

.. code-block:: python
    
    # google/spiders.py
    # -*- coding: utf-8 -*-

    from scrapy_venom.spiders import SpiderStep
    from .steps import LinkStep

    class GoogleSpider(SpiderStep):

        name = 'google-spider'
        initial_url = 'https://www.google.com'

        @property
        def payload(self):
            return {'q': 'social network'}

        @property
        def steps(self):
            return (LinkStep,)


.. code-block:: python

    # google/steps.py
    # -*- coding: utf-8 -*-

    from scrapy_venom.steps import Step

    class LinkStep(Step):

        def crawl(self, selector):
            pass


The implementation of method :func:`crawl` is required and is used to navigate the html and do one thing to achieve the goal of spider. For the step returns a link, we need to define an item class in ``items.py`` with only one attribute: ``url``.


.. code-block:: python
    
    # google/items.py
    # -*- coding: utf-8 -*-

    from scrapy import Item
    from scrapy import Field
    
    class Link(Item):
        url = Field()


Now we can start to crawl the response. In our case, we need to get all ``href`` of the links. Usually we use xpath for this. In the method :func:`crawl` we promise an list of links and all of links will iterate over the method :func:`clean_item` which returns a dict with will instantiate ou item_class `items.Link`.

.. code-block:: python

    # -*-coding: utf-8 -*-

    from scrapy_venom.steps import Step
    from .items import LinkItem

    class LinkStep(Step):

        item_class = LinkItem

        # receives every link, one by one
        def clean_item(self, extraction):
            # assuming that the links will be poor like:
            # >> 'https://www.facebook.com\n\t\t\b'
            # we will clean with .strip()
            cleaned_data = {}
            cleaned_data['url'] = extraction.strip()
            return cleaned_data

        def crawl(self, selector):
            # promises a list of hrefs
            yield selector.xpath('//a/@href')


Okay, now we have completed the first step to achieve our goal. Executing this spider in the terminal by command ``scrapy crawl google-step -t json -o links.json``, we have the result of the first step.

.. code-block:: json
    
    [
    {"url": "https://www.what-is-social-network.com"},
    {"url": "https://www.socialnetworks.com"},
    {"url": "https://www.samplesocial.com"}
    ]


Now we have all the links, but our next problem is "get all images" and in the current response page doesn't have any images. We must pass to the next step the url which he will process. To do this, we have to add ``request_url`` key into the attribute ``next_step_kwargs``.


.. code-block:: python

    # -*-coding: utf-8 -*-

    from scrapy_venom.steps import Step
    from .items import LinkItem

    class LinkStep(Step):

        item_class = LinkItem

        # receives every link, one by one
        def clean_item(self, extraction):
            # assuming that the links will be poor like:
            # >> 'https://www.facebook.com\n\t\t\b'
            # we will clean with .strip()
            cleaned_data = {}
            cleaned_data['url'] = extraction.strip()
            return cleaned_data

        def crawl(self, selector):
            # promises a list of hrefs
            yield selector.xpath('//a/@href')

            # passing the next url to be accessed
            self.next_step_kwargs['request_url'] = self.get_images_link(selector)

        def get_images_link(self, selector):
            # searchs for <a href="#"> that contains "Image"
            url = selector.xpath(
                '//a/text() == "Images"').xpath('./@href').extract()[0]
            return 'https://www.google.com' + url

.. seealso::
    
    `click here to see how use the Xpath syntax <http://www.w3schools.com/xsl/xpath_syntax.asp>`_



    


Get all images from Google
----------------------------------


As we had set in our context, now we need to get all image of the search images page. With the response from ``https://www.google.com?q=social+network&tbm=isch`` requested from previous step, we can define our new step. We don't need create any new item, because we don't want to save the images, only get this links to access other time. So, let's code!


.. code-block:: python
    
    # google/spiders.py
    # -*- coding: utf-8 -*-

    from scrapy_venom.spiders import SpiderStep
    from .steps import LinkStep
    from .steps import ImageStep

    class GoogleSpider(SpiderStep):

        name = 'google-spider'
        initial_url = 'https://www.google.com'

        @property
        def payload(self):
            return {'q': 'social network'}

        @property
        def steps(self):
            return (LinkStep, ImageStep)


.. code-block:: python

    # -*-coding: utf-8 -*-

    from scrapy_venom.steps import Step
    from .items import LinkItem

    class ImageStep(Step):

        item_class = LinkItem

        def clean_item(self, extraction):
            cleaned_data = {}
            cleaned_data['url'] = extraction.strip()
            return cleaned_data

        def crawl(self, selector):
            # promises a list of srcs
            yield selector.xpath('//img/@src')


.. code-block:: json

    [
    {"url": "https://www.what-is-social-network.com"},
    {"url": "https://www.socialnetworks.com"},
    {"url": "https://www.samplesocial.com"},
    {"url": "https://www.samplesocial.com/images/example.png"},
    {"url": "https://www.samplesocial.com/images/logo.png"},
    ]


Store the links in a database
----------------------------------

Store the images in a database
----------------------------------
