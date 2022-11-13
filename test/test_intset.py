import pytest
from intset import IntSet


class TestIntSet:
    def setup_method(self):
        self._intset = IntSet()

        # intset_add test
        self._intset.intset_add(31)
        self._intset.intset_add(4)
        self._intset.intset_add(7)
        self._intset.intset_add(20)

    def test_sorted(self):
        assert list(self._intset) == [4, 7, 20, 31]

    def test_intset_remove(self):
        self._intset.intset_remove(20)
        assert list(self._intset) == [4, 7, 31]

    def test_intset_find(self):
        assert (20 in self._intset) is True
        assert (44 in self._intset) is False

    def test_intset_random(self):
        a = self._intset.intset_random()
        assert a in self._intset

    def test_intset_get(self):
        a = self._intset[2]
        assert a == 20

    def test_intset_len(self):
        assert len(self._intset) == 4

    def test_intset_blob_len(self):
        print(self._intset.intset_blob_len())

    def test_intset_iter(self):
        it = iter(self._intset)
        assert next(it) == 4


if __name__ == '__main__':
    pytest.main()
