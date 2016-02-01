import pytest

from wurst.cli import Context, CreateCommand, SetCommand
from wurst.core.models import Issue, IssueType, Priority


@pytest.mark.django_db
def test_build_context(basic_schema):
    context = Context()
    critical = Priority.objects.get(slug='critical')
    task = IssueType.objects.get(slug='task')

    parts = context.enrich_command('new critical task "Turn Japsu\'s crude prototype into an actual parser"')

    assert list(parts) == [
        CreateCommand,
        critical,
        task,
        "Turn Japsu's crude prototype into an actual parser"
    ]


@pytest.mark.django_db
def test_multiple_commands():
    parts = Context().enrich_command('new new new')
    assert list(parts) == [
        CreateCommand,
        "new",
        "new"
    ]


@pytest.mark.django_db
def test_issue_parse(basic_schema, project):
    issue = Issue.objects.create(project=project, type=basic_schema["type"]["task"], title="Hello")
    parts = Context().enrich_command('set %s crit' % issue.key)
    assert list(parts) == [
        SetCommand,
        issue,
        basic_schema["priority"]["critical"]
    ]
