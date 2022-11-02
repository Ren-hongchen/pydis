import pytest
from collections.abc import Iterator
from adlist import ListNode, LinkedList


def get_value(adlist):
    value = []
    for node in adlist:
        value.append(node.value)
    return value


class TestAdList:
    def setup_method(self):
        self.adlist = LinkedList()
        self.adlist.list_add_node_head(1)
        self.adlist.list_add_node_head(2)
        self.adlist.list_add_node_head(3)

    def test_listnode_create(self):
        node = ListNode(123)
        assert isinstance(node, ListNode)
        assert node.value == 123

    def test_adlist_len(self):
        assert self.adlist.len == 3

    def test_adlist_iter(self):
        assert isinstance(iter(self.adlist), Iterator)

    def test_adlist_add__node_head(self):
        self.adlist.list_add_node_head(4)
        assert get_value(self.adlist) == [4, 3, 2, 1]

    def test_adlist_add_node_tail(self):
        self.adlist.list_add_node_tail(4)
        assert get_value(self.adlist) == [3, 2, 1, 4]

    def test_adlist_insert_node(self):
        self.adlist.list_insert_node(self.adlist.head, 4, 1)
        assert get_value(self.adlist) == [3, 4, 2, 1]

    def test_adlist_search_key(self):
        node = self.adlist.list_search_key(2)
        assert isinstance(node, ListNode)
        assert node.value == 2

    def test_adlist_search_key_have_match(self):
        def match(a, b):
            if a == b:
                return True
        self.adlist.match = match

        node = self.adlist.list_search_key(2)

        assert self.adlist.match is not None
        assert isinstance(node, ListNode)
        assert node.value == 2

    def test_adlist_index(self):
        node = self.adlist.list_index(0)
        assert isinstance(node, ListNode)
        assert node.value == 3

    def test_adlist_del_node(self):
        node = self.adlist.list_search_key(2)
        self.adlist.list_del_node(node)
        assert get_value(self.adlist) == [3, 1]

    def test_adlist_del_node_have_free(self):
        def free(value):
            if value != 0:
                del value

        self.adlist.free = free
        node = self.adlist.list_search_key(2)
        self.adlist.list_del_node(node)

        assert self.adlist.free is not None
        assert get_value(self.adlist) == [3, 1]

    def test_adlist_rotate(self):
        self.adlist.list_rotate()
        assert get_value(self.adlist) == [1, 3, 2]

    def test_adlist_dup(self):
        new_list = self.adlist.list_dup()
        assert isinstance(new_list, LinkedList)
        assert get_value(new_list) == get_value(self.adlist)
        assert (new_list is self.adlist) is False

    def test_adlist_dup_have_dup(self):
        def dup(value):
            return value + 1
        self.adlist.dup = dup
        new_list = self.adlist.list_dup()
        assert self.adlist.dup is not None
        assert isinstance(new_list, LinkedList)
        assert get_value(new_list) == [4, 3, 2]
        assert (new_list is self.adlist) is False

    def test_adlist_release(self):
        del self.adlist
        assert ('adlist' in dir(self)) is False


if __name__ == '__main__':
    pytest.main()
