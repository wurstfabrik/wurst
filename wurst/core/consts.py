import re

from enumfields import Enum

ISSUE_KEY_RE = re.compile(r"^\w+-\d+$", re.I)


class StatusCategory(Enum):
    OPEN = 0
    IN_PROGRESS = 10
    DONE = 80
    CLOSED = 100
    # TODO: Maybe expand this later?
