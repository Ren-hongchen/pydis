import pytest
from ziplist import ZipList


class TestZipList:
    def setup_method(self):
        self.ziplist = ZipList()

        # ziplist_push test
        self.ziplist.ziplist_push(1)
        self.ziplist.ziplist_push('a', head=True)
        self.ziplist.ziplist_push(2**8)
        self.ziplist.ziplist_push('hello world')

    def test_ziplist_push(self):
        assert self.ziplist._data == ['a', 1, 2**8, 'hello world']

    def test_ziplist_insert(self):
        self.ziplist.ziplist_insert(1, 33)
        assert self.ziplist._data == ['a', 33, 1, 2**8, 'hello world']

    def test_ziplist_len(self):
        assert len(self.ziplist) == 4

    def test_ziplist_getitem(self):
        assert self.ziplist[1] == 1

    def test_ziplist_find(self):
        assert self.ziplist.ziplist_find('hello world') == 3

    def test_ziplist_delete(self):
        self.ziplist.ziplist_delete_by_index(2)
        assert self.ziplist._data == ['a', 1, 'hello world']
        self.ziplist.ziplist_delete_by_item('a')
        assert self.ziplist._data == [1, 'hello world']

    def test_ziplist_delete_range(self):
        self.ziplist.ziplist_delete_range((1, 3))
        assert self.ziplist._data == ['a', 'hello world']

    def test_ziplist_iter(self):
        it = iter(self.ziplist)
        assert next(it) == 'a'

    def test_ziplist_blob_len(self):
        print(self.ziplist.ziplist_blob_len())


if __name__ == '__main__':
    pytest.main()
