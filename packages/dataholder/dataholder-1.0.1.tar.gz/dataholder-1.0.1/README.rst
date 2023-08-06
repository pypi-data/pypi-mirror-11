dataholder
======

This is a trick for assignment in an if statement.

Install
-------
.. code-block:: sh

    pip install dataholder

Usage
-----

.. code-block:: python

    import re
    from dataholder import DataHolder

    input = u'test bar 123'
    save_match = DataHolder(attr_name='match')
    if save_match(re.search('foo (\d+)', input)):
        print "Foo"
        print save_match.match.group(1)
    elif save_match(re.search('bar (\d+)', input)):
        print "Bar"
        print save_match.match.group(1)
    elif save_match(re.search('baz (\d+)', input)):
        print "Baz"
        print save_match.match.group(1)


The code was taken from http://stackoverflow.com/a/1806338/1849904

The author of idea is Alex Martelli
