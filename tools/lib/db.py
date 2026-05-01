"""SQLite schema and DB helpers for APV v2 knowledge base."""

import sqlite3
from pathlib import Path

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS knowledge_pages (
    path TEXT PRIMARY KEY,
    domain TEXT NOT NULL,
    type TEXT NOT NULL,
    title TEXT,
    source_url TEXT,
    captured_date TEXT DEFAULT (date('now')),
    last_verified TEXT,
    freshness_days INTEGER DEFAULT 90,
    tags TEXT,
    content_hash TEXT
);

CREATE VIEW IF NOT EXISTS stale_knowledge AS
SELECT * FROM knowledge_pages
WHERE julianday('now') - julianday(last_verified) > freshness_days;

CREATE TABLE IF NOT EXISTS pricing (
    provider TEXT NOT NULL,
    region TEXT NOT NULL,
    service TEXT NOT NULL,
    instance_type TEXT,
    hourly_price REAL,
    monthly_price REAL,
    pricing_model TEXT,
    source_url TEXT,
    verified_date TEXT,
    PRIMARY KEY (provider, region, service, instance_type)
);

CREATE TABLE IF NOT EXISTS compliance (
    framework TEXT NOT NULL,
    country TEXT,
    requirement_id TEXT,
    title TEXT,
    summary TEXT,
    source_url TEXT,
    PRIMARY KEY (framework, requirement_id)
);

CREATE TABLE IF NOT EXISTS infrastructure (
    provider TEXT NOT NULL,
    service TEXT NOT NULL,
    category TEXT,
    features TEXT,
    regions TEXT,
    source_url TEXT,
    PRIMARY KEY (provider, service)
);

CREATE TABLE IF NOT EXISTS knowledge_gaps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project TEXT,
    domain TEXT,
    description TEXT,
    severity TEXT DEFAULT 'medium',
    resolved INTEGER DEFAULT 0,
    created_date TEXT DEFAULT (date('now')),
    resolved_date TEXT
);
"""


def create_schema(db_path: Path) -> sqlite3.Connection:
    """Create all tables/views and return connection with Row factory."""
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA_SQL)
    return conn


def insert_knowledge_page(conn: sqlite3.Connection, page: dict) -> None:
    """INSERT OR REPLACE a knowledge page."""
    conn.execute(
        """INSERT OR REPLACE INTO knowledge_pages
           (path, domain, type, title, source_url, last_verified, freshness_days)
           VALUES (:path, :domain, :type, :title, :source_url, :last_verified, :freshness_days)""",
        page,
    )
    conn.commit()


def get_stale_pages(conn: sqlite3.Connection) -> list[dict]:
    """Query the stale_knowledge view."""
    rows = conn.execute("SELECT * FROM stale_knowledge").fetchall()
    return [dict(r) for r in rows]


def insert_pricing(conn: sqlite3.Connection, entry: dict) -> None:
    """INSERT OR REPLACE a pricing entry."""
    conn.execute(
        """INSERT OR REPLACE INTO pricing
           (provider, region, service, instance_type, hourly_price, monthly_price, source_url, verified_date)
           VALUES (:provider, :region, :service, :instance_type, :hourly_price, :monthly_price, :source_url, :verified_date)""",
        entry,
    )
    conn.commit()
