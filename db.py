"""
Database abstraction layer — works with both SQLite (local) and PostgreSQL (Railway).
Set DATABASE_URL environment variable to use PostgreSQL.
If not set, falls back to SQLite for local development.
"""
import os
import sqlite3

DATABASE_URL = os.environ.get('DATABASE_URL', '')

# Railway injects postgres:// but psycopg2 needs postgresql://
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

USE_PG = bool(DATABASE_URL)

if USE_PG:
    import psycopg2
    import psycopg2.extras

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_DATA = os.environ.get('DATA_DIR') or os.environ.get('RAILWAY_VOLUME_MOUNT_PATH') or BASE_DIR
SQLITE_PATH = os.environ.get('SQLITE_PATH') or os.path.join(_DATA, 'geometry_delivery.db')


def get_db():
    """Return a database connection wrapped in a unified interface."""
    if USE_PG:
        conn = psycopg2.connect(DATABASE_URL)
        conn.autocommit = False
        return PGConnection(conn)
    else:
        conn = sqlite3.connect(SQLITE_PATH)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys=ON")
        return SQLiteConnection(conn)


# ── SQLite wrapper (unchanged behaviour) ──────────────────────────────────
class SQLiteConnection:
    def __init__(self, conn):
        self._conn = conn

    def execute(self, sql, params=()):
        sql = _pg_to_sqlite(sql)
        return self._conn.execute(sql, params)

    def cursor(self):
        return self._conn.cursor()

    def executescript(self, sql):
        # executescript only on SQLite
        self._conn.executescript(sql)

    def commit(self):
        self._conn.commit()

    def close(self):
        self._conn.close()

    def __enter__(self): return self
    def __exit__(self, *a): self._conn.close()


# ── PostgreSQL wrapper ─────────────────────────────────────────────────────
class PGConnection:
    def __init__(self, conn):
        self._conn = conn
        self._cur  = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def execute(self, sql, params=()):
        sql = _sqlite_to_pg(sql)
        self._cur.execute(sql, params or None)
        return PGCursor(self._cur)

    def cursor(self):
        return self._cur

    def executescript(self, sql):
        """Run multiple statements separated by semicolons."""
        for stmt in sql.split(';'):
            stmt = stmt.strip()
            if stmt:
                try:
                    self._cur.execute(_sqlite_to_pg(stmt))
                    self._conn.commit()
                except Exception as e:
                    # Roll back failed statement but continue (IF NOT EXISTS handles duplicates)
                    self._conn.rollback()

    def commit(self):
        self._conn.commit()

    def close(self):
        try: self._conn.commit()
        except: pass
        self._conn.close()

    def __enter__(self): return self
    def __exit__(self, *a): self.close()


class PGCursor:
    """Thin wrapper so .fetchone() / .fetchall() work like sqlite3.Row."""
    def __init__(self, cur):
        self._cur = cur

    def fetchone(self):
        row = self._cur.fetchone()
        return DictRow(row) if row else None

    def fetchall(self):
        rows = self._cur.fetchall()
        return [DictRow(r) for r in rows]

    def __iter__(self):
        for row in self._cur:
            yield DictRow(row)


class DictRow:
    """Behaves like sqlite3.Row — supports both dict-key and index access."""
    def __init__(self, d):
        self._d = dict(d) if d else {}

    def __getitem__(self, key):
        if isinstance(key, int):
            return list(self._d.values())[key]
        return self._d[key]

    def __contains__(self, key):
        return key in self._d

    def get(self, key, default=None):
        return self._d.get(key, default)

    def keys(self):
        return self._d.keys()

    def items(self):
        return self._d.items()

    def __iter__(self):
        return iter(self._d)

    def __repr__(self):
        return f"DictRow({self._d})"


# ── SQL dialect helpers ────────────────────────────────────────────────────
def _sqlite_to_pg(sql):
    """Convert SQLite SQL to PostgreSQL SQL."""
    import re
    # ? placeholders → %s
    sql = re.sub(r'\?', '%s', sql)
    # INTEGER PRIMARY KEY AUTOINCREMENT → SERIAL PRIMARY KEY
    sql = re.sub(r'INTEGER PRIMARY KEY AUTOINCREMENT', 'SERIAL PRIMARY KEY', sql, flags=re.I)
    # CURRENT_TIMESTAMP stays the same
    # TEXT → TEXT (same)
    # INTEGER DEFAULT 1 → INTEGER DEFAULT 1 (same)
    # Remove PRAGMA
    sql = re.sub(r'PRAGMA\s+\w+.*', '', sql, flags=re.I)
    return sql

def _pg_to_sqlite(sql):
    """No-op — SQLite SQL is already correct for SQLite."""
    return sql


def last_insert_id(conn, table=''):
    """Get last inserted ID in a DB-agnostic way."""
    if USE_PG:
        # Use lastval() - works after any INSERT (no RETURNING needed)
        try:
            row = conn._cur.fetchone()
            if row:
                d = dict(row) if not isinstance(row, DictRow) else row._d
                return list(d.values())[0]
        except Exception:
            pass
        # Fallback to lastval()
        conn._cur.execute("SELECT lastval()")
        row = conn._cur.fetchone()
        return list(dict(row).values())[0] if row else None
    else:
        return conn._conn.execute("SELECT last_insert_rowid()").fetchone()[0]


def returning_id(sql, table=''):
    """Append RETURNING id for PostgreSQL inserts."""
    if USE_PG:
        return sql + ' RETURNING id'
    return sql
