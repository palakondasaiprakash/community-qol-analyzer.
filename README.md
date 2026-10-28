# Community Quality-of-Life Indicator Analyzer

Course End Project - **A9513 Python Programming Laboratory**
Department of CSE, Vardhaman College of Engineering, Hyderabad (2026-27)

**Team (Batch 20):** Mitali Sharma (26885A0562) · Spoorthi (26885A0563) · P. Saiprakash (26885A0564)
**Course Facilitator:** Mr. M. Raghavendra, Assistant Professor, CSE

## About
A menu-driven Python application that scores and compares municipal communities
across five indicators - **Healthcare, Education, Transport, Safety, Environment** -
each on a 0-100 scale, stored in a SQLite database.

- **QoLI** = arithmetic mean of the 5 indicators
- **Strongest / Weakest** indicator = argmax / argmin
- **High Priority for Intervention** if `QoLI < 65` **or** any indicator `< 50`
- Exports a ranked text audit report

## Project structure
```
community-qol-analyzer/
├── main.py                    # entry point
├── qol_analyzer/
│   ├── scoring.py             # validation + QoLI maths (pure functions)
│   ├── db.py                  # SQLite persistence
│   ├── report.py              # audit-report export
│   ├── plotting.py            # optional bar chart (matplotlib)
│   └── cli.py                 # terminal menu
├── data/sample_communities.csv
├── tests/test_scoring.py
├── docs/Project_Report.docx   # full project report (Word)
├── docs/Project_Report.pdf    # full project report (PDF)
├── reports/                   # generated audit files
├── requirements.txt
└── LICENSE
```

## Run it
Requires Python 3.8+ (no external packages).
```bash
python main.py                                      # interactive menu
python main.py --import data/sample_communities.csv # preload sample data
```
Menu: `[1]` Add · `[2]` View · `[3]` Scores · `[4]` Strongest/Weakest · `[5]` Ranking · `[6]` Export report · `[7]` Exit · `[8]` Plot chart (optional)

## Sample result (from the report)
| Area | Scores (H/E/T/S/Env) | QoLI | Status |
|------|----------------------|------|--------|
| H | 75 / 82 / 60 / 70 / 68 | **71.0** | OK - Education strongest, Transport weakest |
| D | 50 / 60 / 45 / 55 / 61 | **54.2** | High priority for intervention |

## Optional: score chart
```bash
pip install matplotlib
```
Then choose `[8]` in the menu to save a bar chart like the one in the report (`reports/Area_H_scores.png`).

## Tests
```bash
python tests/test_scoring.py      # no install needed
# or: pip install pytest && pytest
```

## SDG alignment
SDG 3 (Health) · SDG 4 (Education) · SDG 9 (Infrastructure) · SDG 11 (Sustainable Cities)

## Future work
GIS mapping (GeoPandas/Folium) and a REST API for crowdsourced data.

## License
MIT - see [LICENSE](LICENSE).
