import re

from enumfields import Enum

ISSUE_KEY_RE = re.compile(r"^\w+-\d+$", re.I)


class StatusCategory(Enum):
    OPEN = 0
    DONE = 1
    CLOSED = 2
    # TODO: Maybe expand this later?
