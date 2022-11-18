from typing import Optional, Any, List, Callable
from enum import IntEnum

from sds import SDSheader
from object import sds_encoded_object
from db import PydisDB
from dict import Dict

PYDIS_OK = 0
PYDIS_ERROR = -1

UNIT_SECONDS = 0
UNIT_MILLISECONDS = 1


class SkipListEnum(IntEnum):
    SKIPLIST_MAXLEVEL = 32
    SKIPLIST_P = 0.25


class PydisObjectEnum(IntEnum):
    PYDIS_STRING = 0
    PYDIS_LIST = 1
    PYDIS_SET = 2
    PYDIS_ZSET = 3
    PYDIS_HASH = 4


class PydisObjectEncodingEnum(IntEnum):
    PYDIS_ENCODING_RAW = 0  # 简单动态字符串
    PYDIS_ENCODING_INT = 1  # long类型的整数
    PYDIS_ENCODING_HT = 2  # 字典
    PYDIS_ENCODING_ZIPMAP = 3  # 压缩map
    PYDIS_ENCODING_LINKEDLIST = 4  # 双端链表
    PYDIS_ENCODING_ZIPLIST = 5  # 压缩链表
    PYDIS_ENCODING_INTSET = 6  # 整数集合
    PYDIS_ENCODING_SKIPLIST = 7  # 跳跃表和字典
    # PYDIS_ENCODING_EMBSTR = 8  # embstr编码的简单动态字符串


class PydisObject:
    def __init__(self):
        self._type: Optional[int] = None
        self._encoding: Optional[int] = None
        self._lru: Optional[int] = None
        # self._refcount: int = 0
        self._ptr: Any = None

    @property
    def type(self) -> Optional[int]:
        return self._type

    @property
    def encoding(self) -> Optional[int]:
        return self._encoding

    @property
    def lru(self) -> Optional[int]:
        return self._lru

    @property
    def ptr(self) -> Any:
        return self._ptr

    @classmethod
    def from_str(cls, data: str) -> "PydisObject":
        instance = cls()
        instance._type = PydisObjectEnum.PYDIS_STRING
        instance._encoding = PydisObjectEncodingEnum.PYDIS_ENCODING_RAW
        instance._ptr = SDSheader(data)
        return instance


class PydisClient:
    def __init__(self,
                 fd: int,
                 db: PydisDB,
                 dict_id: int,
                 ):
        # 套接字
        self.fd: int = fd

        # 当前使用的数据库
        self.db: PydisDB = db

        # 当前使用的数据库id
        self.dict_id: int = dict_id

        # 客户端的名字(set by CLIENT SETNAME)
        self.name: Optional[PydisObject] = None

        # 查询缓冲区
        self.querybuf: Optional[SDSheader] = None

        # 查询缓冲区长度峰值(最近(100ms及以上)查询缓冲区大小峰值)
        self.querybuf_peak: int = 0

        # 参数数量
        self.argc: int = 0

        # 参数对象数组
        self.argv: List[PydisObject] = []

    def add_reply_error(self, message: str):
        pass

    def add_reply(self, pobj: Optional[PydisObject]):
        pass

    def _get_int_from_object(self, pobj: Optional[PydisObject]) -> int:
        value = None

        if pobj is None:  # pobj为None value设为0
            value = 0

        assert pobj.type == PydisObjectEnum.PYDIS_STRING

        if sds_encoded_object(pobj):
            value = int(pobj.ptr)  # 如果是RAW编码进行转换
        elif pobj.encoding == PydisObjectEncodingEnum.PYDIS_ENCODING_INT:
            value = pobj.ptr  # 如果是INT编码直接赋值
        else:
            # pydis_panic("Unknown String Encoding")
            value = PYDIS_ERROR

        return value

    def get_int_from_object_or_reply(self, pobj: Optional[PydisObject], message: Optional[str]) -> int:
        """
        尝试从对象pobj中取出整数值，或者尝试将pobj中的值转换为整数值，并返回

        :param pobj: 待转换的对象
        :param message: 自定义的错误信息
        :return: 如果成功返回转换后的整数值，否则返回PYDIS_ERROR,并向客户端发生错误信息
        """
        value = self._get_int_from_object(pobj)
        if value == PYDIS_ERROR:
            if message is not None:
                self.add_reply_error(message)
            else:
                self.add_reply_error("value is not an integer or out of range")
            return PYDIS_ERROR

        return value


class PydisServer:
    def __init__(self,
                 config_file: Optional[str] = None):

        # ---------- General ----------

        # 配置文件的绝对路径
        self.config_file: Optional[str] = config_file

        # server_cron()每秒调用次数
        self.hz: int = 0

        # 数据库
        self.db: Optional[PydisDB] = None

        # 命令表(受到 rename 配置选项作用)
        self.commands: Optional[Dict] = None

        # 命令表(无 rename 配置选项作用)
        self.orig_commands: Optional[Dict] = None

        # 事件状态
        # aeEventloop el

        # 最近一次使用时钟
        self.lru_clock: int = 0

        # 关闭服务器的标识
        self.shutdown_asap: int = 0

        # 是否设置了密码
        self.require_passwd: str = ""

        # PID文件
        self.pid_file: str = ""

        # server_cron函数运行次数计数器
        self.cron_loops: int = 0

        # 本服务器的RUN_ID
        self.run_id: str = ""

        # ---------- AOF persistence ----------

        # 自从上次 SAVE 执行以来，数据库被修改的次数
        self.dirty: int = 0

        # 负责 AOF 重写的子进程id
        self.aof_child_pid = -1

        # ---------- RDB persistence ----------

        # 负责 BGSAVE 的子进程id
        self.rdb_child_pid = -1



class PydisCommand:
    def __init__(self,
                 name: str,
                 proc: Callable,
                 arity: int,
                 sflags: str,
                 flags: int,
                 first_key: int,
                 last_key: int,
                 key_step: int):
        # 命令名字
        self.name: str = name

        # 实现函数
        self.pydis_command_proc: Callable = proc

        # 参数个数
        self.arity: int = arity

        # 字符串表示的FLAG
        self.sflags: str = sflags

        # 实际FLAG
        self.flags: int = flags

        # self.get_keys_proc: PydisGetKeysProc 用于集群

        # 为key的第一个参数
        self.first_key: int = first_key

        # 为key的最后一个参数
        self.last_key: int = last_key

        # first key和last key之间的距离
        self.key_step: int = key_step

        # 命令执行花费的总毫微秒数
        self.micro_seconds: int = 0

        # 命令执行的总次数
        self.calls: int = 0


server = PydisServer()
