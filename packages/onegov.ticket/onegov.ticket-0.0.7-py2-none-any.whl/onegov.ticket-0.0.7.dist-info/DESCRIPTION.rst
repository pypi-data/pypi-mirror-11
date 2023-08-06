
Run the Tests
-------------

Install tox and run it::

    pip install tox
    tox

Limit the tests to a specific python version::

    tox -e py27

Conventions
-----------

Onegov Ticket follows PEP8 as close as possible. To test for it run::

    tox -e pep8

Onegov Ticket uses `Semantic Versioning <http://semver.org/>`_

Build Status
------------

.. image:: https://travis-ci.org/OneGov/onegov.ticket.png
  :target: https://travis-ci.org/OneGov/onegov.ticket
  :alt: Build Status

Coverage
--------

.. image:: https://coveralls.io/repos/OneGov/onegov.ticket/badge.png?branch=master
  :target: https://coveralls.io/r/OneGov/onegov.ticket?branch=master
  :alt: Project Coverage

Latests PyPI Release
--------------------
.. image:: https://pypip.in/v/onegov.ticket/badge.png
  :target: https://crate.io/packages/onegov.ticket
  :alt: Latest PyPI Release

License
-------
onegov.ticket is released under GPLv2

Changelog
---------

Unreleased
~~~~~~~~~~

0.0.7 (2015-09-01)
~~~~~~~~~~~~~~~~~~~

- Adds the ability to filter the tickets collection by handler.
  [href]

0.0.6 (2015-08-28)
~~~~~~~~~~~~~~~~~~~

- Adds the ability to delete the data behind a handler, creating a snapshot
  before that happens.
  [href]

- The always run upgrade won't show up in the onegov.core upgrade output
  anymore. Eventually we will remove this upgrade task.
  [href]

0.0.5 (2015-07-16)
~~~~~~~~~~~~~~~~~~~

- Reopening a ticket changes its state to pending.
  [href]

0.0.4 (2015-07-15)
~~~~~~~~~~~~~~~~~~~

- Adds a ticket counting function.
  [href]

0.0.3 (2015-07-15)
~~~~~~~~~~~~~~~~~~~

- Adds an email property to the handler.
  [href]

- Adds reopen ticket function.
  [msom]

0.0.2 (2015-07-14)
~~~~~~~~~~~~~~~~~~~

- Adds a handler_id to easily query for a handler record.
  [href]

- Adds accept/close ticket functions.
  [href]

- Adds a ticket collection that supports pagination and filter.
  [href]

0.0.1 (2015-07-10)
~~~~~~~~~~~~~~~~~~~

- Initial Release


