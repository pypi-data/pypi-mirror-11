LowVoltage is a standalone Python (2.7+ and 3.4+) client for `DynamoDB <http://aws.amazon.com/documentation/dynamodb/>`__
that doesn't hide any feature of `the API <http://docs.aws.amazon.com/amazondynamodb/latest/APIReference/Welcome.html>`__.

It's licensed under the `MIT license <http://choosealicense.com/licenses/mit/>`__.
It depends only on the excellent `python-requests <http://python-requests.org>`__ library.
It's available on the `Python package index <http://pypi.python.org/pypi/LowVoltage>`__, its `documentation is hosted by Python <http://pythonhosted.org/LowVoltage>`__ and its source code is on `GitHub <https://github.com/jacquev6/LowVoltage>`__.

It's currently in the beta stage, meaning I believe the interface will be faily stable but may still change if we have good reasons to do so.
Please have a look to the `changelog <http://pythonhosted.org/LowVoltage/changelog.html>`__ when updating between v0.x releases.
I'll do my best to respect `semantic versioning <http://semver.org/>`__.

Questions? Remarks? Bugs? Want to contribute? `Open an issue <https://github.com/jacquev6/LowVoltage/issues>`__!

.. image:: https://img.shields.io/travis/jacquev6/LowVoltage/master.svg
    :target: https://travis-ci.org/jacquev6/LowVoltage

.. image:: https://img.shields.io/coveralls/jacquev6/LowVoltage/master.svg
    :target: https://coveralls.io/r/jacquev6/LowVoltage

.. image:: https://img.shields.io/codeclimate/github/jacquev6/LowVoltage.svg
    :target: https://codeclimate.com/github/jacquev6/LowVoltage

.. image:: https://img.shields.io/scrutinizer/g/jacquev6/LowVoltage.svg
    :target: https://scrutinizer-ci.com/g/jacquev6/LowVoltage

.. image:: https://img.shields.io/pypi/dm/LowVoltage.svg
    :target: https://pypi.python.org/pypi/LowVoltage

.. image:: https://img.shields.io/pypi/l/LowVoltage.svg
    :target: https://pypi.python.org/pypi/LowVoltage

.. image:: https://img.shields.io/pypi/v/LowVoltage.svg
    :target: https://pypi.python.org/pypi/LowVoltage

.. image:: https://img.shields.io/pypi/pyversions/LowVoltage.svg
    :target: https://pypi.python.org/pypi/LowVoltage

.. image:: https://img.shields.io/pypi/status/LowVoltage.svg
    :target: https://pypi.python.org/pypi/LowVoltage

.. image:: https://img.shields.io/github/issues/jacquev6/LowVoltage.svg
    :target: https://github.com/jacquev6/LowVoltage/issues

.. image:: https://badge.waffle.io/jacquev6/lowvoltage.png?label=ready&title=ready
    :target: https://waffle.io/jacquev6/lowvoltage

.. image:: https://img.shields.io/github/forks/jacquev6/LowVoltage.svg
    :target: https://github.com/jacquev6/LowVoltage/network

.. image:: https://img.shields.io/github/stars/jacquev6/LowVoltage.svg
    :target: https://github.com/jacquev6/LowVoltage/stargazers

.. _quick-start:

Quick start
===========

Install from PyPI::

    $ pip install LowVoltage

Import the package and create a connection (assuming your ``AWS_ACCESS_KEY_ID`` and ``AWS_SECRET_ACCESS_KEY`` environment variables are set):

>>> from LowVoltage import *
>>> connection = Connection("us-west-2", EnvironmentCredentials())

Assuming you have a table named ``"LowVoltage.Tests.Doc.1"`` with a hash key on the number attribute ``"h"``, you can put an item and get it back:

>>> table = "LowVoltage.Tests.Doc.1"

>>> connection(PutItem(table, {"h": 0, "a": 42, "b": u"bar"}))
<LowVoltage.actions.put_item.PutItemResponse ...>

>>> connection(GetItem(table, {"h": 0})).item
{u'a': 42, u'h': 0, u'b': u'bar'}
