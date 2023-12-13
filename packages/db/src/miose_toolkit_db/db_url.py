from urllib.parse import quote_plus


def gen_mysql_db_url(
    host: str = "localhost",
    port: int = 3306,
    user: str = "root",
    password: str = "",
    database: str = "",
    charset: str = "",
) -> str:
    """生成 MySQL 数据库连接 URL"""

    user = quote_plus(user)
    password = quote_plus(password)
    database = quote_plus(database)
    charset = quote_plus(charset)

    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}{charset and f'?charset={charset}'}"


def gen_postgresql_db_url(
    host: str = "localhost",
    port: int = 5432,
    user: str = "postgres",
    password: str = "",
    database: str = "",
    sslmode: str = "",
) -> str:
    """生成 PostgreSQL 数据库连接 URL"""

    user = quote_plus(user)
    password = quote_plus(password)
    database = quote_plus(database)
    sslmode = quote_plus(sslmode)

    return f"postgresql://{user}:{password}@{host}:{port}/{database}{sslmode and f'?sslmode={sslmode}'}"


def gen_sqlite_db_url(db_path: str) -> str:
    """生成 SQLite 数据库连接 URL"""

    if not db_path.startswith("/") and not db_path.startswith("./"):
        db_path = f"./{db_path}"

    return f"sqlite:///{db_path}"
