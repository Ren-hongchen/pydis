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
        key = random.sample(self._data.keys(), 1)[0]
        value = self._data.get(key)
        return key, value

    def dict_delete(self, key: Any) -> None:
        del self._data[key]
