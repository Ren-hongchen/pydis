import pytest
from dict import Dict


class FakeData:
    def __hash__(self):
        return id(self)
    pass


class TestDict:
    def setup_method(self):
        self.dict = Dict()
        self.fake_data = FakeData()

    def test_dict_add(self):
        self.dict['1'] = 1
        self.dict['2'] = self.fake_data
        self.dict[self.fake_data] = 2
        assert list(self.dict._data.keys()) == ["1", "2", self.fake_data]
        assert list(self.dict._data.values()) == [1, self.fake_data, 2]

    def test_dict_fetch_value(self):
        self.dict['1'] = 1
        self.dict['2'] = 2
        self.dict['3'] = 3
        assert self.dict["2"] == 2

    def test_dict_replace(self):
        self.dict['1'] = 1
        self.dict['1'] = 2
        assert self.dict["1"] == 2

    def test_dict_get_random_key(self):
        self.dict['1'] = 1
        self.dict['2'] = 2
        self.dict['3'] = 3
        assert self.dict.dict_get_random_key() in (("1", 1), ("2", 2), ("3", 3))

    def test_dict_delete(self):
        self.dict['1'] = 1
        self.dict['2'] = 2
        self.dict['3'] = 3
        self.dict.dict_delete("2")
        assert list(self.dict._data.keys()) == ["1", "3"]
        assert list(self.dict._data.values()) == [1, 3]


if __name__ == '__main__':
    pytest.main()
