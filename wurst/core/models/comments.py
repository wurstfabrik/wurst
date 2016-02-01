from django.conf import settings
from django.db import models
from django.utils.timezone import now
from reversion import revisions as reversion


@reversion.register
class Comment(models.Model):
    issue = models.ForeignKey("wurst.Issue", related_name="comments")
    created = models.DateTimeField(default=now, editable=False, db_index=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True, related_name="comments_created", editable=False
    )
    text = models.TextField()
