Scrapy-venom? what?
======================================


Scrapy-venom é um padrão para **web crawling** do framework scrapy (http://doc.scrapy.org/). Geralmente iniciamos no mundo de desenvolvimento de software utilizando linguagens que usam, por padrão, funções **síncronas**. Porém, por diversos motivos, para **web crawling**, é mais adequado a utilização de funções **assíncronas**, e para novos desenvolvedores é confuso e difícil iniciar projetos nesse estilo. O Scrapy-venom inicia uma nova abordagem, a implementação do conceito de fluxos, uma definição sequencial de passos a serem seguidos para cumprir um objetivo.


.. seealso::
    **Qual a diferença entre funções síncronas e assíncronas?** http://pt.stackoverflow.com/questions/51268/qual-a-diferen%C3%A7a-entre-comunica%C3%A7%C3%A3o-ass%C3%ADncrona-e-s%C3%ADncrona


O conceito de Steps
--------------------

Basicamente, o conceito é formado por uma sequencia definida de passos. Uma Spider irá definir um passo inicial e cada passo irá definir qual o próximo passo a ser seguido. Conforme o exemplo a seguir:

**GoogleSpider**

O objetivo desta spider é realizar a pesquisa de uma palavra-chave no google e salvar todos os links e imagens obtidos no resultado da pesquisa.

* **STEP 1:** Realizar requisição https://www.google.com.br?q=palavra-chave
* **STEP 2:** Salvar todos os links do html recebido do passo anterior, realizar requisição para a aba "Imagens" passando o resultado para o próximo passo
* **STEP 3:** Salvar todas as imagens do html recebido do passo anterior.
