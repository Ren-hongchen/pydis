import pytest

from skiplist import SkipList
from pydis import PydisObject


class TestSkipList:
    def setup_method(self):
        self.skiplist = SkipList()

        # zsl_insert test
        pobj = PydisObject()
        self.skiplist.zsl_insert(1.0, pobj)
        self.skiplist.zsl_insert(2.0, pobj)
        self.skiplist.zsl_insert(3.0, pobj)

    def get_items(self):
        res = []
        x = self.skiplist.head
        for i in range(self.skiplist.level - 1, -1, -1):
            while x.level[i].forward:
                res.append(x.level[i].forward.score)
                x = x.level[i].forward
        return res

    # 不完善，没有测试到分值相同，比较pobj的情景
    def test_zsl_delete(self):
        pobj = PydisObject()
        assert self.skiplist.zsl_delete(1.0, pobj) is True
        assert self.get_items() == [2.0, 3.0]

    # 不完善，没有测试到分值相同，比较pobj的情景
    def test_zsl_get_rank(self):
        pobj = PydisObject()
        assert self.skiplist.zsl_get_rank(1.0, pobj) == 1
        assert self.skiplist.zsl_get_rank(2.0, pobj) == 2

    def test_zsl_get_element_by_rank(self):
        assert self.skiplist.zsl_get_element_by_rank(1).score == 1.0
        assert self.skiplist.zsl_get_element_by_rank(2).score == 2.0
        assert self.skiplist.zsl_get_element_by_rank(5) is None

    def test_zsl_is_in_range(self):
        assert self.skiplist.zsl_is_in_range((1.0, 3.0)) is True

    def test_zsl_first_in_range(self):
        assert self.skiplist.zsl_first_in_range((1.0, 2.0)).score == 1.0
        assert self.skiplist.zsl_first_in_range((2.0, 3.0)).score == 2.0

    def test_zsl_last_in_range(self):
        assert self.skiplist.zsl_last_in_range((1.0, 2.0)).score == 2.0
        assert self.skiplist.zsl_last_in_range((1.0, 3.0)).score == 3.0

    def test_zsl_delete_range_by_score(self):
        self.skiplist.zsl_delete_range_by_score((1.0, 3.0), None)
        assert self.get_items() == [3.0]

    def test_zsl_delete_range_by_rank(self):
        self.skiplist.zsl_delete_range_by_rank((1, 3), None)
        assert self.get_items() == [3.0]


if __name__ == "__main__":
    pytest.main()
