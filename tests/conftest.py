import os

import pytest
import toml
from rest_framework.test import APIClient
from six import StringIO

from wurst.core.consts import StatusCategory
from wurst.core.models import IssueType, Priority, Project, Status
from wurst.core.utils.schema_import import SchemaImporter

BASIC_SCHEMA_PATH = os.path.join(
    os.path.dirname(__file__), "..", "wurst", "core", "schemata", "basic.toml"
)
BASIC_SCHEMA_DATA = toml.load(BASIC_SCHEMA_PATH)


@pytest.mark.django_db
@pytest.fixture
def basic_schema():
    schi = SchemaImporter()
    schi.stdout = StringIO()
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


@pytest.fixture()
def admin_api_client(admin_user):
    api_client = APIClient()
    api_client.login(username=admin_user.username, password="password")
    api_client.user = admin_user
    return api_client
