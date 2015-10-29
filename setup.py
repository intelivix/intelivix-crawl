# -*- coding: utf-8 -*8-

from setuptools import setup, find_packages


setup(
    name='intelivix-crawl',
    version='0.0.1',
    packages=find_packages(),
    package_data={
        'scrapy_venom': [],
    },
    entry_points={
        'console_scripts': ['venom = scrapy_venom.management:execute_command']
    },
    install_requires=[],
    zip_safe=False,
)
