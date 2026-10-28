"""Text audit-report generation."""

from datetime import datetime

from .db import DEFAULT_DB, fetch_all, row_scores
from .scoring import classify, is_high_priority


def export_report(filename="reports/community_qol_audit.txt", db_name=DEFAULT_DB):
    rows = fetch_all(db_name, order_by_score=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write("=== COMMUNITY QUALITY-OF-LIFE AUDIT REPORT ===\n")
        f.write(f"Generated: {datetime.now():%Y-%m-%d %H:%M}\n\n")
        for rank, r in enumerate(rows, 1):
            flag = "HIGH PRIORITY FOR INTERVENTION" if is_high_priority(row_scores(r)) else "OK"
            f.write(
                f"{rank}. {r['community_name']} | QoLI: {r['composite_score']} "
                f"({classify(r['composite_score'])}) | Best: {r['strongest_indicator']} "
                f"| Deficit: {r['weakest_indicator']} | Status: {flag}\n"
            )
    return filename
