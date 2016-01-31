from autoslug.fields import AutoSlugField
from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now
from enumfields import EnumIntegerField

from wurst.consts import StatusCategory


@python_2_unicode_compatible
class IssueType(models.Model):
    """
    An issue type, e.g. "Task", "Bug", "Story", ...
    """

    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name', unique=True)
    nouns = models.TextField(blank=True)
    # TODO: Color/icon

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Status(models.Model):
    """
    A status associated with a given issue, e.g. "to do", "in progress", "rejected", "done"
    """

    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name', unique=True)
    category = EnumIntegerField(StatusCategory, db_index=True, default=StatusCategory.OPEN)
    value = models.IntegerField(default=0, db_index=True)  # Ordering value

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'statuses'


@python_2_unicode_compatible
class Priority(models.Model):
    """
    A priority for an issue, e.g. "high", "low", "critical", "whenever"
    """

    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name', unique=True)
    nouns = models.TextField(blank=True)
    value = models.IntegerField(default=0, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'priorities'


@python_2_unicode_compatible
class Issue(models.Model):
    """
    The main issue model.
    """

    project = models.ForeignKey("wurst.Project", related_name="issues")
    type = models.ForeignKey("wurst.IssueType", related_name="issues")
    status = models.ForeignKey("wurst.Status", related_name="issues")
    priority = models.ForeignKey("wurst.Priority", related_name="issues")
    key = models.CharField(unique=True, db_index=True, max_length=32)
    title = models.CharField(max_length=140)
    description = models.TextField(blank=True)
    start_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    created = models.DateTimeField(default=now, editable=False, db_index=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True, related_name="issues_created", editable=False
    )
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True, related_name="issues_assigned",
    )

    # TODO: parent FK?
    # TODO: tags
    # TODO: issue linking

    def save(self, *args, **kwargs):
        self._fill_fields()
        super(Issue, self).save(*args, **kwargs)

    def clean(self):
        self._fill_fields()
        super(Issue, self).clean()

    def _fill_fields(self):
        """
        Fill in any empty fields. Called upon save and clean.
        """
        if not self.key:
            self.key = self.project.generate_key()
        if not self.priority_id:
            self.priority = Priority.objects.filter(value=0).first()
        if not self.status_id:
            self.status = Status.objects.filter(value=StatusCategory.OPEN.value).order_by("value").first()

    def __str__(self):
        return self.key
