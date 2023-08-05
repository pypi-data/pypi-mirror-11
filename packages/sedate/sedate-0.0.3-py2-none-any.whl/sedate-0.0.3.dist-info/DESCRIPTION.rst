
There are projects like `Arrow <https://github.com/crsmithdev/arrow>`_ or
`Delorean <https://github.com/crsmithdev/arrow>`_ which provide ways to work
with timezones without having to think about it too much.

Seantis doesn't use them because we *want* to reason about these things,
to ensure they are correct, and partly because of self-loathing.

Adding another layer makes this reasoning harder.

Run the Tests
-------------

Install tox and run it::

    pip install tox
    tox

Limit the tests to a specific python version::

    tox -e py27

Conventions
-----------

Sedate follows PEP8 as close as possible. To test for it run::

    tox -e pep8

Sedate uses `Semantic Versioning <http://semver.org/>`_

Build Status
------------

.. image:: https://travis-ci.org/seantis/sedate.png
  :target: https://travis-ci.org/seantis/sedate
  :alt: Build Status

Coverage
--------

.. image:: https://coveralls.io/repos/seantis/sedate/badge.png?branch=master
  :target: https://coveralls.io/r/seantis/sedate?branch=master
  :alt: Project Coverage

Latests PyPI Release
--------------------
.. image:: https://pypip.in/v/sedate/badge.png
  :target: https://crate.io/packages/sedate
  :alt: Latest PyPI Release

License
-------
sedate is released under GPLv2

Changelog
---------

Unreleased
~~~~~~~~~~

0.0.3 (2015-08-05)
~~~~~~~~~~~~~~~~~~~

- Adds a function to turn date-ish objects into datetimes.
  [href]

0.0.2 (2015-08-04)
~~~~~~~~~~~~~~~~~~~

- Fix align_date_to_day failing with certain timezones.
  [href]

0.0.1 (2015-06-30)
~~~~~~~~~~~~~~~~~~~

- Initial Release


