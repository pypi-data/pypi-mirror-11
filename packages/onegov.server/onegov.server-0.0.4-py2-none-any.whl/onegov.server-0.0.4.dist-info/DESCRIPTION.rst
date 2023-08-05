
Run the Tests
-------------

Install tox and run it::

    pip install tox
    tox

Limit the tests to a specific python version::

    tox -e py27

Conventions
-----------

Onegov Server follows PEP8 as close as possible. To test for it run::

    tox -e pep8

Onegov Server uses `Semantic Versioning <http://semver.org/>`_

Build Status
------------

.. image:: https://travis-ci.org/OneGov/onegov.server.png
  :target: https://travis-ci.org/OneGov/onegov.server
  :alt: Build Status

Coverage
--------

.. image:: https://coveralls.io/repos/OneGov/onegov.server/badge.png?branch=master
  :target: https://coveralls.io/r/OneGov/onegov.server?branch=master
  :alt: Project Coverage

Latests PyPI Release
--------------------
.. image:: https://pypip.in/v/onegov.server/badge.png
  :target: https://crate.io/packages/onegov.server
  :alt: Latest PyPI Release

License
-------
onegov.server is released under GPLv2

Changelog
---------

Unreleased
~~~~~~~~~~

0.0.4 (2015-07-16)
~~~~~~~~~~~~~~~~~~~

- Adds the ability to load yaml configs from string.
  [href]

- Remove support for Python 3.3.
  [href]

0.0.3 (2015-06-26)
~~~~~~~~~~~~~~~~~~~

- Adds the ability to disable morepath autoconfig.
  [href]

- Pressing Ctrl+T in the onegov-server cli will now show a memory summary. This
  is helpful for determening if there are memory leaks or not.
  [href]

- Improves the debug server output, highlighting slow requests and dimming out
  redirects.
  [href]

- Include Morepath's upcoming changes to module imports until Morepath 0.11
  is released.
  [href]

0.0.2 (2015-04-30)
~~~~~~~~~~~~~~~~~~~

- Fixes onegov-server being unable to start when the packages are not stored
  as eggs.

  This fix might be unnnecessary in the future:
  https://github.com/morepath/morepath/issues/319

  [href]

0.0.1 (2015-04-29)
~~~~~~~~~~~~~~~~~~~

- Initial Release [href]


