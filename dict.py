from typing import Any, Tuple
import random


class Dict:
    def __init__(self) -> None:
        self._priv_data: Any = None
        self._data = {}

    def __len__(self) -> int:
        return len(self._data)

    def __getitem__(self, key: Any) -> Any:
        return self._data.get(key)

    def __setitem__(self, key: Any, value: Any) -> None:
        self._data[key] = value

    def dict_get_random_key(self) -> Tuple[Any, Any]:
        """
        从字典中随机返回一个键值对
        :return: 键值对(元组形式)
        """
        key = random.sample(self._data.keys(), 1)[0]
        value = self._data.get(key)
        return key, value

    def dict_delete(self, key: Any) -> None:
        """
        从字典中删除给定键所对应的键值对
        :param key: 需要删除的键
        :return: None
        """
        del self._data[key]
