from typing import Iterator


#  Simple Dynamic Strings Header
class SDSheader:

    def __init__(self, data: str) -> None:
        self._data = data

    def __len__(self) -> int:
        return len(self._data)  # Cpython对于内置类型，会从一个C结构体里查询对象的长度，所以为O(1)

    def __iter__(self) -> Iterator:
        return iter(self._data)

    def __getitem__(self, index: int) -> str:
        return self._data[index]

    def __add__(self, sdshdr: "SDSheader") -> "SDSheader":
        try:
            return SDSheader(self._data + sdshdr._data)
        except TypeError:
            return NotImplemented

    def __radd__(self, sdshdr: "SDSheader") -> "SDSheader":
        return self + sdshdr

    def __repr__(self) -> str:
        return f'SDSheader<{self._data}>'

    @property
    def data(self) -> str:
        return self._data

    def sdscat(self, cat_data: str) -> None:
        """
        将给定字符串拼接到SDS字符串的末尾

        :param cat_data: 拼接字符串
        :return: None
        """
        self._data += cat_data

    def sdsdup(self) -> "SDSheader":
        """
        创建一个SDS的副本(copy)

        :return: SDSheader
        """
        return SDSheader(self._data)

    def sdsclear(self) -> None:
        """
        清空SDS保存的字符串内容

        :return: None
        """
        self._data = ""
    
    def sdscpy(self, cpy_data: str) -> None:
        """
        将给定的字符串复制到SDS里面，覆盖原来的字符串

        :param cpy_data: 新字符串
        :return: None
        """
        self._data = cpy_data

    def sdsrange(self, start, end) -> None:
        """
        保留SDS给定区间内数据，不在区间内的数据会被覆盖或清除(左闭右开)

        :param start: 起始位置
        :param end: 结束位置
        :return: None
        """
        self._data = self._data[start:end]

    def sdstrim(self, trim_data: str) -> None:
        """
        接受一个字符串作为参数，从SDS左右两端分别移除所有在字符串中出现过的字符

        :param trim_data: 需要移除的字符
        :return: None
        """
        self._data = self._data.strip(trim_data)

    def sdscmp(self, sdshdr: "SDSheader") -> bool:
        """
        对比两个SDS字符串是否相等

        :param sdshdr: 需要对比的SDS
        :return: 是否相等
        """
        return self._data == sdshdr._data
