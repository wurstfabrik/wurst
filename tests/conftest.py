import os

import pytest

from wurst.consts import StatusCategory
from wurst.models import Project, IssueType, Priority, Status
from wurst.utils.schema_import import SchemaImporter

BASIC_SCHEMA_DATA = {
    'status': [{'name': 'To Do'}, {'name': 'In Progress'}, {'name': 'Done', 'category': 1}],
    'type': [{'name': 'Task'}],
    'priority': [
        {'name': 'Low', 'value': -10}, {'name': 'Normal', 'value': 0},
        {'name': 'High', 'value': 50}, {'name': 'Critical', 'value': 100}
    ]
}


@pytest.mark.django_db
@pytest.fixture
def basic_schema():
    schi = SchemaImporter()
    schi.import_from_data(BASIC_SCHEMA_DATA)
    return schi.objects


@pytest.mark.django_db
@pytest.fixture
def project():
    return Project.objects.get_or_create(name="Test", slug="test", prefix="T-")[0]


@pytest.mark.django_db
@pytest.fixture
def task_type():
    return IssueType.objects.get_or_create(name="Task", slug="task")[0]


@pytest.mark.django_db
@pytest.fixture
def normal_priority():
    return Priority.objects.get_or_create(name="Normal", slug="normal")[0]


@pytest.mark.django_db
@pytest.fixture
def todo_status():
    return Status.objects.get_or_create(name="To Do", slug="to-do")[0]


@pytest.mark.django_db
@pytest.fixture
def done_status():
    return Status.objects.get_or_create(name="Done", slug="done", category=StatusCategory.DONE)[0]


@pytest.mark.django_db
@pytest.fixture
def closed_status():
    return Status.objects.get_or_create(name="Closed", slug="closed", category=StatusCategory.CLOSED)[0]
