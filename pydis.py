from typing import Optional, Any
from enum import IntEnum


class SkipListEnum(IntEnum):
    SKIPLIST_MAXLEVEL = 32
    SKIPLIST_P = 0.25


class PydisObjectEnum(IntEnum):
    PYDIS_STRING = 0
    PYDIS_LIST = 1
    PYDIS_SET = 2
    PYDIS_ZSET = 3
    PYDIS_HASH = 4


class PydisObjectEncodingEnum(IntEnum):
    PYDIS_ENCODING_RAW = 0  # 简单动态字符串
    PYDIS_ENCODING_INT = 1  # long类型的整数
    PYDIS_ENCODING_HT = 2  # 字典
    PYDIS_ENCODING_ZIPMAP = 3  # 压缩map
    PYDIS_ENCODING_LINKEDLIST = 4  # 双端链表
    PYDIS_ENCODING_ZIPLIST = 5  # 压缩链表
    PYDIS_ENCODING_INTSET = 6  # 整数集合
    PYDIS_ENCODING_SKIPLIST = 7  # 跳跃表和字典
    PYDIS_ENCODING_EMBSTR = 8  # embstr编码的简单动态字符串


class PydisObject:
    def __init__(self):
        self._type: Optional[int] = None
        self._encoding: Optional[int] = None
        self._lru: Optional[int] = None
        # self._refcount: int = 0
        self._ptr: Any = None

    @property
    def type(self) -> Optional[int]:
        return self._type

    @property
    def encoding(self) -> Optional[int]:
        return self._encoding

    @property
    def lru(self) -> Optional[int]:
        return self._lru

    @property
    def ptr(self) -> Any:
        return self._ptr
