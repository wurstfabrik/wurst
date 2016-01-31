# -- encoding: UTF-8 --
import json

from django.test import SimpleTestCase

_dummy_test_case = SimpleTestCase(methodName="setUp")


def assert_response_contains(response, text, **kwargs):
    _dummy_test_case.assertContains(response=response, text=text, **kwargs)


def assert_response_does_not_contain(response, text, **kwargs):
    _dummy_test_case.assertNotContains(response=response, text=text, **kwargs)


def get_response_data(response, status_code=200):
    if status_code:  # pragma: no branch
        assert response.status_code == status_code, (
            "Status code %s is not the expected %s" % (response.status_code, status_code)
        )
    return json.loads(response.content.decode('utf-8'))
