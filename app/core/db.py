from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os
from sqlalchemy import (
    String, Boolean, DateTime, Float, Integer, ForeignKey, Text
)

DB_URL = 'postgresql://neondb_owner:npg_aqNj3ZfOKkB7@ep-rapid-queen-aecqqwut-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require'

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
            _clean_enum_data(conn, inspector)

            for table in Base.metadata.sorted_tables:
                table_name = table.name
                if not inspector.has_table(table_name):
                    continue

                existing_cols = {c["name"]: c for c in inspector.get_columns(table_name)}

                _rename_columns(conn, table_name, existing_cols)

                existing_cols = {c["name"]: c for c in inspector.get_columns(table_name)}

                for col in table.columns:
                    if col.name in existing_cols:
                        continue

                    ddl = _column_ddl(col)
                    sql = f'ALTER TABLE "{table_name}" ADD COLUMN IF NOT EXISTS "{col.name}" {ddl}'
                    conn.execute(text(sql))
                    print(f"[auto-sync] ALTER TABLE {table_name} ADD COLUMN {col.name} {ddl}")

            _add_enum_check_constraints(conn, inspector)
    except Exception as e:
        print(f"[auto-sync] skipped: {e}")


def _clean_enum_data(conn, inspector):
    for table in Base.metadata.sorted_tables:
        table_name = table.name
        if not inspector.has_table(table_name):
            continue

        for col in table.columns:
            col_type = col.type
            if not (isinstance(col_type, Enum) and not col_type.native_enum):
                continue

            quoted = f'"{col.name}"'
            sql = (
                f'UPDATE "{table_name}" SET {quoted} = TRIM({quoted}) '
                f'WHERE {quoted} IS NOT NULL AND {quoted} <> TRIM({quoted})'
            )
            result = conn.execute(text(sql))
            if result.rowcount:
                print(f"[auto-sync] trimmed {result.rowcount} rows in {table_name}.{col.name}")


def _add_enum_check_constraints(conn, inspector):
    for table in Base.metadata.sorted_tables:
        table_name = table.name
        if not inspector.has_table(table_name):
            continue

        for col in table.columns:
            col_type = col.type
            if not (isinstance(col_type, Enum) and not col_type.native_enum):
                continue

            enum_class = getattr(col_type, "enum_class", None)
            if enum_class is None:
                continue

            values = [m.value for m in enum_class]
            values_list = ", ".join(f"'{v}'" for v in values)
            constraint_name = f"{table_name}_{col.name}_check"

            exists = conn.execute(
                text(
                    "SELECT 1 FROM information_schema.table_constraints "
                    "WHERE table_name = :table_name AND constraint_name = :constraint_name"
                ),
                {"table_name": table_name, "constraint_name": constraint_name},
            ).first()

            if exists:
                continue

            sql = (
                f'ALTER TABLE "{table_name}" ADD CONSTRAINT "{constraint_name}" '
                f'CHECK ("{col.name}" IN ({values_list}))'
            )
            conn.execute(text(sql))
            print(f"[auto-sync] ADD CONSTRAINT {constraint_name} CHECK ({col.name} IN ({values_list}))")


COLUMN_RENAMES = {
    "orders": {
        "discount_price": "coupon_value",
    },
}


def _rename_columns(conn, table_name: str, existing_cols: dict):
    renames = COLUMN_RENAMES.get(table_name, {})
    for old_name, new_name in renames.items():
        if old_name in existing_cols and new_name not in existing_cols:
            sql = f'ALTER TABLE "{table_name}" RENAME COLUMN "{old_name}" TO "{new_name}"'
            conn.execute(text(sql))
            print(f"[auto-sync] RENAME {table_name}.{old_name} -> {new_name}")
