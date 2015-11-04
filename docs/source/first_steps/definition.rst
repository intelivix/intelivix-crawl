Scrapy-venom? what?
======================================

Scrapy-venom is a standard way for **web crawling** with the `Scrapy framework <http://doc.scrapy.org/>`_. Usually we started in the programming world solving simple problems with sync functions, which eventually forms the mindset for sync programming. When new people start with scrapy, which uses async functions, it's hard and confusing for they to get used to the projects. Scrapy-venom come with a new approach for the use of Scrapy, implementing the concept of flows, a definition of sequential steps to achieve the goal.


.. seealso::
    `Sync and Async what?? See this topic for understand <http://stackoverflow.com/questions/16336367/what-is-the-difference-between-synchronous-and-asynchronous-programming-in-node>`_.


The concept of Steps
--------------------

Basically, the concept is a sequence of steps. The spider defines the initial step and every step will decide the next step to be executed. See the example:

**GoogleSpider**

The goal of this spider is make a query to google and get all links and images from the result.

* **STEP 1:** Make a GET request: https://www.google.com.br?q=keyword
* **STEP 2:** Get all links from the response and make a new request to the page of images, passing the result to the next step.
* **STEP 3:** Get all images from the response of the previous step.
