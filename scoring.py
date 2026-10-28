"""Pure scoring logic (no I/O) - easy to test."""

INDICATORS = ("Healthcare", "Education", "Transport", "Safety", "Environment")

QOLI_THRESHOLD = 65.0       # composite below this -> high priority
INDICATOR_THRESHOLD = 50.0  # any single indicator below this -> high priority


def validate_score(value):
    """Return float(value) if it is numeric and within 0-100, else None."""
    try:
        score = float(value)
    except (TypeError, ValueError):
        return None
    return score if 0.0 <= score <= 100.0 else None


def composite_score(scores):
    """QoLI = arithmetic mean of the indicator scores."""
    return round(sum(scores.values()) / len(scores), 2)


def identify_extremes(scores):
    """Return (strongest, weakest) indicator names: argmax / argmin."""
    strongest = max(scores, key=scores.get)
    weakest = min(scores, key=scores.get)
    return strongest, weakest


def is_high_priority(scores):
    """High priority if QoLI < 65 OR any indicator < 50."""
    return (
        composite_score(scores) < QOLI_THRESHOLD
        or any(v < INDICATOR_THRESHOLD for v in scores.values())
    )


def classify(qoli):
    """Human-readable performance band for a composite score."""
    if qoli >= 80:
        return "Excellent"
    if qoli >= 65:
        return "Good"
    if qoli >= 50:
        return "Needs Improvement"
    return "Critical"
