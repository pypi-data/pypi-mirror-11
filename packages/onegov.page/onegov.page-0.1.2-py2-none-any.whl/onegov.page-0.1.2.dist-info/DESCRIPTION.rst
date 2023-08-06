
Run the Tests
-------------

Install tox and run it::

    pip install tox
    tox

Limit the tests to a specific python version::

    tox -e py27

Conventions
-----------

Onegov Page follows PEP8 as close as possible. To test for it run::

    tox -e pep8

Onegov Page uses `Semantic Versioning <http://semver.org/>`_

Build Status
------------

.. image:: https://travis-ci.org/OneGov/onegov.page.png
  :target: https://travis-ci.org/OneGov/onegov.page
  :alt: Build Status

Coverage
--------

.. image:: https://coveralls.io/repos/OneGov/onegov.page/badge.png?branch=master
  :target: https://coveralls.io/r/OneGov/onegov.page?branch=master
  :alt: Project Coverage

Latests PyPI Release
--------------------
.. image:: https://pypip.in/v/onegov.page/badge.png
  :target: https://crate.io/packages/onegov.page
  :alt: Latest PyPI Release

License
-------
onegov.page is released under GPLv2

Changelog
---------

Unreleased
~~~~~~~~~~

0.1.2 (2015-08-28)
~~~~~~~~~~~~~~~~~~~

- Moved most code out to onegov.core for similar modules to use.
  [href]

0.1.1 (2015-06-26)
~~~~~~~~~~~~~~~~~~~

- Adds support for onegov.core.upgrade
  [href]

- Remove support for Python 3.3.
  [href]

0.1.0 (2015-05-07)
~~~~~~~~~~~~~~~~~~~

- Adds a page type column which may be used for polymorphic identites.
  [href]

0.0.1 (2015-04-29)
~~~~~~~~~~~~~~~~~~~

- Initial Release [href]


