# -- encoding: UTF-8 --
import six


class NounsMixin(object):
    def get_nouns(self):
        nouns = getattr(self, "nouns", ())
        if isinstance(nouns, six.string_types):
            nouns = set(nouns.split())
        else:
            nouns = set(nouns)
        nouns.add(self.slug)
        nouns.add(self.name)
        return nouns
