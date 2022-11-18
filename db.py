from typing import Optional

from dict import Dict
from pydis import PydisObject, server
from sds import SDSheader


class PydisDB:
    def __init__(self, id_: int):
        # 数据库键空间，保存库中所有键值对
        self.dict: Dict = Dict()
        # 键的过期时间，字典的键为键，字典的值为过期事件 UNIX 时间戳
        self.expire: Dict = Dict()
        # 正在阻塞的键
        self.blocking_keys = Dict()
        # 可以解除阻塞的键
        self.ready_keys = Dict()
        # 正在被WATCH命令监视的键
        self.watched_keys = Dict()

        # eviction_pool

        # 数据库id
        self.id: int = id_

        # 数据库键的平均TTL
        self.avg_ttl: int = 0

    def lookup_key(self, key: PydisObject) -> Optional[PydisObject]:
        """
        从数据库中取出key对应的值(对象)

        :param key: key
        :return: 如果值(对象)存在，返回其值或对象，否则返回None
        """
        value: PydisObject = self.dict[key.ptr]

        if value:
            # 更新时间信息，只在子进程不存在时进行
            if server.rdb_child_pid == -1 and server.aof_child_pid == -1:
                # value.lru = LRUCLOCK()
                pass
            return value
        return None

    def lookup_key_write(self, key: PydisObject) -> Optional[PydisObject]:
        # expire_if_needed()
        return self.lookup_key(key)

    def _db_add(self, key: PydisObject, value: PydisObject) -> None:
        # 复制键名
        copy: SDSheader = key.ptr.sdsdup()
        # 添加键值对
        self.dict[copy] = value
        # 如果开启了集群模式，那么将键保存到槽里面
        # if server.cluster_enabled: slotToKeyAdd(key)

    def _remove_expire(self, key: PydisObject):
        assert self.dict[key.ptr] is not None
        self.expire.dict_delete(key.ptr)

    def _signal_modified_key(self, key: PydisObject) -> None:
        # touch_watched_key()
        pass

    def _signal_flushed_db(self):
        # touch_watched_keys_on_flush()
        pass

    def set_key(self, key: PydisObject, value: PydisObject) -> None:
        """
        高层次Set操作，不管Key是否存在，将其与Value关联起来
        1. 值对象的引用计数增加(未实现)
        2. 监视Key的客户端将收到键已被修改的通知
        3. 键的过期时间会被移除(键变为永久的)
        :param key: key
        :param value: value
        :return: None
        """
        # 添加数据
        self._db_add(key, value)

        # 增加引用计数
        # self.incrRefCount(val)

        # 移除过期时间
        self._remove_expire(key)
        # 发送通知
        self._signal_modified_key(key)

    def set_expire(self, key: PydisObject, when: float) -> None:

        key = key.ptr

        # 确定在主字典中含有此键
        assert self.dict[key] is not None

        # 更新或新建过期时间键值对
        self.expire[key] = when


