cne
===

.. image:: https://img.shields.io/pypi/v/cne.svg
    :target: https://pypi.python.org/pypi/cne

.. image:: https://img.shields.io/pypi/dm/cne.svg
        :target: https://pypi.python.org/pypi/cne

.. image:: https://img.shields.io/pypi/dm/cne.svg
        :target: https://pypi.python.org/pypi/cne

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
        :target: https://raw.githubusercontent.com/lgaticaq/python-cne/master/LICENSE

.. image:: https://codeship.com/projects/4d6ff4e0-2a72-0133-0222-622b866f1c07/status?branch=master
        :target: https://codeship.com/projects/98282

Get fuel price from cne api

Installation
------------

.. code-block:: bash

    $ pip install cne


Use
---

.. code-block:: python

    >>> import cne
    >>> data = cne.get()
    >>> print(data)
    {'gasolina_97': 842, 'gasolina_95': 805, 'kerosene': 578, 'gasolina_93': 769, 'petroleo_diesel': 494}
    >>> data = cne.get(fuel_type='gasolina_93')
    >>> print(data)
    769
