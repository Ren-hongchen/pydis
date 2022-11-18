from sys import getsizeof
from typing import List, Union, Iterator


class ZipList:
    def __init__(self):
        self._data: List[Union[int, str]] = []

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Iterator:
        return iter(self._data)

    def __getitem__(self, index: int) -> Union[int, str]:
        return self._data[index]

    def ziplist_push(self, item: Union[int, str], head=False) -> None:
        """
        添加一个新值，可以添加到表头或表尾

        :param item: 新添加的值
        :param head: 默认为False，添加到表尾，设置为True，则添加到表头
        :return: None
        """
        if head:
            self._data.insert(0, item)
        else:
            self._data.append(item)

    def ziplist_insert(self, index: int, item: Union[int, str]) -> None:
        """
        将一个新值插入到指定位置之后

        :param index: 插入位置
        :param item: 新添加的值
        :return: None
        """
        self._data.insert(index, item)

    def ziplist_find(self, item: Union[int, str]) -> int:
        """
        查找给定值的位置

        :param item: 待查找的值
        :return: 在压缩链表中的位置
        """
        return self._data.index(item)

    def ziplist_delete_by_index(self, index: int) -> None:
        """
        删除给定位置的值

        :param index: 待删除的位置
        :return: None
        """
        del self._data[index]

    def ziplist_delete_by_item(self, item: Union[int, str]) -> None:
        """
        删除某个给定值

        :param item: 待删除的值
        :return: None
        """
        self._data.remove(item)

    def ziplist_delete_range(self, limits: tuple) -> None:
        """
        删除某个给定范围内的所有值

        :param limits: 元组形式(左闭右开)
        :return: None
        """
        del self._data[limits[0]:limits[1]]

    def ziplist_blob_len(self) -> int:
        """
        返回压缩链表占用的内存字节数

        :return: 内存字节数
        """
        return getsizeof(self) + getsizeof(self._data)
