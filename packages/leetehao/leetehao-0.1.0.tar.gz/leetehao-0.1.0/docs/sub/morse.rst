Morse
=====

`Morse code`_ encoder/decoder

.. _`Morse code`: https://en.wikipedia.org/wiki/Morse_code

Usage
-----

Example:

.. code-block:: python

    >>> from leetehao import morse
    >>> morse.encode('hello world')
    '.... . .-.. .-.. --- / .-- --- .-. .-.. -..'
    >>> morse.encode('.... . .-.. .-.. --- / .-- --- .-. .-.. -..')
    'HELLO WORLD'

