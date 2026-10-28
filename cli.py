"""Menu-driven terminal interface (7 options from the report + optional chart)."""

import argparse
import csv

from . import db
from .report import export_report
from .scoring import INDICATORS, classify, is_high_priority, validate_score

MENU = """
=== Community Quality-of-Life Indicator Analyzer ===
[1] Add Community Telemetry
[2] View All Records
[3] Calculate Composite Scores
[4] Identify Weakest/Strongest Indicators
[5] Comparative Community Ranking
[6] Export Development Audit Report
[7] Exit
[8] Plot Community Chart (needs matplotlib)
"""


def _prompt_score(label):
    while True:
        score = validate_score(input(f"Enter {label} score (0-100): "))
        if score is not None:
            return score
        print("  Invalid input - enter a number between 0 and 100.")


def add_record():
    name = input("Enter Community Name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return
    scores = {i: _prompt_score(i) for i in INDICATORS}
    comp, strong, weak = db.add_community(name, scores)
    print(f"Saved {name}! QoLI: {comp} | Best: {strong} | Weakest: {weak}")


def view_all():
    rows = db.fetch_all()
    if not rows:
        print("No records yet.")
        return
    print(f"{'Community':<18}" + "".join(f"{i[:6]:>8}" for i in INDICATORS) + f"{'QoLI':>8}")
    for r in rows:
        print(f"{r['community_name']:<18}"
              + "".join(f"{r[i.lower()]:>8.1f}" for i in INDICATORS)
              + f"{r['composite_score']:>8.2f}")


def show_scores():
    for r in db.fetch_all():
        print(f"{r['community_name']:<18} QoLI = {r['composite_score']:>6.2f}  "
              f"[{classify(r['composite_score'])}]")


def show_extremes():
    for r in db.fetch_all():
        print(f"{r['community_name']:<18} Strongest: {r['strongest_indicator']:<12} "
              f"Weakest: {r['weakest_indicator']}")


def show_ranking():
    rows = db.fetch_all(order_by_score=True)
    for rank, r in enumerate(rows, 1):
        alert = "  <-- HIGH PRIORITY FOR INTERVENTION" if is_high_priority(db.row_scores(r)) else ""
        print(f"{rank}. {r['community_name']:<18} {r['composite_score']:>6.2f}{alert}")


def plot_chart():
    name = input("Community to plot: ").strip()
    try:
        from .plotting import plot_community
        print(f"Chart saved to {plot_community(name)}")
    except ImportError:
        print("matplotlib is not installed. Run: pip install matplotlib")
    except ValueError as exc:
        print(exc)


def import_csv(path):
    """Bulk-load communities from a CSV with columns: Community + 5 indicators."""
    count = 0
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            scores = {i: validate_score(row[i]) for i in INDICATORS}
            if None in scores.values():
                print(f"Skipping {row.get('Community')}: invalid score.")
                continue
            db.add_community(row["Community"], scores)
            count += 1
    return count


ACTIONS = {"1": add_record, "2": view_all, "3": show_scores,
           "4": show_extremes, "5": show_ranking}


def main():
    parser = argparse.ArgumentParser(description="Community QoL Indicator Analyzer")
    parser.add_argument("--import", dest="csv_path", help="CSV file to import before starting")
    args = parser.parse_args()

    db.init_db()
    if args.csv_path:
        print(f"Imported {import_csv(args.csv_path)} communities.")

    while True:
        print(MENU)
        choice = input("Choice: ").strip()
        if choice in ACTIONS:
            ACTIONS[choice]()
        elif choice == "6":
            print(f"Report saved to {export_report()}")
        elif choice == "8":
            plot_chart()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")
