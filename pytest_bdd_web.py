# -*- coding: utf-8 -*-

"""pytest plugin providing a BDD 'language' for web app integration-testing.

Implements a simple headless browser that requests web pages according
to a URL mapping, parses web forms, and enables assertions about
the various web responses using PyQuery selectors (similar to jQuery).

Example:
    Feature: Homepage functionality
        Scenario: Homepage
            When the user requests list home
            Then response 0 status code is "200"
            And response 0 element "#main_title" contains 'Welcome'

        Scenario: User profile
            When the user requests view user_profile
            And the user sets-array choices [1 3 4]
            And the user submits update user_profile
            Then response 0 status code is "200"
            And response 0 element "tr:contains('Balance')" contains '45.67'
            And response 0 form-contains-array-outline <arrayfield> <arrayvalue>
            And response 1 status code is "200"
            And response 1 shows element "div.success"
            And response 1 doesn't show element "div.alert"

            Examples:
            | arrayfield | arrayvalue |
            | choices    | [0 2 3]    |

Requires you to provide these fixtures:

    * client
    * url_mapping

`client` must implement `get` and `post` methods, compatible with
`Flask.test_client`.

Example:
    @pytest.fixture
    def app():
        \"""Create, configure a new app instance for each test.\"""
        "..."
        return app

    @pytest.fixture
    def client(app):
        return app.test_client()

`url_mapping` must be a dictionary, with keys of top-level "groups",
and values mapping a human-readable "action" to an absolute URL in
your web app.

Example:
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
"""

__version__ = '0.1.0'

import pytest
from pytest_bdd import when, then, parsers
from pytest_bdd.steps import inject_fixture
from pyquery import PyQuery as pq

def _formdata_from_html(html):
    import mechanize
    br = mechanize.Browser()
    br.set_html(html, url=None)
    filtered_forms = [f for f in br.forms() if f.action is None]
    if len(filtered_forms) != 1:
        return None
    return { c.name: c.value for c in filtered_forms[0].controls }

"""Used in mutable fashion. With 'when'.target_fixture, should use immutable"""
@pytest.fixture
def _responses():
    return []

@pytest.fixture
def _form_data():
    """Session state, needed to track form - must zap on new request"""
    return None

def _url_args(url, args):
    args = args.split()
    if len(args):
        url = url.format(*args)
    return url

def _form_request(request, _form_data, client, req, url):
    if req == 'get':
        response = client.get(url, follow_redirects=True)
    else:
        response = client.post(url, data=_form_data, follow_redirects=True)
    if response.status_code != 200:
        assert "{} gave {}".format(url, response.status_code) is None
    inject_fixture(request, '_form_data', _formdata_from_html(response.data))
    return response

# When Steps

@when(parsers.re('the user requests (?P<action>[^ ]+) (?P<what>[^ ]+) ?(?P<args>.*)'))
def response_request(request, _form_data, client, _responses, action, what, args, url_mapping):
    """
    Will operate on the URL looked up from the `url_mapping`, with
    any args substituted in for occurrences of `{}` in the mapped
    URL.

    Example:
        When the user requests view user_profile
    """
    url = _url_args(url_mapping[what][action], args)
    _responses.append(_form_request(request, _form_data, client, 'get', url))

@when(parsers.parse('the user sets {field} "{value}"'))
def form_update_fieldsimple(_form_data, field, value):
    """
    Sets a form value on the current web page.

    Example:
        When the user sets fullname "Big Bob"
    """
    _form_data[field] = value

@when(parsers.parse('the user sets-array {afield} [{avalue}]'))
def form_update_fieldarray(_form_data, afield, avalue):
    """
    Sets a form value on the current web page.

    Example:
        When the user sets-array choices [1 3 4]
    """
    avalue = avalue.split() # string -> list
    _form_data[afield] = avalue

@when('the user sets-array-outline <arrayfield> <arrayvalue>')
def form_update_fieldarray_outline(_form_data, arrayfield, arrayvalue):
    """
    Sets a form value on the current web page.

    Example:
        When the user sets-array-outline <arrayfield> <arrayvalue>

        Examples:
        | arrayfield | arrayvalue |
        | choices    | [0 2 3]    |
    """
    arrayvalue = arrayvalue[1:-1].split() # string -> list
    _form_data[arrayfield] = arrayvalue

@when(parsers.re('the user submits (?P<action>[^ ]+) (?P<what>[^ ]+) ?(?P<args>.*)'))
def user_submit(request, _form_data, url_mapping, client, _responses, action, what, args):
    """
    Will operate on the URL looked up from the `url_mapping`, with
    any args substituted in for occurrences of `{}` in the mapped
    URL.

    Example:
        When the user submits delete blog 4ec2d70
    """
    url = _url_args(url_mapping[what][action], args)
    _responses.append(_form_request(request, _form_data, client, 'post', url))

# Then Steps

@then(parsers.parse('response {response_index:d} status code is "{code:d}"'))
def response_code(_responses, response_index, code):
    """
    Example:
        Then response 0 status code is "200"
    """
    assert _responses[response_index].status_code == code

@then(parsers.parse('response {response_index:d} json-has "{key}"'))
def response_json_contains(_responses, response_index, key):
    """
    Example:
        Then response 0 json-has "account_balance"
    """
    assert key in _responses[response_index].get_json()

@then(parsers.parse('response {response_index:d} json-contains "{key}" "{phrase}"'))
def response_json_contains_value(_responses, response_index, key, phrase):
    """
    Example:
        Then response 0 json-contains "account_balance" "45.67"
    """
    assert phrase in _responses[response_index].get_json()[key]

@then(parsers.parse('response {response_index:d} form-contains-array-outline <arrayfield> <arrayvalue>'))
def response_form_contains_array_outline(_responses, response_index, arrayfield, arrayvalue):
    """
    Then-clause asserting about a given outline form-field having the given
    outline array value.

    Example:
        Then response 0 form-contains-array-outline <arrayfield> <arrayvalue>

        Examples:
        | arrayfield | arrayvalue |
        | choices    | [0 2 3]    |
    """
    arrayvalue = arrayvalue[1:-1].split() # string -> list
    assert arrayvalue == _formdata_from_html(_responses[response_index].data)[arrayfield]

@then(parsers.parse('''response {response_index:d} doesn't show element "{selector}"'''))
def response_notcontains(_responses, response_index, selector):
    """
    Example:
        Then response 0 doesn't show element "div.alert"
    """
    d = pq(_responses[response_index].data)
    p2 = d(selector)
    if not p2: return
    p1 = p2.prev()
    if p1.attr("name"): # form input that actually had the error
        assert "{} {}".format(p1.attr("name"), p2.text()) is None
    else:
        assert p2.text() is None

@then(parsers.parse('''response {response_index:d} shows element "{selector}"'''))
def response_contains(_responses, response_index, selector):
    """
    Example:
        Then response 0 shows element "div.success"
    """
    _elt_contains(_responses[response_index].data, selector, "")

def _elt_contains(html, selector, phrase, invert=False):
    d = pq(html)
    p = d(selector)
    if not p:
        assert f'Element "{selector}" not found' is None
    alltext = p.outerHtml()
    if (phrase in alltext) == (not invert): return
    msg = 'unexpectedly' if invert else 'not'
    assert '"{}" {} found in "{}"'.format(phrase, msg, alltext) is None

@then(parsers.parse('''response {response_index:d} element "{selector}" contains '{phrase}\''''))
def response_selector(_responses, response_index, selector, phrase):
    """
    Example:
        Then response 0 element "#username" contains 'bob'
    """
    _elt_contains(_responses[response_index].data, selector, phrase)

@then(parsers.parse('response {response_index:d} element "{selector}" contains-outline <contains>'))
def response_selector_outline(_responses, response_index, selector, contains):
    """
    Then-clause asserting about a PyQuery-selected element containing an
    outline value.

    Example:
        Then response 0 element "#username" contains-outline <contains>

        Examples:
        | contains |
        | Bob |
    """
    _elt_contains(_responses[response_index].data, selector, contains)

@then(parsers.parse('''response {response_index:d} element "{selector}" doesn't contain '{phrase}\''''))
def response_selector(_responses, response_index, selector, phrase):
    """
    Example:
        Then response 0 element "#username" doesn't contain 'bob'
    """
    _elt_contains(_responses[response_index].data, selector, phrase, invert=True)

@then(parsers.parse('''response {response_index:d} element "{selector}" doesn't contain-outline <contains>'''))
def response_selector_invert_outline(_responses, response_index, selector, contains):
    """
    Then-clause asserting about a PyQuery-selected element not containing an
    outline value.

    Example:
        Then response 0 element "#response" doesn't contain-outline <contains>

        Examples:
        | contains |
        | 0 items added |
    """
    _elt_contains(_responses[response_index].data, selector, contains, invert=True)
