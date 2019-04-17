from enum import Enum

class StatusCodes(Enum):
    NEW = 0
    PROCESSING_PARSING = 1
    PROCESSING_DOWNLOADING = 2
    FAILED = 3
    SUCCESS = 4
