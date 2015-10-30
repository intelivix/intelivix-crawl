Spiders disponíveis para o uso
=======================================

Classes que disponibilizam diversos utilitários para a criação de novas spiders.

Bases disponíveis e sua utilização
-----------------------------------

.. class:: scrapy_venom.steps.spider.SpiderStep
   :noindex:

   Implementação do conceito de fluxo, ou seja, definição de uma sequencia de passos a serem seguidos. Através do atributo :attr:`initial_step_cls`, é definido o primeiro **step** a ser executado, aonde cada **step** tem um atributo :attr:`next_step_cls` que define o próximo **step** a ser executado.


.. class:: scrapy_venom.steps.spider.URLSpiderStep
   :noindex:

   Implementação da :class:`SpiderStep` com o objetivo de facilitar buscas com o método :func:`prepare_payload`, onde são informados os parâmetros de busca e estes parâmetros são injetados no atributo :attr:`initial_url`.



Entendendo o funcionamento das Bases disponíveis
-------------------------------------------------


.. autoclass:: scrapy_venom.base.SpiderBase

.. autoclass:: scrapy_venom.steps.spider.SpiderStep

.. autoclass:: scrapy_venom.steps.spider.URLSpiderStep