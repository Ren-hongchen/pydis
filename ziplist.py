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
        if head:
            self._data.insert(0, item)
        else:
            self._data.append(item)

    def ziplist_insert(self, index: int, item: Union[int, str]) -> None:
        self._data.insert(index, item)

    def ziplist_find(self, item: Union[int, str]) -> int:
        return self._data.index(item)

    def ziplist_delete_by_index(self, index: int) -> None:
        del self._data[index]

    def ziplist_delete_by_item(self, item: Union[int, str]) -> None:
        self._data.remove(item)

    def ziplist_delete_range(self, limits: tuple) -> None:
        del self._data[limits[0]:limits[1]]

    def ziplist_blob_len(self) -> int:
        return getsizeof(self) + getsizeof(self._data)
