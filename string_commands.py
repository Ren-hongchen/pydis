from typing import Optional
from time import time

from pydis import PydisClient, PydisObject, server
from pydis import PYDIS_OK, PYDIS_ERROR, UNIT_SECONDS, UNIT_MILLISECONDS
from object import try_object_encoding

PYDIS_SET_NO_FLAGS = 0
PYDIS_SET_NX = (1 << 0)  # 当键不存在时设置
PYDIS_SET_XX = (1 << 1)  # 当键存在时设置


def check_string_length(client: PydisClient, size: int) -> int:
    if size > 512*1024*1024:
        client.add_reply_error("字符串长度超出最大上限(512MB)")
        return PYDIS_ERROR
    return PYDIS_OK


def set_generic_command(client: PydisClient, flags: int, key: PydisObject, value: PydisObject,
                        expire: PydisObject, unit: int,
                        ok_reply: Optional[PydisObject], abort_reply: Optional[PydisObject]):
    milliseconds: float = 0.0

    if expire:
        milliseconds = client.get_int_from_object_or_reply(expire, None)  # 取出过期时间
        if milliseconds == PYDIS_ERROR:
            return
        if milliseconds <= 0:  # 检验过期时间正确性
            client.add_reply_error("Invalid expire time in SETEX")
            return

        if unit == UNIT_SECONDS:  # 无论输入是秒还是毫秒，最终都以毫秒形式保存
            milliseconds *= 1000

    # 如果设置了 NX 或者 XX 参数，那么检查条件是否不符合这两个设置
    # 在条件不符合时报错，报错的内容由 abort_reply 参数决定
    if (flags & PYDIS_SET_NX and client.db.lookup_key_write(key) is not None) or\
            (flags & PYDIS_SET_XX and client.db.lookup_key_write(key) is None):
        # client.add_reply(abort_reply if abort_reply else shared.nullbulk)
        client.add_reply(abort_reply)
        return

    # 将键值关联到数据库
    client.db.set_key(key, value)

    # 数据库设置为脏
    server.dirty += 1

    # 设置过期时间
    if expire:
        client.db.set_expire(key, time() + milliseconds)

    # 发送事件通知
    # notify_keyspace_event()

    # 发送事件通知
    # if expire: notify_keyspace_event()

    client.add_reply(PydisObject.from_str("ok") if ok_reply is None else ok_reply)


def set_command(client: PydisClient):
    expire: Optional[PydisObject] = None
    unit = UNIT_SECONDS
    flags = PYDIS_SET_NO_FLAGS

    # 检验参数
    for i in range(3, client.argc):
        argument: str = client.argv[i].ptr
        next_obj: Optional[PydisObject] = client.argv[i + 1] if i != (client.argc - 1) else None

        argument = argument.lower()
        if argument[0:2] == 'nx':
            flags |= PYDIS_SET_NX
        elif argument[0:2] == 'xx':
            flags |= PYDIS_SET_XX
        elif argument[0:2] == 'ex' and next_obj:
            unit = UNIT_SECONDS
            expire = next_obj
            i += 1
        elif argument[0:2] == 'px' and next_obj:
            unit = UNIT_MILLISECONDS
            expire = next_obj
            i += 1
        else:
            client.add_reply(PydisObject.from_str("Syntax Error"))
            return

    # 尝试对对象进行编码
    client.argv[2] = try_object_encoding(client.argv[2])

    set_generic_command(client, flags, client.argv[1], client.argv[2], expire, unit, None, None)
