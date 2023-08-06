===============================
Flatson
===============================

.. image:: https://img.shields.io/travis/scrapinghub/flatson.svg
        :target: https://travis-ci.org/scrapinghub/flatson

.. image:: https://img.shields.io/pypi/v/flatson.svg
        :target: https://pypi.python.org/pypi/flatson


A tool to flatten JSON-like objects, allowing to configure via an annotated JSON schema

* Free software: BSD license
* Documentation: https://flatson.readthedocs.org.

Features
--------

* Flattens Python dictionaries using a JSON schema
* Supports per-field configuration via the schema

Usage::

    >>> from flatson import Flatson
    >>> schema = {
            "$schema": "http://json-schema.org/draft-04/schema",
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "number"},
                "address": {
                    "type": "object",
                    "properties": {"city": {"type": "string"}, "street": {"type": "string"}}
                },
                "skills": {"type": "array", "items": {"type": "string"}}
            }
        }
    >>> sample = {
                "name": "Claudio", "age": 42,
                "address": {"city": "Paris", "street": "Rue de Sevres"},
                "skills": ["hacking", "soccer"]}
    >>> f = Flatson(schema)
    >>> f.fieldnames
    ['address.city', 'address.street', 'age', 'name', 'skills']
    >>> f.flatten(sample)
    ['Paris', 'Rue de Sevres', 42, 'Claudio', '["hacking","soccer"]']

You can get a dict with the field names order preserved::

    >>> f.flatten_dict(sample)
    OrderedDict([('address.city', 'Paris'), ('address.street', 'Rue de Sevres'), ('age', 42), ('name', 'Claudio'), ('skills', '["hacking","soccer"]')])

You can also configure array serialization behavior through the schema (default JSON)::

    >>> schema = {
            "$schema": "http://json-schema.org/draft-04/schema",
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "skills": {
                    "type": "array",
                    "items": {"type": "string"},
                    "flatson_serialize": {"method": "join_values"},
                }
            }
        }
    >>> f = Flatson(schema)
    >>> f.flatten({"name": "Salazar", "skills": ["hacking", "socker", "partying"]})
    ['Salazar', 'hacking,socker,partying']


Next Steps
----------

Read more on :ref:`how to use Flatson <usage>`, check out the `Github Repo`_
and feel free to send Issues or PRs. =)

.. _Github Repo: https://github.com/scrapinghub/flatson
