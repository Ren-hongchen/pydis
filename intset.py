import bisect
import random
from array import array
from typing import Iterator
from sys import getsizeof

INTSET_ENC_INT16 = 'h'
INTSET_ENC_INT32 = 'i'
INTSET_ENC_INT64 = 'l'

INTSET_ENC_INT16_MAX = 32767
INTSET_ENC_INT32_MAX = 2147483647
INTSET_ENC_INT64_MAX = 9223372036854775807


class IntSet:
    def __init__(self, encoding=INTSET_ENC_INT16) -> None:
        self._encoding: int = encoding
        self._data: array = array(encoding, [])

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Iterator:
        return iter(self._data)

    def __contains__(self, item: int) -> bool:
        return item in self._data

    def __getitem__(self, index: int) -> int:
        return self._data[index]

    def _add(self, item: int) -> None:
        if item in self._data:
            return
        bisect.insort(self._data, item)

    def _get_suitable_encoding(self, item: int) -> str:
        if item <= INTSET_ENC_INT16_MAX:
            return INTSET_ENC_INT16
        elif item <= INTSET_ENC_INT32_MAX:
            return INTSET_ENC_INT32
        else:
            return INTSET_ENC_INT64

    def _upgrade(self, encoding: str) -> None:
        new_array = array(encoding, [item for item in self._data])
        del self._data
        self._data = new_array

    def intset_add(self, item: int) -> None:
        """
        将给定元素添加到整数集合里

        :param item: 给定元素
        :return: None
        """
        if item > INTSET_ENC_INT64_MAX:
            raise ValueError("数值超出集合上限")
        suitable_encoding = self._get_suitable_encoding(item)
        if self._encoding == suitable_encoding:
            self._add(item)
        else:
            self._upgrade(suitable_encoding)
            self._add(item)

    def intset_remove(self, item: int) -> None:
        """
        从整数集合中移除给定元素

        :param item: 被移除元素
        :return: None
        """
        if item not in self._data:
            return
        self._data.remove(item)

    def intset_random(self) -> int:
        """
        从整数集合中随机返回一个元素

        :return: 随机返回的元素
        """
        length = len(self._data) - 1
        index = random.randint(0, length)
        return self._data[index]

    def intset_blob_len(self) -> int:
        """
        返回整数集合占用的内存字节数

        :return: 内存字节数
        """
        return getsizeof(self) + getsizeof(self._data)
