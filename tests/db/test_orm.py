from pathlib import Path

from miose_toolkit_db import (
    Mapped,
    MappedColumn,
    MioModel,
    MioOrm,
    asc,
    desc,
    gen_sqlite_db_url,
)
from sqlalchemy import String


def test_orm():
    # 删除如果存在的测试数据库
    Path("test1.temp.db").unlink(True)
    Path("test2.temp.db").unlink(True)

    # 创建数据库连接
    db1 = MioOrm(gen_sqlite_db_url("test1.temp.db"))
    db2 = MioOrm(gen_sqlite_db_url("test2.temp.db"))

    @db1.reg_predefine_data_model(table_name="test", primary_key="id")
    class DBTest1(MioModel):
        id: Mapped[str] = MappedColumn(String(length=28), primary_key=True)
        name: Mapped[str] = MappedColumn(String(length=128), comment="名称")
        url: Mapped[str] = MappedColumn(String(length=256), comment="链接")
        extra_info: Mapped[str] = MappedColumn(String(length=1024), comment="额外信息")

    @db2.reg_predefine_data_model(table_name="test", primary_key="id")
    class DBTest2(MioModel):
        id: Mapped[str] = MappedColumn(String(length=28), primary_key=True)
        name: Mapped[str] = MappedColumn(String(length=128), comment="名称")
        url: Mapped[str] = MappedColumn(String(length=256), comment="链接")
        extra_info: Mapped[str] = MappedColumn(String(length=1024), comment="额外信息")

    # 创建数据表
    db1.create_all()
    db2.create_all()

    # 添加测试数据到第一个数据
    DBTest1.add(
        data={
            DBTest1.id: "1",
            DBTest1.name: "TestName1",
            DBTest1.url: "http://example.com/1",
            DBTest1.extra_info: {"key": "value1"},
        },
    )

    # 根据 ID 查询数据
    retrieved_data1 = DBTest1.get_by_pk("1")
    assert retrieved_data1 and retrieved_data1.name == "TestName1"

    # 根据 字段查询数据
    retrieved_data2 = DBTest1.get_by_field(field=DBTest1.name, value="TestName1")
    assert retrieved_data2 and retrieved_data2.name == "TestName1"

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
    retrieved_data3 = DBTest2.get_by_pk("1")
    assert retrieved_data3 and retrieved_data3.name == "TestName2"

    # 测试删除数据
    retrieved_data3.delete()
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

    # 测试筛选
    filtered_data = DBTest2.filter(conditions={DBTest2.name: "AutoInsertName"})
    assert len(filtered_data) == 1
    assert filtered_data[0].name == "AutoInsertName"  # type:ignore

    # 测试复杂筛选
    filtered_data = DBTest2.filter(
        conditions={DBTest2.name: "AutoInsertName"},
        fields=[DBTest2.name],
        order_by=[desc(DBTest2.id)],
        limit=1,
        offset=0,
    )
    assert len(filtered_data) == 1
    assert filtered_data[0].name == "AutoInsertName"
    try:
        assert filtered_data[0].url is None  # type:ignore
    except AttributeError:
        pass
    else:
        raise Exception("Failed to filter data with specified fields")

    # 关闭数据库连接
    db1.close_db_connection()
    db2.close_db_connection()

    # 删除测试数据库
    Path("test1.temp.db").unlink(True)
    Path("test2.temp.db").unlink(True)


if __name__ == "__main__":
    test_orm()
