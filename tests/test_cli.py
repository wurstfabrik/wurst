import pytest

from wurst.cli import Context, create, wurst
from wurst.core.models import IssueType, Priority


@pytest.mark.django_db
def test_build_context(basic_schema):
    context = Context()
    critical = Priority.objects.get(slug='critical')
    task = IssueType.objects.get(slug='task')

    parts = context.enrich_command('wurst new critical task "Turn Japsu\'s crude prototype into an actual parser"')

    assert parts == [
        wurst,
        create,
        critical,
        task,
        "Turn Japsu's crude prototype into an actual parser"
    ]
