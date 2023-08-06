
Run the Tests
-------------

Install tox and run it::

    pip install tox
    tox

Limit the tests to a specific python version::

    tox -e py27

Conventions
-----------

Onegov People follows PEP8 as close as possible. To test for it run::

    tox -e pep8

Onegov People uses `Semantic Versioning <http://semver.org/>`_

Build Status
------------

.. image:: https://travis-ci.org/OneGov/onegov.people.png
  :target: https://travis-ci.org/OneGov/onegov.people
  :alt: Build Status

Coverage
--------

.. image:: https://coveralls.io/repos/OneGov/onegov.people/badge.png?branch=master
  :target: https://coveralls.io/r/OneGov/onegov.people?branch=master
  :alt: Project Coverage

Latests PyPI Release
--------------------
.. image:: https://pypip.in/v/onegov.people/badge.png
  :target: https://crate.io/packages/onegov.people
  :alt: Latest PyPI Release

License
-------
onegov.people is released under GPLv2

Changelog
---------

Unreleased
~~~~~~~~~~

0.0.3 (2015-08-24)
~~~~~~~~~~~~~~~~~~~

- Adds compatibility with onegov.core 0.4.25
  [href]

0.0.2 (2015-08-18)
~~~~~~~~~~~~~~~~~~~

- Renames 'academic_title' to the more general 'salutation'. This requires
  a onegov-core upgrade run to migrate existing databases.
  [href]

- Removes Gravatar support.
  [href]

0.0.1 (2015-07-03)
~~~~~~~~~~~~~~~~~~~

- Initial Release


