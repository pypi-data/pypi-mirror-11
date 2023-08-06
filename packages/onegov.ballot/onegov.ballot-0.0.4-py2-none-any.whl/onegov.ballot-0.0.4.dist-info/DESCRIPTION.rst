
Run the Tests
-------------

Install tox and run it::

    pip install tox
    tox

Limit the tests to a specific python version::

    tox -e py27

Conventions
-----------

Onegov Ballot follows PEP8 as close as possible. To test for it run::

    tox -e pep8

Onegov Ballot uses `Semantic Versioning <http://semver.org/>`_

Build Status
------------

.. image:: https://travis-ci.org/OneGov/onegov.ballot.png
  :target: https://travis-ci.org/OneGov/onegov.ballot
  :alt: Build Status

Coverage
--------

.. image:: https://coveralls.io/repos/OneGov/onegov.ballot/badge.png?branch=master
  :target: https://coveralls.io/r/OneGov/onegov.ballot?branch=master
  :alt: Project Coverage

Latests PyPI Release
--------------------
.. image:: https://pypip.in/v/onegov.ballot/badge.png
  :target: https://crate.io/packages/onegov.ballot
  :alt: Latest PyPI Release

License
-------
onegov.ballot is released under GPLv2

Changelog
---------

Unreleased
~~~~~~~~~~

0.0.4 (2015-08-31)
~~~~~~~~~~~~~~~~~~~

- Renames the "yays" to "yeas", the correct spelling.

0.0.3 (2015-06-26)
~~~~~~~~~~~~~~~~~~~

- Remove support for Python 3.3.
  [href]

- Adds support for onegov.core.upgrade.
  [href]

0.0.2 (2015-06-19)
~~~~~~~~~~~~~~~~~~~

- Each ballot result now needs a municipality id, a.k.a BFS-Nummer.
  [href]

0.0.1 (2015-06-18)
~~~~~~~~~~~~~~~~~~~

- Initial Release


