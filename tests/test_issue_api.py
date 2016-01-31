# -- encoding: UTF-8 --
import pytest
from django.core.urlresolvers import reverse
from django.utils.crypto import get_random_string
from tests.utils import get_response_data
from wurst.models import Issue


@pytest.mark.django_db
def test_issue_create_api(basic_schema, project, admin_api_client):
    title = "Say %s!" % get_random_string()
    resp = get_response_data(admin_api_client.post(reverse("v1:issue-list"), data={
        "project": "test",
        "title": title,
        "type": "task"
    }), status_code=201)
    assert Issue.objects.get(pk=resp["id"]).title == title
