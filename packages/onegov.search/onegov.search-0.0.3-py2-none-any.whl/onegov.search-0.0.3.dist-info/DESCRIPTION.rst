
Run the Tests
-------------

Install tox and run it::

    pip install tox
    tox

Limit the tests to a specific python version::

    tox -e py27

Conventions
-----------

Onegov Search follows PEP8 as close as possible. To test for it run::

    tox -e pep8

Onegov Search uses `Semantic Versioning <http://semver.org/>`_

Build Status
------------

.. image:: https://travis-ci.org/OneGov/onegov.search.png
  :target: https://travis-ci.org/OneGov/onegov.search
  :alt: Build Status

Coverage
--------

.. image:: https://coveralls.io/repos/OneGov/onegov.search/badge.png?branch=master
  :target: https://coveralls.io/r/OneGov/onegov.search?branch=master
  :alt: Project Coverage

Latests PyPI Release
--------------------
.. image:: https://pypip.in/v/onegov.search/badge.png
  :target: https://crate.io/packages/onegov.search
  :alt: Latest PyPI Release

License
-------
onegov.search is released under GPLv2

Changelog
---------

Unreleased
~~~~~~~~~~

0.0.3 (2015-09-18)
~~~~~~~~~~~~~~~~~~~

- No longer require elasticsearch to run when configuring the application.
  [href]

0.0.2 (2015-09-18)
~~~~~~~~~~~~~~~~~~~

- Adds the ability to reindex all elasticsearch records.
  [href]

- Fixes a number of issues with the onegov.town integration.
  [href]

0.0.1 (2015-09-17)
~~~~~~~~~~~~~~~~~~~

- Initial Release


