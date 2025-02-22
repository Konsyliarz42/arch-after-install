from enum import Enum


class ExitCode(int, Enum):
    SUCCESS = 0
    ERROR = 1
    CANCELED = 125
    NOT_EXECUTABLE = 126
    NOT_FOUND = 127
    KEY_REVOKED = 128
