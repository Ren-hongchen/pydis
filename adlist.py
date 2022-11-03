from typing import Any, Callable, Iterator, Optional


class ListNode:
    def __init__(self, value: Any) -> None:
        self._prev: Optional[ListNode] = None
        self._next: Optional[ListNode] = None
        self._value = value

    @property
    def prev(self) -> Optional["ListNode"]:
        return self._prev

    @prev.setter
    def prev(self, node: Optional["ListNode"]) -> None:
        self._prev = node
    
    @property
    def next(self) -> Optional["ListNode"]:
        return self._next

    @next.setter
    def next(self, node: Optional["ListNode"]) -> None:
        self._next = node

    @property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, value: Any) -> None:
        self._value = value


class LinkedList:

    def __init__(self) -> None:
        self._head: Optional[ListNode] = None
        self._tail: Optional[ListNode] = None
        self._len = 0

        self._dup: Optional[Callable] = None
        self._free: Optional[Callable] = None
        self._match: Optional[Callable] = None
    
    def __iter__(self) -> Iterator:
        p = self._head
        while p is not None:
            yield p
            p = p.next

    def __del__(self):
        for node in self:
            if self._free:
                self._free(node.value)
            del node
        del self

    @property
    def dup(self) -> Optional[Callable]:
        return self._dup

    @dup.setter
    def dup(self, dup_func: Callable) -> None:
        self._dup = dup_func

    @property
    def free(self) -> Optional[Callable]:
        return self._free

    @free.setter
    def free(self, free_func: Callable) -> None:
        self._free = free_func

    @property
    def match(self) -> Optional[Callable]:
        return self._match

    @match.setter
    def match(self, match_func: Callable) -> None:
        self._match = match_func

    @property
    def len(self) -> int:
        return self._len

    @property
    def head(self) -> Optional[ListNode]:
        return self._head
    
    @property
    def tail(self) -> Optional[ListNode]:
        return self._tail
    
    def list_add_node_head(self, value: Any) -> None:
        """
        将一个包含给定值的新节点添加到链表的表头

        :param value: 新节点的值
        :return: None
        """
        node = ListNode(value)

        if self._head is None:
            self._head = self._tail = node
            node.prev = node.next = None
        else: 
            node.next = self._head
            node.prev = None
            self._head.prev = node
            self._head = node

        self._len += 1

    def list_add_node_tail(self, value: Any) -> None:
        """
        将一个包含给定值的新节点添加到链表的表尾

        :param value: 新节点的值
        :return: None
        """
        node = ListNode(value)

        if self._tail is None:
            self._tail = self._head = node
            node.prev = node.next = None
        else:
            node.prev = self._tail
            node.next = None
            self._tail.next = node
            self._tail = node

        self._len += 1
    
    def list_insert_node(self, node: ListNode, value: Any, after: int) -> None:
        """
        将一个包含给定值的新节点添加到给定节点的之前或之后

        :param node: 给定节点
        :param value: 新节点的值
        :param after: 值为1 -- 添加到 给定节点 之后
                      值为0 -- 添加到 给定节点 之前
        :return: None
        """
        if node is None:
            return
        new_node = ListNode(value)

        if after != 0:
            new_node.prev = node
            new_node.next = node.next

            if self._tail is node:
                self._tail = new_node
        else:
            new_node.next = node
            new_node.prev = node.prev

            if self._head is node:
                self._head = new_node

        if new_node.prev is not None:
            new_node.prev.next = new_node
        if new_node.next is not None:
            new_node.next.prev = new_node

        self._len += 1

    def list_search_key(self, value: Any) -> Optional[ListNode]:
        """
        查找并返回链表中包含给定值的节点

        :param value: 查找节点的值
        :return: 查找成功返回节点
                 查找失败返回None
        """
        for node in self:
            if self._match is not None:
                if self._match(node.value, value):
                    return node
            else:
                if node.value == value:
                    return node
        return None
    
    def list_index(self, index: int) -> Optional[ListNode]:
        """
        返回链表在给定索引上的节点

        :param index: 索引 0为第一个 -1为倒数第一个
        :return: 查找成功返回节点
                 查找失败返回None
        """
        if index < 0:
            index = (-index) - 1
            p = self._tail
            while index and p:
                index -= 1
                p = p.prev
        else:
            p = self._head
            while index and p:
                index -= 1
                p = p.next
        return p

    def list_del_node(self, node: ListNode) -> None:
        """
        从链表中删除给定节点

        :param node: 需要删除的节点
        :return: None
        """
        if node.prev:
            node.prev.next = node.next
        else:
            self._head = node.next
        if node.next:
            node.next.prev = node.prev
        else:
            self._tail = node.prev

        if self._free:
            self._free(node.value)
        del node
        self._len -= 1

    def list_rotate(self) -> None:
        """
        将链表的表尾节点弹出，然后将被弹出的节点插入到链表的表头

        :return: None
        """
        if self._tail is None or self._head is None:
            return
        p = self._tail

        if p.prev is not None:
            self._tail = p.prev
            self._tail.next = None

        self._head.prev = p
        p.prev = None
        p.next = self._head
        self._head = p
    
    def list_dup(self) -> Optional["LinkedList"]:
        """
        复制一个链表的副本

        :return: 返回新链表，可能为None
        """
        new_list = LinkedList()

        new_list.dup = self._dup
        new_list.free = self.free
        new_list.match = self.match

        for node in self:
            if new_list.dup is not None:
                value = new_list.dup(node.value)
                if value is None:
                    del new_list
                    return None
            else:
                value = node.value
            
            new_list.list_add_node_tail(value)
        
        return new_list
