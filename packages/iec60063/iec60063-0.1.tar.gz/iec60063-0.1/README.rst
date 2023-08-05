
IEC60063 Preferred Values
=========================

This python module provides a generator for the IEC60063 Preferred
Values. These are the 'standard' values for varius types of passive
electrical components, such as resistors, capacitors, etc.

For more information about IEC60063, take a look at this
`Wikipedia page <https://en.wikipedia.org/wiki/Preferred_number>`_.

Usage Example
-------------

>>> import iec60063
>>> values = iec60063.gen_vals('resistor', 'E12', '1E', '10K')
>>> for value in values:
>>>     print value


.. note:: Though this module provides the preferred values, there is no
          guarantee that the values generated will actually be something
          that you can find in a market near you. If this is something you
          intend to use to calculate values for components that you will
          physically need, you should first try to determine what ranges
          of values are easily available from wherever you normally obtain
          them for each series and component type.


Installation
------------

This package can be installed from pypi using pip::

    $ pip install iec60063

Or using easy_install::

    $ easy_install iec60063


Source Downloads and Documentation
----------------------------------

The simplest way to obtain the source for this package is to clone the git repository::

    https://github.com/chintal/iec60063

You can install it as usual, with::

    python setup.py install

The latest version of the documentation can be found at `ReadTheDocs <http://iec60063.readthedocs.org/en/latest/index.html>`_.

License
-------

iec60063 is distributed under the LGPLv3 license.
