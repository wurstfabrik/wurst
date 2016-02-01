from autoslug.fields import AutoSlugField
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Project(models.Model):
    """
    A Project; the top-level model that holds issues.
    """

    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name', unique=True)
    prefix = models.CharField(unique=True, max_length=10)

    def generate_key(self):
        """
        Generate the next sequential issue key for this project.

        This function is not race-condition safe; if the moons align
        just right, two issue save attempts may try the same key.

        If that happens, the caller would be gently advised to
        try again very soon.

        :return: Issue key string.
        """
        return "%s%s" % (self.prefix, self.issues.count() + 1)

    def __str__(self):
        return self.name
