# Miose Toolkit 工具箱: Database 子项目

## 介绍

Database 子项目包含了一个对 sqlalchemy 进行了简单封装和对象化的数据库工具。

## 测试用例库 -> [用例库](/tests/db)

测试用例库中包含了所有模块的测试用例，可以参考其中的代码来使用模块。

## 功能列表

### 1. 数据库链接生成器 [测试用例](/tests/db/test_db_url.py)

数据库链接生成器可以帮助你快速生成数据库链接，基本使用如下:

```python
from miose_toolkit_db import (
    gen_mysql_db_url,
    gen_postgresql_db_url,
    gen_sqlite_db_url,
)

# 生成 MySQL 数据库链接
mysql_url = gen_mysql_db_url(
    host="test_host",
    port=3306,
    user="test_user",
    password="test_password",
    database="test_database",
    charset="utf8mb4",
)

# 生成 PostgreSQL 数据库链接
postgresql_url = gen_postgresql_db_url(
    host="test_host",
    port=5432,
    user="test_user",
    password="test_password",
    database="test_database",
    sslmode="prefer",
)

# 生成 SQLite 数据库链接
sqlite_url = gen_sqlite_db_url(db_path="test.db")
```

### 2. 数据库 ORM 工具 [测试用例](/tests/db/test_orm.py)

数据库 ORM 工具可以帮助你对象化数据库表，基本使用如下:

```python
from miose_toolkit_db import (
    asc,
    gen_sqlite_db_url,
    desc,
    Column,
    Mapped,
    MappedColumn,
    MioModel,
    MioOrm,
)

# 引入 sqlalchemy 数据字段模型
from sqlalchemy import String, Text

# 创建数据库连接 (以 SQLite 为例，可搭配数据库链接生成器使用其它数据库)
db = MioOrm(gen_sqlite_db_url("test.db"))

# 定义数据模型 (推荐使用注解方式)
@db.reg_predefine_data_model(table_name="test", primary_key="id")
class DBTest(MioModel):
    id: Mapped[str] = MappedColumn(String(length=28), primary_key=True)
    name: Mapped[str] = MappedColumn(String(length=128), comment="名称")
    url: Mapped[str] = MappedColumn(String(length=256), comment="链接")
    extra_info: Mapped[dict] = MappedColumn(Text, comment="额外信息")
    # ... 其他字段

# 创建数据表
db.create_all()

# 添加行 (直接添加)
DBTest.add(
    id="1",
    name="test_name",
    url="http://example.com/1",
    extra_info={"key": "value1"},
    # ... 其他字段
)

# 添加行 (字段提示方式 - 推荐)
DBTest.add(
    data={
        DBTest.id.key: "1",
        DBTest.name.key: "TestName1",
        DBTest.url.key: "http://example.com/1",
        DBTest.extra_info.key: {"key": "value1"},
    },
    convert_json=True,  # 自动序列化 JSON 字段
)

# 单条查询数据
retrieved_data = DBTest.get_by_pk("1")
print(retrieved_data.name)  # 输出: test_name

# 单条查询数据 (字段查询)
retrieved_data = DBTest.get_by_field(
    field=DBTest.name,  # 查询字段
    value="TestName1",  # 查询值
    allow_multiple=False    # 是否允许多条数据 (默认 False， 即查询结果不唯一则报错)
)
print(retrieved_data.url)  # 输出: http://example.com/1

# 简单过滤查询
filtered_data = DBTest.filter(
    conditions={
        DBTest.name: "TestName1",
    }
)

# 复杂过滤查询
filtered_data = DBTest.filter(
    conditions={DBTest.name: "AutoInsertName"},  # 条件
    fields=[DBTest.name],   # 指定返回字段
    order_by=[desc(DBTest.id)],  # 排序
    limit=10,    # 限制返回条数
    offset=0,    # 偏移量
)

# 更新数据 (直接更新)
retrieved_data.update(
    name="NewName",
    ... # 其他字段
)

# 更新数据 (字段提示方式 - 推荐)
retrieved_data.update(
    data={
        DBTest.name.key: "NewName2",
        DBTest.url.key: "http://example.com/2",
        DBTest.extra_info.key: {"key": "value2"},
    },
    convert_json=True,  # 自动序列化 JSON 字段
)

# 删除数据
retrieved_data.delete()

# 关闭数据库连接
db.close_db_connection()
```
