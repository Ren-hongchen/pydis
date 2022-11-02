import pytest
from collections.abc import Iterator
from sds import SDSheader


class TestSDS:
    def setup_method(self):
        self.sds = SDSheader("Hello")

    def test_sds_create(self):
        assert isinstance(self.sds, SDSheader)

    def test_sds_len(self):
        assert len(self.sds) == 5

    def test_sds_iter(self):
        assert isinstance(iter(self.sds), Iterator)
    
    def test_sds_getitem(self):
        assert self.sds[0:2] == 'He'

    def test_sds_add(self):
        new_sds = SDSheader("World")
        assert (self.sds + new_sds).data == "HelloWorld"

    def test_sdscat(self):
        self.sds.sdscat("World")
        assert self.sds.data == "HelloWorld"

    def test_sdsdup(self):
        new_sds = self.sds.sdsdup()
        assert isinstance(new_sds, SDSheader) and (new_sds.data == self.sds.data)

    def test_sdsclear(self):
        self.sds.sdsclear()
        assert self.sds.data == ""

    def test_sdscpy(self):
        self.sds.sdscpy("HelloBob")
        assert self.sds.data == "HelloBob"

    def test_sdsrange(self):
        self.sds.sdsrange(0, 2)
        assert self.sds.data == "He"

    def test_sdstrim(self):
        self.sds.sdstrim("H")
        assert self.sds.data == "ello"

    def test_sdscmp(self):
        sds1 = SDSheader("Hello")
        sds2 = SDSheader("World")
        sds3 = SDSheader("Hello")
        assert sds1.sdscmp(sds2) is False
        assert sds1.sdscmp(sds3) is True


if __name__ == '__main__':
    pytest.main()
