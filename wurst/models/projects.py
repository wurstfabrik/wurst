from autoslug.fields import AutoSlugField
from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name', unique=True)
    prefix = models.CharField(unique=True, max_length=10)

    def generate_key(self):
        return "%s%s" % (self.prefix, self.issues.count() + 1)
