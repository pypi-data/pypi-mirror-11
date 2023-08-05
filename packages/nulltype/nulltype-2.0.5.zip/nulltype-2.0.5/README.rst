
| |version| |downloads| |supported-versions| |supported-implementations|


.. |version| image:: http://img.shields.io/pypi/v/nulltype.png?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/nulltype

.. |downloads| image:: http://img.shields.io/pypi/dm/nulltype.png?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/nulltype

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/nulltype.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/nulltype

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/nulltype.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/nulltype

Helps define 'null' types different from, but parallel to, ``None``.

``None`` is a great `sentinel value <http://en.wikipedia.org/wiki/Sentinel_value>`_
and a classic implementation of the
`null object pattern <http://en.wikipedia.org/wiki/Null_Object_pattern>`_.

But there are times that you need more than one nullish value to
represent different aspects of emptiness. "Nothing there" is
logically different from "undefined," "prohibited,"
"end of data" and other kinds of null.

The core function of ``nulltype``
is representing emptiness and falsity in a way that doesn't overload ``None``
(or ``False``, ``0``, ``{}``, ``[]`` or any of the other possible
"there's nothing here!") values.
It helps create designated identifiers with specific meanings
such as ``Passthrough``, ``Prohibited``, and ``Undefined``.

Usage
=====

::

    from nulltype import NullType

    Empty = NullType('Empty')

    # following just to show it's working
    assert bool(Empty) == False
    assert len(Empty) == 0
    assert list(Empty) == []
    assert Empty.some_attribute is Empty
    assert Empty[22] is Nothing
    assert Empty("hey", 12) is Empty

That created a custom ``NullType``. You can create as many
of them as you like. For your convenience, two default
values, ``Null`` and ``Nothing``, are exported. That way,
if you don't really want to create your own, you can
import a pre-constituted null value, such as::

    from nulltype import Nothing

Dereferencing
=============

Alternate null types can be particularly useful when parsing
data or traversing data structures which might or might not be
present. This is common in dealing with the data returned by
`REST <http://en.wikipedia.org/wiki/Representational_state_transfer>`_
APIs, for instance.

As one example, `the documentation for Google's Gmail API <https://developers.google.com/gmail/api/quickstart/quickstart-python>`_
suggests the following code::


    threads = gmail_service.users().threads().list(userId='me').execute()
    if threads['threads']:
        for thread in threads['threads']:
            print 'Thread ID: %s' % (thread['id'])

But there is a lot going on there to avoid a problematic dereference.
If instead you have a ``Nothing`` null type defined, the code is
shorter (and avoids an extra, very transient variable)::

    results = gmail_service.users().threads().list(userId='me').execute()
    for thread in results.get('threads', Nothing):
        print 'Thread ID: %s' % (thread['id'])

This model of "go ahead, get it if you can" works well for
chains of access as well::

    results.get("payload", Nothing).get("headers", Nothing)

Will return the correct object if it's there, but ``Nothing`` otherwise.
And if you then try to test it (e.g. with ``if`` or a logical expression)
or iterate over it (e.g. with ``for``), it will act as though it's an empty list.

``Nothing`` isn't nothing. It's something that will simplify your code.

Uniqueness
==========

``NullType`` instances are meant to be
`singletons <http://en.wikipedia.org/wiki/Singleton_pattern>`_, with just one per
program. They almost are, though technically multiple ``NullType`` instances are
reasonable, making it more of a `multiton
pattern <http://en.wikipedia.org/wiki/Multiton_pattern>`_.

The uniqueness of each singleton is currently not enforced, making it a usage
convention rather than strict law. With even minimal care, this is a problem
roughly 0% of the time.

Notes
=====

 * Similar modules include `sentinels <http://pypi.python.org/pypi/sentinels>`_ and `null
   <http://pypi.python.org/pypi/null>`_. Of these, I prefer ``sentinels`` because it
   is clearly Python 3 ready, includes a ``pickle`` mechanism.

 * The author, `Jonathan Eunice <mailto:jonathan.eunice@gmail.com>`_ or
   `@jeunice on Twitter <http://twitter.com/jeunice>`_
   welcomes your comments and suggestions.

Recent Changes
==============

 *  Version 2.0 starts major upgrade from just Boolean operations being nulled
    to essentially all sorts of accesses and updates being nulled. It defines two
    default ``NullType`` instances, ``Null`` and ``Nothing``. The ability
    to have anonymous (unnamed) nulls has been removed as superfluous.

 *  Automated multi-version testing managed with the wonderful
    `pytest <http://pypi.python.org/pypi/pytest>`_,
    `pytest-cov <http://pypi.python.org/pypi/pytest>`_,
    and `tox <http://pypi.python.org/pypi/tox>`_.
    Successfully packaged for, and tested against, all late-model versions of
    Python: 2.6, 2.7, 3.2, 3.3, 3.4, as well as PyPy 2.5.1 (based on 2.7.9)
    and PyPy3 2.4.0 (based on 3.2.5).

 *  The author, `Jonathan Eunice <mailto:jonathan.eunice@gmail.com>`_ or
    `@jeunice on Twitter <http://twitter.com/jeunice>`_
    welcomes your comments and suggestions.

Installation
============

::

    pip install -U nulltype

To ``easy_install`` under a specific Python version (3.3 in this example)::

    python3.3 -m easy_install nulltype

(You may need to prefix these with ``sudo`` to authorize installation. In
environments without super-user privileges, you may want to use ``pip``'s
``--user`` option, to install only for a single user, rather than
system-wide.)
