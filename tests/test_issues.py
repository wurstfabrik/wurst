import pytest

from wurst.core.consts import StatusCategory
from wurst.core.models import Issue, IssueType, Priority, Status


@pytest.mark.django_db
def test_issue_creation(basic_schema, project):
    i = Issue.objects.create(
        project=project,
        type=basic_schema["type"]["task"]
    )
    assert i.key.startswith(project.prefix)


@pytest.mark.django_db
def test_issue_transitions(basic_schema, project):
    i = Issue.objects.create(
        project=project,
        type=basic_schema["type"]["task"]
    )
    stati = basic_schema["status"]
    assert i.status == stati["todo"]
    i.transition("in-progress")
    i.transition("in-progress")  # exercise the no-op case
    assert i.status == stati["progress"]
    i.transition("todo")
    assert i.status == stati["todo"]
    i.transition("progress")
    assert i.status == stati["progress"]
    i.transition("done")
    assert i.status == stati["done"]


@pytest.mark.django_db
def test_issue_transitions_without_workflow(project):
    type = IssueType.objects.create(name="blep")
    Priority.objects.create(name="blep")
    with pytest.raises(ValueError):  # missing status, this oughta raise
        Issue.objects.create(project=project, type=type)
    open = Status.objects.create(name="open", category=StatusCategory.OPEN)
    closed = Status.objects.create(name="close", category=StatusCategory.CLOSED)
    i = Issue.objects.create(project=project, type=type)
    assert i.status == open
    i.transition("close")
    i.transition(closed)  # exercise the not-looking-up-via-slug route

