from typing import Optional, Any
from enum import IntEnum

class SkipListEnum(IntEnum):
    SKIPLIST_MAXLEVEL = 32
    SKIPLIST_P = 0.25



class PydisObject:
    def __init__(self):
        self._type: Optional[int] = None
        self._encoding: Optional[int] = None
        self._lru: Optional[int] = None
        # self._refcount: int = 0
        self._ptr: Any = None