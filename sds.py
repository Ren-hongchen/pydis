from typing import Iterator


#  Simple Dynamic Strings Header
class SDSheader:

    def __init__(self, data: str) -> None:
        self._data = data

    def __len__(self) -> int:
        return len(self._data)

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
        self._data += cat_data

    def sdsdup(self) -> "SDSheader":
        return SDSheader(self._data)

    def sdsclear(self) -> None:
        self._data = ""
    
    def sdscpy(self, cpy_data: str) -> None:
        self._data = cpy_data

    def sdsrange(self, start, end) -> None:
        self._data = self._data[start:end]

    def sdstrim(self, trim_data: str) -> None:
        self._data = self._data.strip(trim_data)

    def sdscmp(self, sdshdr: "SDSheader") -> bool:
        return self._data == sdshdr._data
