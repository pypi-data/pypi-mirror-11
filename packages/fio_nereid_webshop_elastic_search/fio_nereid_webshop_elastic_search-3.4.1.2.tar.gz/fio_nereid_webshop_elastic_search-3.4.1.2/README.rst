nereid-webshop-elastic-search
=============================

.. image:: https://circleci.com/gh/fulfilio/nereid-webshop-elastic-search/tree/develop.svg?style=shield
    :target: https://circleci.com/gh/fulfilio/nereid-webshop-elastic-search
    :alt: Build Status
.. image:: https://pypip.in/download/fio_nereid_webshop_elastic_search/badge.svg
    :target: https://pypi.python.org/pypi/fio_nereid_webshop_elastic_search/
    :alt: Downloads
.. image:: https://pypip.in/version/fio_nereid_webshop_elastic_search/badge.svg
    :target: https://pypi.python.org/pypi/fio_nereid_webshop_elastic_search/
    :alt: Latest Version
.. image:: https://pypip.in/status/fio_nereid_webshop_elastic_search/badge.svg
    :target: https://pypi.python.org/pypi/fio_nereid_webshop_elastic_search/
    :alt: Development Status

Migration to 3.4
----------------

In version 3.4, the module changed from using ``product_attribute`` core
module from tryton community to `product_attribute_strict 
<https://github.com/openlabs/product-attribute-strict>`_. The
``product_attribute_strict`` module includes a script which helps to
migrate from ``product_attribute`` transparently.
