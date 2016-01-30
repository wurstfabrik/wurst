import pytest

from wurst.models import Issue


@pytest.mark.django_db
def test_issue_creation(basic_schema, project):
    i = Issue.objects.create(
        project=project,
        type=basic_schema["type"]["task"]
    )
    assert i.key.startswith(project.prefix)
