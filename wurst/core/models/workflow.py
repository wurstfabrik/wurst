from autoslug import AutoSlugField
from django.core.exceptions import ValidationError
from django.db import models


class Transition(models.Model):
    type = models.ForeignKey("wurst.IssueType")
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from="name", unique_with="type")
    verbs = models.TextField(blank=True)
    from_statuses = models.ManyToManyField("wurst.Status", blank=True, related_name="from_transitions")
    from_any_status = models.BooleanField(default=False)
    to_status = models.ForeignKey("wurst.Status", related_name="to_transitions")
    initial = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super(Transition, self).save(*args, **kwargs)
        if self.initial:
            Transition.objects.filter(type=self.type).exclude(pk=self.pk).update(initial=False)

    @classmethod
    def mangle_import_datum(cls, datum):
        from wurst.core.models.issues import IssueType, Status
        datum = datum.copy()
        datum["type"] = IssueType.objects.get(slug=datum["type"])
        datum["to_status"] = Status.objects.get(slug=datum["to_status"])
        datum["from_statuses"] = [Status.objects.get(slug=s) for s in datum.get("from_statuses", ())]
        return datum

    def execute(self, issue):
        if issue.status == self.to_status:  # no-op
            return
        if issue.type != self.type:
            raise ValidationError("Issue %s type is not %s" % (issue, self.type))
        if not self.from_any_status and not self.from_statuses.filter(id=issue.status_id).exists():
            raise ValidationError("Issue %s status %s not allowed" % (issue, issue.status))
        issue.status = self.to_status

    def get_verbs(self):
        verbs = {self.name, self.slug}
        if self.verbs:
            verbs.update(set(self.verbs.split()))
        return verbs
