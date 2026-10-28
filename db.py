"""SQLite persistence layer."""

import sqlite3

from .scoring import INDICATORS, composite_score, identify_extremes

DEFAULT_DB = "quality_of_life.db"

SCHEMA = """CREATE TABLE IF NOT EXISTS community_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    community_name TEXT UNIQUE NOT NULL,
    healthcare REAL, education REAL, transport REAL,
    safety REAL, environment REAL,
    composite_score REAL,
    strongest_indicator TEXT,
    weakest_indicator TEXT
)"""


def init_db(db_name=DEFAULT_DB):
    conn = sqlite3.connect(db_name)
    with conn:
        conn.execute(SCHEMA)
    conn.close()


def add_community(name, scores, db_name=DEFAULT_DB):
    """Validate bounds, compute metrics, insert/replace. Returns (comp, strong, weak)."""
    for key, value in scores.items():
        if not 0 <= value <= 100:
            raise ValueError(f"Score for {key} out of bounds (0-100).")
    comp = composite_score(scores)
    strong, weak = identify_extremes(scores)
    conn = sqlite3.connect(db_name)
    with conn:
        conn.execute(
            """INSERT OR REPLACE INTO community_metrics
               (community_name, healthcare, education, transport, safety,
                environment, composite_score, strongest_indicator, weakest_indicator)
               VALUES (?,?,?,?,?,?,?,?,?)""",
            (name, *(scores[i] for i in INDICATORS), comp, strong, weak),
        )
    conn.close()
    return comp, strong, weak


def fetch_all(db_name=DEFAULT_DB, order_by_score=False):
    """Return all communities as a list of dicts."""
    query = "SELECT * FROM community_metrics"
    if order_by_score:
        query += " ORDER BY composite_score DESC"
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    rows = [dict(r) for r in conn.execute(query)]
    conn.close()
    return rows


def row_scores(row):
    """Extract the indicator dict from a DB row."""
    return {i: row[i.lower()] for i in INDICATORS}
