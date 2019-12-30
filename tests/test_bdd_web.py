# -*- coding: utf-8 -*-


def test_bar_fixture(testdir):
    """Make sure that pytest accepts our fixture."""

    # create a temporary pytest test module
    testdir.makepyfile("""
        import pytest
        from pytest_bdd import scenarios
        from flask import Flask as _Flask
        import os
        import pytest_bdd_web

        scenarios('simple.feature')

        class Flask(_Flask):
            testing = True
            secret_key = "test key"

        @pytest.fixture
        def app():
            app = Flask("flask_test", root_path=os.path.dirname(__file__))
            @app.route("/", methods=["GET", "POST"])
            def index():
                return '<div id="main_title">Welcome</div>'
            return app

        @pytest.fixture
        def client(app):
            return app.test_client()

        @pytest.fixture
        def url_mapping():
            return {
                'home': {
                    'list': '/',
                    },
            };
    """)

    testdir.makefile(".feature", simple="""
        Feature: Homepage functionality
            Scenario: Homepage
                When the user requests list home
                Then response 0 status code is "200"
                And response 0 element "#main_title" contains 'Welcome'
    """)

    # run pytest with the following cmd args
    result = testdir.runpytest(
        '-v'
    )

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*::test_homepage PASSED*',
    ])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0
