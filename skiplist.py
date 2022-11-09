import random
from typing import Optional, List

from pydis import PydisObject, SkipListEnum
from object import compare_string_objects, equal_string_objects
from dict import Dict


class SkipListLevel:
    def __init__(self):
        self._forward: Optional[SkipListNode] = None
        self._span: int = 0

    @property
    def forward(self) -> Optional["SkipListNode"]:
        return self._forward

    @forward.setter
    def forward(self, forward: Optional["SkipListNode"]) -> None:
        self._forward = forward

    @property
    def span(self) -> int:
        return self._span

    @span.setter
    def span(self, span: int) -> None:
        self._span = span


class SkipListNode:
    def __init__(self, level: int, score: float, pobj: Optional[PydisObject]) -> None:
        self._backward: Optional["SkipListNode"] = None
        self._score: float = score
        self._pobj: Optional[PydisObject] = pobj
        self._level: List[SkipListLevel] = [SkipListLevel()] * level

    @property
    def backward(self) -> Optional["SkipListNode"]:
        return self._backward

    @backward.setter
    def backward(self, backward: Optional["SkipListNode"]) -> None:
        self._backward = backward

    @property
    def score(self) -> float:
        return self._score

    @property
    def pobj(self) -> Optional[PydisObject]:
        return self._pobj

    @property
    def level(self) -> List[SkipListLevel]:
        return self._level


class SkipList:
    def __init__(self):
        self._head: Optional[SkipListNode] = SkipListNode(SkipListEnum.SKIPLIST_MAXLEVEL, 0, None)
        self._tail: Optional[SkipListNode] = None
        self._length: int = 0
        # 跳跃表内，层数最大的节点的层数(表头节点不计算在内)
        self._level: int = 1

    def _get_random_level(self) -> int:
        level = 1
        while random.randint(0, 0x7fff) < (SkipListEnum.SKIPLIST_P * 0xffff):
            level += 1
        return level if level < SkipListEnum.SKIPLIST_MAXLEVEL else SkipListEnum.SKIPLIST_MAXLEVEL

    def zsl_insert(self, score: float, pobj: Optional[PydisObject]) -> SkipListNode:
        assert score is not None

        update: List[Optional[SkipListNode]] = [None] * SkipListEnum.SKIPLIST_MAXLEVEL
        rank: List[int] = [0] * SkipListEnum.SKIPLIST_MAXLEVEL

        x = self._head
        for i in range(self._level - 1, -1, -1):

            rank[i] = 0 if i == (self._level - 1) else rank[i + 1]

            while x.level[i].forward and (
                x.level[i].forward.score < score or
                (x.level[i].forward.score == score and
                 compare_string_objects(x.level[i].forward.pobj, pobj))
            ):
                rank[i] += x.level[i].span
                x = x.level[i].forward

            update[i] = x

        level = self._get_random_level()
        if level > self._level:

            for i in range(self._level, level):
                rank[i] = 0
                update[i] = self._head
                update[i].level[i].span = self._length

            self._level = level

        x = SkipListNode(level, score, pobj)
        for i in range(0, level):
            x.level[i].forward = update[i].level[i].forward
            update[i].level[i].forward = x
            x.level[i].span = update[i].level[i].span - (rank[0] - rank[i])
            update[i].level[i].span = (rank[0] - rank[i]) + 1

        for i in range(level, self._level):
            update[i].level[i].span += 1

        x.backward = None if update[0] is self._head else update[0]

        if x.level[0].forward:
            x.level[0].forward.backward = x
        else:
            self._tail = x

        self._length += 1

        return x

    def _zsl_delete_node(self, x: SkipListNode, update: List[SkipListNode]) -> None:

        for i in range(self._level):
            if update[i].level[i].forward is x:
                update[i].level[i].span = x.level[i].span - 1
                update[i].level[i].forward = x.level[i].forward
            else:
                update[i].level[i].span -= 1

        if x.level[0].forward:
            x.level[0].forward.backward = x.backward
        else:
            self._tail = x.backward

        while self._level > 1 and self._head.level[self._level - 1].forward is None:
            self._level -= 1

        self._length -= 1

    def zsl_delete(self, score: float, pobj: PydisObject) -> bool:

        update: List[Optional[SkipListNode]] = [None] * SkipListEnum.SKIPLIST_MAXLEVEL

        x = self._head
        for i in range(self._level - 1, -1, -1):

            while x.level[i].forward and (
                    x.level[i].forward.score < score or
                    (x.level[i].forward.score == score and
                     compare_string_objects(x.level[i].forward.pobj, pobj))
            ):
                x = x.level[i].forward

            update[i] = x

        x = x.level[0].forward
        if x and score == x.score and equal_string_objects(x.pobj, pobj):
            self._zsl_delete_node(x, update)
            del x
            return True

        return False

    def zsl_get_rank(self, score: float, pobj: PydisObject) -> int:

        rank = 0
        x = self._head

        for i in range(self._level - 1, -1, -1):

            while x.level[i].forward and (
                    x.level[i].forward.score < score or
                    (x.level[i].forward.score == score and
                     compare_string_objects(x.level[i].forward.pobj, pobj))
            ):
                rank += x.level[i].span
                x = x.level[i].forward

            if x.pobj and equal_string_objects(x.pobj, pobj):
                return rank

        return 0

    def zsl_get_element_by_rank(self, rank: int) -> Optional[SkipListNode]:

        traversed = 0
        x = self._head

        for i in range(self._level - 1, -1, -1):

            while x.level[i].forward and (traversed + x.level[i].span) < rank:
                traversed += x.level[i].span
                x = x.level[i].forward

            if traversed == rank:
                return x

        return None

    def zsl_is_in_range(self, limits: tuple) -> bool:

        if limits[0] > limits[1]:
            raise ValueError("左值应该小于右值")

        x = self._tail
        if x is None or x.score > limits[1]:
            return False

        x = self._head.level[0].forward
        if x is None or x.score <= limits[0]:
            return False

        return True

    def zsl_first_in_range(self, limits: tuple) -> Optional[SkipListNode]:

        if not self.zsl_is_in_range(limits):
            raise ValueError("该区间不在表内")

        x = self._head
        for i in range(self._level - 1, -1, -1):

            while x.level[i].forward and (x.level[i].forward.score >= limits[0]):
                x = x.level[i].forward

        x = x.level[0].forward
        assert x is not None

        if x.score > limits[1]:
            return None

        return x

    def zsl_last_in_range(self, limits: tuple) -> Optional[SkipListNode]:

        if not self.zsl_is_in_range(limits):
            raise ValueError("该区间不在表内")

        x = self._head
        for i in range(self._level - 1, -1, -1):

            while x.level[i].forward and (x.level[i].forward.score < limits[1]):
                x = x.level[i].forward

        x = x.level[0].forward
        assert x is not None

        if x.score <= limits[0]:
            return None

        return x

    def zsl_delete_range_by_score(self, limits: tuple, pdict: Dict) -> int:

        update: List[Optional[SkipListNode]] = [None] * SkipListEnum.SKIPLIST_MAXLEVEL
        removed: int = 0

        x: SkipListNode = self._head
        for i in range(self._level - 1, -1, -1):

            while x.level[i].forward and x.level[i].forward.score < limits[0]:
                x = x.level[i].forward

            update[i] = x

        x: SkipListNode = x.level[0].forward

        while x and x.score < limits[1]:
            next: SkipListNode = x.level[0].forward
            self._zsl_delete_node(x, update)
            pdict.dict_delete(x.pobj)
            del x
            removed += 1
            x = next

        return removed

    def zsl_delete_range_by_rank(self, limits: tuple, pdict: Dict) -> int:

        update: List[Optional[SkipListNode]] = [None] * SkipListEnum.SKIPLIST_MAXLEVEL
        removed: int = 0
        traversed: int = 0

        x: SkipListNode = self._head
        for i in range(self._level - 1, -1, -1):

            while x.level[i].forward and (traversed + x.level[i].span < limits[0]):
                traversed += x.level[i].span
                x = x.level[i].forward

            update[i] = x

        traversed += 1
        x: SkipListNode = x.level[0].forward

        while x and traversed < limits[1]:
            next: SkipListNode = x.level[0].forward
            self._zsl_delete_node(x, update)
            pdict.dict_delete(x.pobj)
            del x
            traversed += 1
            removed += 1
            x = next

        return removed



