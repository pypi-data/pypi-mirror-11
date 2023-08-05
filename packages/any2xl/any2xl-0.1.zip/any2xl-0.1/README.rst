Introduction
============

`any2xl`_ is a helper module to ease producing XLS(X) files from different
sources. It uses `openpyxl`_ by Eric Gazoni to produce the actual XLS file.
It provides primitives and helpers alongside with `any2`_ that help produce
XLS(X)
files from diverse sources.

Licence
=======

This package is covered by the permissive BSD licence.

Python versions
===============

any2xl works on python 2.7 and python 3.4

Example Usage
=============

::

    from datetime import datetime as dt
    from decimal import Decimal
    from any2xl import List2xl

    target_filename = "out.xls"

    data = [
        (dt.now(), Decimal("15.3"), u'Noël'),
        (dt.now(), Decimal("10.3"), u'Pentecôte'),
        (dt.now(), Decimal("100.02"), u'Jérôme'),
        (dt.now(), Decimal("0.03"), u'Some unaccented data'),
    ]

    colnames = ["Time", "Amount", "Description"]

    # we want column names as the first line of our XLS file
    # so we give the names to the constructor
    xl = List2xl(target_filename, colnames=colnames)

    # and we ask the write method to write the names
    xl.write(data, write_names=True)

    # serialize to disk
    xl.finalize()

In this example we only act as a really thin wrapper over the openpyxl
library and if you only need this kind of functionality you may be better off
using directly openpyxl...

The purpose of any2xl and were it is really interesting is when you have more
complex datastructures::

    from decimal import Decimal
    import datetime

    from any2xl import List2xl
    from any2 import Obj2List
    from any2 import NameTransformer

    quantizer = Decimal('0.01')


    class SubObj(object):
        def __init__(self, v):
            self.amount = Decimal('42.4242424242')
            self.start_date = datetime.date(year=2001, month=2, day=3)
            self.description = "%s_%s" % ("Task", v)


    class MyObj(object):
        def __init__(self, v, urgent):
            self.description = v
            self.urgent = urgent
            self.subobj = SubObj(v)


    def quantize2(value):
        return value.quantize(quantizer)

    def yesno(value):
        if value:
            return "Yes"
        else:
            return "No"

    vals = [('Project 1', True), ('Project 2', False), ('Project 3', False)]
    objs = [MyObj(*val) for val in vals]

    # the name transformer will work on output columns
    # in fact indexes...
    colnames = [
        "Start Date",
        "Amount",
        "Description",
        "Task Description",
        "Is Urgent"
    ]
    transformer = NameTransformer(colnames)
    transformer.register_func('Amount', quantize2)
    transformer.register_func('Is Urgent', yesno)

    # to adapt an object as a list we must give the list of attributes we want
    attrs = [
        'subobj.start_date',
        'subobj.amount',
        'description',
        'subobj.description',
        'urgent'
    ]
    data_feed = Obj2List(objs, attrs, transformer=transformer)

    xl = List2xl('obj2list_out.xls', colnames=colnames)
    xl.write(data_feed, write_names=True)
    xl.finalize()


Here you see that we have a (somewhat complex) input iterator yielding
imbricated objects and we need to transform some of the data during the
process.

We could have used other transformers, the list is in any2.transformers

Plans
=====

  - Adding unit tests is our main priority, the main functionalities are in
    `any2`_ which is 100% test covered. So we only need to add the thin wrapper
    above openpyxl in our unit tests
  - At the moment we can only produce "raw" xls files without formatting. We
    plan to introduce new xl specific formatters to be able to apply cell and
    row formattings in the same way we use transformers.

Changelog
=========

0.1 Jul. 29 2015
~~~~~~~~~~~~~~~~

    - Initial release

Contributors
============

By order of contribution date:

    - `Florent Aide`_

.. _Florent Aide: https://bitbucket.org/faide
.. _any2: https://bitbucket.org/faide/any2
.. _any2xl: https://bitbucket.org/faide/any2xl
.. _openpyxl: https://openpyxl.readthedocs.org/en/latest/
