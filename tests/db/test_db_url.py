from miose_toolkit_db import (
    gen_mysql_db_url,
    gen_postgresql_db_url,
    gen_sqlite_db_url,
)


def test_db_url_generator():
    assert gen_mysql_db_url() == "mysql+pymysql://root:@localhost:3306/"
    assert (
        gen_mysql_db_url(
            host="test_host",
            port=3306,
            user="test_user",
            password="test_password",
            database="test_database",
            charset="utf8mb4",
        )
        == "mysql+pymysql://test_user:test_password@test_host:3306/test_database?charset=utf8mb4"
    )

    assert gen_postgresql_db_url() == "postgresql://postgres:@localhost:5432/"
    assert (
        gen_postgresql_db_url(
            host="test_host",
            port=5432,
            user="test_user",
            password="test_password",
            database="test_database",
            sslmode="prefer",
        )
        == "postgresql://test_user:test_password@test_host:5432/test_database?sslmode=prefer"
    )

    assert gen_sqlite_db_url("test.db") == "sqlite:///./test.db"
    assert gen_sqlite_db_url("./test.db") == "sqlite:///./test.db"
    assert gen_sqlite_db_url("/test.db") == "sqlite:////test.db"
