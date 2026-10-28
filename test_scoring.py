import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qol_analyzer import db
from qol_analyzer.scoring import (composite_score, identify_extremes,
                                  is_high_priority, validate_score)

AREA_H = {"Healthcare": 75, "Education": 82, "Transport": 60,
          "Safety": 70, "Environment": 68}
AREA_D = {"Healthcare": 50, "Education": 60, "Transport": 45,
          "Safety": 55, "Environment": 61}


def test_area_h_composite_matches_report():
    assert composite_score(AREA_H) == 71.0


def test_area_h_extremes():
    assert identify_extremes(AREA_H) == ("Education", "Transport")


def test_area_d_is_high_priority():
    assert composite_score(AREA_D) == 54.2
    assert is_high_priority(AREA_D)
    assert not is_high_priority(AREA_H)


def test_validate_score():
    assert validate_score("55") == 55.0
    assert validate_score("101") is None
    assert validate_score("-1") is None
    assert validate_score("abc") is None


def test_db_roundtrip():
    path = os.path.join(tempfile.mkdtemp(), "t.db")
    db.init_db(path)
    assert db.add_community("Area H", AREA_H, path)[0] == 71.0
    assert db.fetch_all(path)[0]["community_name"] == "Area H"


if __name__ == "__main__":  # run without pytest: python tests/test_scoring.py
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("PASS", name)
