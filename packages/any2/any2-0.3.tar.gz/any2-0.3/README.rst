Introduction
============

Any2 is the base for a serie of tools:

  - `Any2csv`_
  - `Any2fixed`_
  - `Any2xl`_

and provides common features such as object adapters and transformers.

.. _Any2csv: https://bitbucket.org/faide/any2csv
.. _Any2fixed: https://bitbucket.org/faide/any2fixed
.. _Any2xl: https://bitbucket.org/faide/any2xl

Licence
=======

This package is covered by the permissive BSD licence.

Python versions
===============

Any2 is tested with the help of tox on python 2.7 and python 3.4
It may work with older versions (some parts were developped using python 2.3)
but no tests or even garantee is made on this.

Changelog
=========

0.3 Jul, 29 2015
~~~~~~~~~~~~~~~~~

  - All new adapters derive from any2.adapters.BaseAdapter
  - Added a new Obj2List adapter to adapt object yielding iterators into
    list yielding iterators, since it is based on the new BaseAdapter it
    supports the same transformer system.

0.2 Jul. 29 2015
~~~~~~~~~~~~~~~~~

  - Fully test covered
  - All raised exceptions now are based on Any2Error to help users catch them

Contributors
============

By order of contribution date:

  - `Florent Aide`_

.. _Florent Aide: https://bitbucket.org/faide
