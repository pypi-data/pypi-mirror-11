Roman numerals
==============

`Roman numerals`_ encoder/decoder

.. warning:: ASCII characters support value 1~3999 only...

.. todo:: using unicode to extend

.. _`Roman numerals`: https://en.wikipedia.org/wiki/Roman_numerals

Usage
-----

Example:

.. code-block:: python

    >>> from leetehao import roman
    >>> roman.encode(2549)
    'MMDXLIX'
    >>> roman.encode('MMDXLIX')
    2549
