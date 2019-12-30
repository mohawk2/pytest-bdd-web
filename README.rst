==============
pytest-bdd-web
==============

.. image:: https://img.shields.io/pypi/v/pytest-bdd-web.svg
    :target: https://pypi.org/project/pytest-bdd-web
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pytest-bdd-web.svg
    :target: https://pypi.org/project/pytest-bdd-web
    :alt: Python versions

.. image:: https://travis-ci.org/mohawk2/pytest-bdd-web.svg?branch=master
    :target: https://travis-ci.org/mohawk2/pytest-bdd-web
    :alt: See Build Status on Travis CI

.. image:: https://ci.appveyor.com/api/projects/status/github/mohawk2/pytest-bdd-web?branch=master
    :target: https://ci.appveyor.com/project/mohawk2/pytest-bdd-web/branch/master
    :alt: See Build Status on AppVeyor

pytest plugin providing a BDD 'language' for web app integration-testing.

----

Features
--------

Implements a simple headless browser that requests web pages according
to a URL mapping, parses web forms, and enables assertions about
the various web responses using PyQuery selectors (similar to jQuery).

Example::

    Feature: Homepage functionality
        Scenario: Homepage
            When the user requests list home
            Then response 0 status code is "200"
            And response 0 element "#main_title" contains 'Welcome'

        Scenario: User profile
            When the user requests view user_profile
            Then response 0 status code is "200"
            And response 0 element "tr:contains('Balance')" contains '45.67'
            And response 0 form-contains-array-outline <arrayfield> <arrayvalue>

            Examples:
            | arrayfield | arrayvalue |
            | choices    | [0 2 3]    |


Requires you to provide these fixtures:

    * client
    * url_mapping

`client` must implement `get` and `post` methods, compatible with
`Flask.test_client`.

Example::

    @pytest.fixture
    def app():
        """Create, configure a new app instance for each test."""
        "..."
        return app

    @pytest.fixture
    def client(app):
        return app.test_client()

`url_mapping` must be a dictionary, with keys of top-level "groups",
and values mapping a human-readable "action" to an absolute URL in
your web app.

Example::

    URL_MAPPING = {
        'home': {
            'list': '/',
            'articles': '/latest/',
        },
        'user_profile': {
            'view': '/user/profile/',
            'update': '/user/profile/update',
        },
        'blog': {
            'delete': '/blog/{}/delete', # {} gets filled from feature args
        },
    };
    @pytest.fixture
    def url_mapping():
        return URL_MAPPING



Requirements
------------

PyQuery, pytest-bdd, mechanize


Installation
------------

You can install "pytest-bdd-web" via `pip`_ from `PyPI`_::

    $ pip install pytest-bdd-web


Contributing
------------
Contributions are very welcome. Tests can be run with `tox`_, please ensure
the coverage at least stays the same before you submit a pull request.

License
-------

Distributed under the terms of the `MIT`_ license, "pytest-bdd-web" is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`MIT`: http://opensource.org/licenses/MIT
.. _`file an issue`: https://github.com/mohawk2/pytest-bdd-web/issues
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project
