Constants
=========

Default constants are overwritable.

How to overwrite constants
--------------------------

1. Create `leetehao_local.py` at your project running root
2. Add constants you wnat to overwite, i.e: `MORSE_SPLIT = '^_^'`
3. Run your shell or project again

.. warning::
    Overwrited constants ONLY apply to constants which is accessed with `global_constants`.
    Take previous settings for example, use `global_contants.morse.MORSE_SPLIT` to retireve constants would get default and built-in value ' ' not '^_^'
