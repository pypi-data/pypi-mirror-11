pydba
=====

A handy Python library for common database admin operations.

.. image:: https://img.shields.io/pypi/v/pydba.svg
  :target: https://pypi.python.org/pypi/pydba

Requirements
------------
.. image:: https://img.shields.io/pypi/pyversions/pydba.svg
  :target: pypi.python.org/pypi/pydba

Features
--------

Basic imports and class constructor usage.

    >>> from pydba import PostgresDB
    >>> db = PostgresDB()
    >>> db.available()
    True
    >>> db.names()
    ['postgres']

Database creation and deletion.

    >>> db.create('foo')
    >>> db.names()
    ['postgres', 'foo']
    >>> db.rename('foo', 'bar')
    >>> db.names()
    ['postgres', 'bar']

Database backup and restore.

    >>> db.dump('bar', 'bar.backup')
    >>> db.drop('bar')
    >>> db.names()
    ['postgres']
    >>> db.restore('bar', 'bar.backup')
    >>> db.names()
    ['postgres', 'bar']

Querying and shutting down database connections.

    >>> db.connections('postgres')
    [Connection(datname='postgres', pid=13832, state='idle', query='', usename='drkjam', ...)]
    >>> db.kill_connections('postgres')
    >>> db.connections('postgres')
    []


