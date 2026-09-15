from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os
from sqlalchemy import (
    String, Boolean, DateTime, Float, Integer, ForeignKey, Text
)

DB_URL = 'postgresql://postgres:674@localhost:5432/freshmart'

engine = create_engine(
    DB_URL,
    pool_pre_ping=True,
    pool_recycle=300,
)

localSession = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


class Base(DeclarativeBase):
    pass


def get_db():
    db = localSession()
    try:
        yield db
    finally:
        db.close()


def _column_ddl(col) -> str:
    python_type = col.type
    type_name = type(python_type).__name__.lower()

    if isinstance(python_type, Text):
        sql_type = "TEXT"
    elif isinstance(python_type, String):
        sql_type = f"VARCHAR({python_type.length})" if python_type.length else "VARCHAR"
    elif isinstance(python_type, Integer):
        sql_type = "INTEGER"
    elif isinstance(python_type, Float):
        sql_type = "FLOAT"
    elif isinstance(python_type, Boolean):
        sql_type = "BOOLEAN"
    elif isinstance(python_type, DateTime):
        sql_type = "TIMESTAMP"
    else:
        sql_type = "TEXT"

    nullable = "NULL" if col.nullable else "NOT NULL"

    default = ""
    if col.default is not None and col.default.arg is not None and not callable(col.default.arg):
        val = col.default.arg
        if isinstance(val, bool):
            default = f" DEFAULT {str(val).upper()}"
        elif isinstance(val, (int, float)):
            default = f" DEFAULT {val}"
        elif isinstance(val, str):
            escaped = val.replace("'", "''")
            default = f" DEFAULT '{escaped}'"

    return f"{sql_type} {nullable}{default}"


def auto_sync_schema():
    try:
        inspector = inspect(engine)
        with engine.begin() as conn:
            for table in Base.metadata.sorted_tables:
                table_name = table.name
                if not inspector.has_table(table_name):
                    continue

                existing_cols = {c["name"]: c for c in inspector.get_columns(table_name)}

                for col in table.columns:
                    if col.name in existing_cols:
                        continue

                    ddl = _column_ddl(col)
                    sql = f'ALTER TABLE "{table_name}" ADD COLUMN IF NOT EXISTS "{col.name}" {ddl}'
                    conn.execute(text(sql))
                    print(f"[auto-sync] ALTER TABLE {table_name} ADD COLUMN {col.name} {ddl}")
    except Exception as e:
        print(f"[auto-sync] skipped: {e}")
