baseconv
========

Copyright (c) 2010, 2011, 2012, 2015 Guilherme Gondim.
All rights reserved.

Copyright (c) 2009 Simon Willison.
All rights reserved.

Copyright (c) 2002 Drew Perttula.
All rights reserved.

**Description:**
    Python module to convert numbers from base 10 integers to base X strings and back again.
**Author(s):**
    Drew Perttula, Simon Willison, Guilherme Gondim
**License:**
    Python Software Foundation License version 2
**Project website:**
    https://github.com/semente/python-baseconv
**References:**
    http://www.djangosnippets.org/snippets/1431/ ;
    http://code.activestate.com/recipes/111286/

Install and Usage Instructions
------------------------------

You can use ``pip`` to install ``baseconv`` module::

    $ pip install python-baseconv

Sample usage::

  >>> base20 = BaseConverter('0123456789abcdefghij')
  >>> base20.encode(1234)
  '31e'
  >>> base20.decode('31e')
  '1234'
  >>> base20.encode(-1234)
  '-31e'
  >>> base20.decode('-31e')
  '-1234'
  >>> base11 = BaseConverter('0123456789-', sign='$')
  >>> base11.encode('$1234')
  '$-22'
  >>> base11.decode('$-22')
  '$1234'

License information
-------------------

See the file "LICENSE" for terms & conditions for usage, and a
DISCLAIMER OF ALL WARRANTIES.

This baseconv distribution contains no GNU General Public Licensed (GPLed)
code, just like prior baseconv distributions.

All trademarks referenced herein are property of their respective
holders.

Django
------

The Django Project includes a copy of this module on ``django.utils.baseconv``.
