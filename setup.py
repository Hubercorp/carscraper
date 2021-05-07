from setuptools import setup, find_packages

setup(
    name='oldtimertrends',
    version='0.1',
    description='auction scrapper',
    author='Jerome Huberty',
    author_email='',
    packages=find_packages(),
    install_requires=[
        'Scrapy',
        'pymongo',
        'cryptography'
    ]
)