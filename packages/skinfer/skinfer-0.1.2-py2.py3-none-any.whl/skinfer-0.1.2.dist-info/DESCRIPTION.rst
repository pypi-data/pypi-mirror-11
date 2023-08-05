============================================
Skinfer - tool for working with JSON schemas
============================================

.. image:: https://badge.fury.io/py/skinfer.png
    :target: http://badge.fury.io/py/skinfer

.. image:: https://travis-ci.org/scrapinghub/skinfer.png?branch=master
        :target: https://travis-ci.org/scrapinghub/skinfer

.. image:: https://pypip.in/d/skinfer/badge.png
        :target: https://pypi.python.org/pypi/skinfer


Simple tool to infer and/or merge JSON schemas

* Free software: BSD license
* Documentation: https://skinfer.readthedocs.org.

Features
--------

* Generating schema in **JSON Schema draft 4** format
* Inferring schema from multiple samples
* Merging schemas - nice for generating schema in Map-Reduce fashion
  or updating an old schema with new data


Example of using `schema_inferer` to generate a schema from a list of samples::

    $ cat samples.jsonl
    {"name": "Claudio", "age": 29}
    {"name": "Roberto", "surname": "Gomez", "age": 72}
    $ ./bin/schema_inferer --jsonlines samples.jsonl
    {
        "$schema": "http://json-schema.org/draft-04/schema",
        "required": [
            "age",
            "name"
        ],
        "type": "object",
        "properties": {
            "age": {
                "type": "number"
            },
            "surname": {
                "type": "string"
            },
            "name": {
                "type": "string"
            }
        }
    }


Install with::

    $ pip install skinfer

Or, if you don't have ``pip``, you can still install it with::

    $ easy_install skinfer




History
-------

0.1.1 (2015-05-01)
------------------

* Support more complex string-type schemas
* Attempt to infer JSON lines format instead of just failing
* API cleanup: no need for long imports anymore
* Updated documentation, added docstrings
* Fixed merging schema for arrays with tuple vs list validation
* Fixed compatibility issues with Python 2.6
* Improved test coverage, added end-to-end tests


0.1.0 (2015-03-03)
---------------------

* First release on PyPI.


