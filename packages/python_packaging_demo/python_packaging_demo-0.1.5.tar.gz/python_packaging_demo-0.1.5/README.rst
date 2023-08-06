A sample Python project
=========================
License
-------

.. image:: https://img.shields.io/pypi/l/python_packaging_demo.svg
    :target: https://github.com/webee/python-packaging-demo/blob/master/LICENSE
    :alt: The MIT License

PYPI
----

.. image:: https://img.shields.io/pypi/v/python_packaging_demo.svg
    :target: https://pypi.python.org/pypi/python_packaging_demo
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/wheel/python_packaging_demo.svg
    :target: https://pypi.python.org/pypi/python_packaging_demo
    :alt: wheel

.. image:: https://img.shields.io/pypi/format/python_packaging_demo.svg
    :target: https://pypi.python.org/pypi/python_packaging_demo
    :alt: format

.. image:: https://img.shields.io/pypi/pyversions/python_packaging_demo.svg
    :target: https://pypi.python.org/pypi/python_packaging_demo
    :alt: python versions

.. image:: https://img.shields.io/pypi/implementation/python_packaging_demo.svg
    :target: https://pypi.python.org/pypi/python_packaging_demo
    :alt: implementation

.. image:: https://img.shields.io/pypi/status/python_packaging_demo.svg
    :target: https://pypi.python.org/pypi/python_packaging_demo
    :alt: status

.. image:: https://img.shields.io/pypi/dm/python_packaging_demo.svg
    :target: https://pypi.python.org/pypi/python_packaging_demo
    :alt: downloads/month

.. image:: https://img.shields.io/pypi/dw/python_packaging_demo.svg
    :target: https://pypi.python.org/pypi/python_packaging_demo
    :alt: downloads/week

.. image:: https://img.shields.io/pypi/dd/python_packaging_demo.svg
    :target: https://pypi.python.org/pypi/python_packaging_demo
    :alt: downloads/day

Describe
--------

A sample project that demonstrate python packaging and upload to pypi.

build && upload
::

    $ python setup.py sdist
    $ python setup.py bdist_wheel
    $ python setup.py register -r pypi
    $ python setup.py sdist upload -r pypi
    $ python setup.py bdist_wheel upload -r pypi
