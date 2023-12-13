from pathlib import Path
from typing import TYPE_CHECKING

from sqlalchemy import Column, String

if TYPE_CHECKING:
    from ..miose_toolkit_db import (
        MDb,
        gen_sqlite_db_url,
    )
else:
    from miose_toolkit_db import (
        MDb,
        gen_sqlite_db_url,
    )


def test_orm():
    # 删除如果存在的测试数据库
    Path("test1.temp.db").unlink(True)
    Path("test2.temp.db").unlink(True)

    # 创建数据库连接
    db1 = MDb(gen_sqlite_db_url("test1.temp.db"))
    db2 = MDb(gen_sqlite_db_url("test2.temp.db"))

    @db1.reg_predefine_data_model(table_name="test", primary_key="id")
    class DBTest1:
        id = Column(String(length=28), primary_key=True)
        name = Column(String(length=128), comment="名称")
        url = Column(String(length=256), comment="链接")
        extra_info = Column(String(length=1024), comment="额外信息")

    @db2.reg_predefine_data_model(table_name="test", primary_key="id")
    class DBTest2:
        id = Column(String(length=28), primary_key=True)
        name = Column(String(length=128), comment="名称")
        url = Column(String(length=256), comment="链接")
        extra_info = Column(String(length=1024), comment="额外信息")

    # 创建数据表
    db1.create_all()
    db2.create_all()

    # 添加测试数据到第一个数据库
    test_data1 = {
        "id": "1",
        "name": "TestName1",
        "url": "http://example.com/1",
        "extra_info": {"key": "value1"},
    }

    DBTest1.add(**test_data1)

    # 根据 ID 查询数据
    retrieved_data1 = DBTest1.get_by_pk("1")
    assert retrieved_data1.name == "TestName1"  # type:ignore

    # 从第一个数据库提取一条数据
    retrieved_data1 = DBTest1.get_by_pk("1")

    # 插入到第二个数据库
    if retrieved_data1:
        test_data2 = {
            "id": retrieved_data1.id,
            "name": "TestName2",
            "url": "http://example.com/2",
            "extra_info": {"key": "value2"},
        }
        DBTest2.add(**test_data2)
    else:
        raise Exception("Failed to get data from DBTest1")

    # 查询第二个数据库
    retrieved_data2 = DBTest2.get_by_pk("1")
    assert retrieved_data2.name == "TestName2"  # type:ignore

    # 测试删除数据
    DBTest2.delete(retrieved_data2)
    deleted_data2 = DBTest2.get_by_pk("1")
    assert deleted_data2 is None

    # 测试自动插入数据
    auto_insert_data = {
        "id": "2",
        "name": "AutoInsertName",
        "url": "http://example.com/auto",
        "extra_info": {"key": "auto_value"},
    }

    DBTest2.auto_insert(**auto_insert_data)

    # 测试批量插入数据 (暂不支持重复主键更新)
    DBTest2.batch_add(
        [
            {
                "id": "3",
                "name": "BatchInsertName",
                "url": "http://example.com/batch",
                "extra_info": {"key": "batch_value"},
            },
            {
                "id": "4",
                "name": "BatchInsertName",
                "url": "http://example.com/batch",
                "extra_info": {"key": "batch_value"},
            },
        ],
    )

    # 测试查询所有数据
    all_data = DBTest2.get_all()
    assert len(all_data) == 3

    # 关闭数据库连接
    db1.close_db_connection()
    db2.close_db_connection()

    # 删除测试数据库
    Path("test1.temp.db").unlink(True)
    Path("test2.temp.db").unlink(True)
