# Miose Toolkit 工具箱: Database 子项目

## 介绍

Database 子项目包含了一个对 sqlalchemy 进行了简单封装的数据库工具。

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
    Column,
    Mapped,
    MappedColumn,
    MioModel,
    MioOrm,
    gen_sqlite_db_url,
)

# 引入 sqlalchemy 数据模型
from sqlalchemy import String

# 创建数据库连接 (以 SQLite 为例，可搭配数据库链接生成器使用其它数据库)
db = MioOrm(gen_sqlite_db_url("test.db"))

# 定义数据模型 (注解方式)
@db.reg_predefine_data_model(table_name="test", primary_key="id")
class DBTest(MioModel):
    id: Mapped[str] = MappedColumn(String(length=28), primary_key=True)
    name: Mapped[str] = MappedColumn(String(length=128), comment="名称")
    # ... 其他字段

# 创建数据表
db.create_all()

# 添加数据
DBTest.add(
    id="1",
    name="test_name",
    # ... 其他字段
)

# 查询数据
retrieved_data = DBTest.get_by_pk("1")
print(retrieved_data.name)  # 输出: test_name

# 更新数据
retrieved_data.update(
    name="NewName",
    ... # 其他字段
)

# 删除数据
retrieved_data.delete()

# 关闭数据库连接
db.close_db_connection()
```
