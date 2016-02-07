# -- encoding: UTF-8 --
import pytest
from reversion import revisions as reversion
from django.core.urlresolvers import reverse
from django.utils.crypto import get_random_string
from tests.utils import get_response_data
from wurst.core.models import Issue


@pytest.mark.django_db
def test_issue_create_api(basic_schema, project, admin_api_client):
    title = "Say %s!" % get_random_string()
    resp = get_response_data(admin_api_client.post(reverse("v1:issue-list"), data={
        "project": "test",
        "title": title,
        "type": "task"
    }), status_code=201)
    assert Issue.objects.get(pk=resp["id"]).title == title


@pytest.mark.django_db
def test_issue_patch_api(basic_schema, project, admin_api_client):
    title = "Say %s!" % get_random_string()
    resp = get_response_data(admin_api_client.post(reverse("v1:issue-list"), data={
        "project": "test",
        "title": title,
        "type": "task"
    }), status_code=201)
    resp = get_response_data(admin_api_client.patch(reverse("v1:issue-detail", kwargs={"pk": resp["id"]}), data={
        "title": "nnep"
    }), status_code=200)
    issue = Issue.objects.get(pk=resp["id"])
    assert issue.title == "nnep"
    assert reversion.get_for_object(issue).count() == 2


@pytest.mark.django_db
def test_issue_comments_api(basic_schema, project, admin_api_client):
    issue = Issue.objects.create(project=project, title="durr", type=basic_schema["type"]["task"])
    # Add comments:
    for x in range(5):
        resp = get_response_data(admin_api_client.post(reverse("v1:comment-list"), data={
            "issue": issue.pk,
            "text": "hey hey hey",
        }), status_code=201)
    # Patch the last comment:
    resp = get_response_data(admin_api_client.patch(reverse("v1:comment-detail", kwargs={"pk": resp["id"]}), data={
        "text": "nnep"
    }), status_code=200)
    assert issue.comments.count() == 5
    resp = get_response_data(
        admin_api_client.get(reverse("v1:issue-detail", kwargs={"pk": issue.pk}))
    )
    assert len(resp["comments"]) == 5
    assert resp["comments"][0]["text"] == "hey hey hey"
    assert resp["comments"][-1]["text"] == "nnep"


@pytest.mark.django_db
def test_issue_transition_api(basic_schema, project, admin_api_client):
    title = "Say %s!" % get_random_string()
    resp = get_response_data(admin_api_client.post(reverse("v1:issue-list"), data={
        "project": "test",
        "title": title,
        "type": "task"
    }), status_code=201)

    issue_url = reverse("v1:issue-detail", kwargs={"pk": (resp["id"])})
    get_response_data(admin_api_client.patch(issue_url, data={
        "status": "done"
    }), status_code=400)
    resp = get_response_data(admin_api_client.patch(issue_url, data={
        "transition": "in-progress"
    }), status_code=200)
    issue = Issue.objects.get(pk=resp["id"])
    assert issue.status.slug == "progress"
