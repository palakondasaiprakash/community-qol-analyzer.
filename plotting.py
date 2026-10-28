"""Optional bar chart of a community's indicator scores (needs matplotlib)."""

from .db import fetch_all, row_scores
from .scoring import identify_extremes


def plot_community(name, filename=None, db_name="quality_of_life.db", show=False):
    import matplotlib
    if not show:
        matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    row = next((r for r in fetch_all(db_name) if r["community_name"] == name), None)
    if row is None:
        raise ValueError(f"Community '{name}' not found.")
    scores = row_scores(row)
    strong, weak = identify_extremes(scores)
    colors = ["#2ea05c" if k == strong else "#d9534f" if k == weak else "#4e79a7"
              for k in scores]

    fig, ax = plt.subplots(figsize=(7, 4.5))
    bars = ax.bar(scores.keys(), scores.values(), color=colors, width=0.6)
    for bar, v in zip(bars, scores.values()):
        ax.text(bar.get_x() + bar.get_width() / 2, v + 1.5, f"{v:g}",
                ha="center", fontweight="bold")
    ax.axhline(row["composite_score"], color="gray", linestyle="--")
    ax.text(len(scores) - 0.5, row["composite_score"] + 1,
            f"Composite: {row['composite_score']}", ha="right", color="gray")
    ax.set_ylim(0, 100)
    ax.set_ylabel("Score (0-100)")
    ax.set_title(f"Quality of Life Scores - {name}", fontweight="bold")
    fig.tight_layout()

    filename = filename or f"reports/{name.replace(' ', '_')}_scores.png"
    fig.savefig(filename, dpi=150)
    if show:
        plt.show()
    plt.close(fig)
    return filename
