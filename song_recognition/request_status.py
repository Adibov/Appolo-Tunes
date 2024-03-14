import enum


class RequestStatus(enum.Enum):
    PENDING = 'pending'
    FAILURE = 'failure'
    READY = 'ready'
    DONE = 'done'
