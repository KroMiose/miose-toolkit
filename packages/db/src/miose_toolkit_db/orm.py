from importlib import import_module
from pathlib import Path
from typing import Any, Dict, List, Optional, Type, TypeVar

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.orm.query import Query

try:
    import ujson as json  # type: ignore
except ImportError:
    import json


T = TypeVar("T", bound="MioModel")


class MioModel:
    """数据模型基类"""

    @classmethod
    def add(cls: Type[T], **kwarg) -> T:
        """新增行"""
        raise NotImplementedError

    @classmethod
    def batch_add(cls, data_list: List[Dict[str, Any]]) -> None:
        """批量新增行 (暂不支持更新)"""
        raise NotImplementedError

    @classmethod
    def get_by_pk(cls: Type[T], pk_value: Any) -> Optional[T]:
        """根据主键查询行"""
        raise NotImplementedError

    @classmethod
    def get_by_field(cls: Type[T], field: str, value: str) -> Optional[T]:
        """根据字段查询行"""
        raise NotImplementedError

    @classmethod
    def filter(cls: Type[T], **kwarg) -> List[T]:
        """筛选数据行"""
        raise NotImplementedError

    @classmethod
    def get_all(cls: Type[T]) -> List[T]:
        """查询所有行"""
        raise NotImplementedError

    def update(self: T, data: Optional[Dict[str, Any]] = None, **kwarg) -> T:
        """更新行"""
        raise NotImplementedError

    def delete(self) -> None:
        """删除行"""
        raise NotImplementedError

    @classmethod
    def auto_insert(cls: Type[T], **kwarg) -> T:
        """自动插入数据"""
        raise NotImplementedError

    @classmethod
    def auto_insert_by_field(
        cls: Type[T],
        field: str,
        value: str,
        **kwarg,
    ) -> T:
        """根据字段自动插入数据"""
        raise NotImplementedError

    @classmethod
    def sqa_query(cls: Type[T]) -> Query[T]:
        """获取 SQLAlchemy 查询对象"""
        raise NotImplementedError


class MioOrm:
    def __init__(self, db_url: str, **kwarg) -> None:
        """初始化数据库连接

        :param db_url: 数据库连接 URL
        :param kwarg: 数据库连接参数
            例如:
                - pool_pre_ping: False  # 每次连接前检查连接是否有效
                - pool_size: 10  # 连接池大小
                - max_overflow: 20  # 超过连接池大小后最多创建的连接数
                - pool_recycle: 3600  # 连接回收时间 (秒)
        """
        if db_url.startswith("sqlite:///"):
            root = db_url.replace("sqlite:///", "").rsplit("/", 1)[0]
            Path(root).mkdir(parents=True, exist_ok=True)
        self._db_url = db_url
        self._db_args = kwarg
        self._create_db_connection(db_url, **kwarg)

        database_type = db_url.split("://")[0]

        if "mysql" in database_type:
            database_type = "mysql"
        elif "sqlite" in database_type:
            database_type = "sqlite"
        elif "postgresql" in database_type:
            database_type = "postgresql"

        # 根据数据库类型动态导入不同的插入方法
        self._insert = import_module(f"sqlalchemy.dialects.{database_type}").insert
        # print("type:", type(self._insert))

    def _create_db_connection(self, db_url: str) -> None:
        """创建数据库连接

        Args:
        :param db_url: 数据库连接 URL
        """
        try:
            # 创建对象的基类:
            self._Base = declarative_base()

            # 初始化数据库连接:
            self._engine = create_engine(db_url, **self._db_args)
            self._connection = self._engine.connect()

            # 创建DBSession类型:
            self._db: Session = sessionmaker(bind=self._engine)()
        except Exception:
            print("Failed to create database connection")
            raise

    def reconnect(self) -> None:
        """重新连接数据库"""
        self.close_db_connection()
        self._create_db_connection(self._db_url, **self._db_args)

    def close_db_connection(self) -> None:
        """关闭数据库连接"""
        self._db.close()
        self._connection.close()
        self._engine.dispose()

    def get_sqa_db(self) -> Session:
        """获取数据库连接

        Returns:
        :return: 数据库连接
        """
        return self._db

    def get_sqa_Base(self) -> Any:
        """获取 SQLAlchemy 的 Base 类

        Returns:
        :return: SQLAlchemy 的 Base 类
        """
        return self._Base

    def create_all(self) -> None:
        """创建所有数据表"""
        self._Base.metadata.create_all(self._engine)

    def reg_predefine_data_model(self, table_name="", primary_key: str = "id"):
        """注册预定义的数据模型装饰器构建器

        Args:
        :param cls: 数据模型类
        """

        db = self._db

        def modal_class_wrapper(cls: Type[T]) -> Type[T]:
            """数据模型装饰器"""

            class ModelClass(cls, self.get_sqa_Base()):
                """预定义数据模型基类"""

                __allow_unmapped__ = True
                __tablename__ = table_name or cls.__name__.lower()

                @classmethod
                def add(cls: Type[T], **kwarg) -> T:
                    """新增行

                    Args:
                    :param kwarg: 行数据

                    Returns:
                    :return: 行对象
                    """

                    for k, v in kwarg.items():
                        if isinstance(v, (dict, list)):
                            kwarg[k] = json.dumps(v, ensure_ascii=False)
                    data = cls(**kwarg)

                    try:
                        db.add(data)
                        db.commit()
                    except Exception:
                        db.rollback()
                        raise

                    return data

                @classmethod
                def batch_add(cls, data_list: List[Dict[str, Any]]) -> None:
                    """批量新增行 (暂不支持更新)

                    Args:
                    :param data_list: 行数据列表
                    """

                    for data in data_list:
                        for k, v in data.items():
                            if isinstance(v, (dict, list)):
                                data[k] = json.dumps(v, ensure_ascii=False)

                    try:
                        db.bulk_insert_mappings(cls, data_list)
                        db.commit()
                    except Exception:
                        db.rollback()
                        raise

                @classmethod
                def get_by_pk(cls, pk_value: Any):
                    """根据主键查询行

                    Args:
                    :param pk_value: 行主键值

                    Returns:
                    :return: 行对象 (不存在则返回 None)
                    """

                    return (
                        db.query(cls)
                        .filter(getattr(cls, primary_key) == pk_value)
                        .first()
                    )

                @classmethod
                def get_by_field(cls, field: str, value: str):
                    """根据字段查询行"""

                    obj = db.query(cls)
                    if not hasattr(cls, field):
                        raise ValueError(f"Invalid field: {field}")
                    return obj.filter(getattr(cls, field) == value).first()

                @classmethod
                def filter(cls: Type[T], **kwarg) -> List[T]:
                    """筛选数据行"""

                    obj = db.query(cls)
                    for k, v in kwarg.items():
                        if not hasattr(cls, k):
                            raise ValueError(f"Invalid field: {k}")
                        obj = obj.filter(getattr(cls, k) == v)
                    return obj.all()

                @classmethod
                def get_all(cls: Type[T]) -> List[T]:
                    """查询所有行"""

                    return db.query(cls).all()  # type: ignore

                def update(
                    self,
                    data: Optional[Dict[str, Any]] = None,
                    auto_convert_json: bool = True,
                    **kwarg,
                ):
                    """更新行"""

                    if not data:
                        data = {}

                    data.update(kwarg)

                    for k, v in data.items():
                        if isinstance(v, (dict, list)) and auto_convert_json:
                            data[k] = json.dumps(v, ensure_ascii=False)
                        else:
                            raise ValueError(f"Invalid value type: {type(v)}")
                    for k, v in data.items():
                        setattr(self, k, v)
                    db.commit()
                    return self

                def compare_change(self, new_data: Dict[str, Any]) -> List[str]:
                    """比较新旧数据的变化，返回发生变化的字段名"""

                    for k, v in new_data.items():
                        if isinstance(v, (dict, list)):
                            new_data[k] = json.dumps(v, ensure_ascii=False)
                    changed_fields = []
                    for key, value in new_data.items():
                        if str(getattr(self, key)) != str(value):
                            changed_fields.append(key)
                    return changed_fields

                def delete(self) -> None:
                    """删除行"""

                    try:
                        db.delete(self)
                        db.commit()
                        del self
                    except Exception:
                        db.rollback()
                        raise

                @classmethod
                def auto_insert(cls: Type[T], **kwargs) -> T:
                    """自动插入行 (不存在则新增)

                    Args:
                    :param kwargs: 行数据

                    Returns:
                    :return: 行对象
                    """

                    if primary_key in kwargs:
                        item = cls.get_by_pk(kwargs[primary_key])
                        if item:
                            return item.update(kwargs)
                    return cls.add(**kwargs)

                @classmethod
                def auto_insert_by_field(
                    cls: Type[T],
                    field: str,
                    value: str,
                    **kwargs,
                ) -> T:
                    """根据字段自动插入行 (不存在则新增)

                    Args:
                    :param field: 字段名
                    :param value: 字段值
                    :param kwargs: 行数据

                    Returns:
                    :return: 行对象
                    """

                    item = cls.get_by_field(field, value)
                    if item:
                        return item.update(data=kwargs)
                    return cls.add(**kwargs)

                @classmethod
                def sqa_query(cls: Type[T]) -> Query[T]:
                    """获取 SQLAlchemy 查询对象0

                    Returns:
                    :return: SQLAlchemy 查询对象

                    Examples:
                    >>> 基础分页查询: query = ModelClass.sqa_query().filter(ModelClass.id > 0).order_by(ModelClass.id.desc()).limit(10)
                    """
                    return db.query(cls)

            return ModelClass

        return modal_class_wrapper
