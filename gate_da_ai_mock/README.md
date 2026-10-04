# GATE DA — Section 7 (AI): 100 Mock Tests

`GATE_DA_AI_Mock_Tests_100_Sets.pdf` holds 100 full mock tests for the AI section of the GATE Data Science & AI syllabus. Each test has 25 questions worth 40 marks, mixing MCQ, MSQ and NAT, and is followed by its answer key and step-by-step solutions. The book is 1,311 pages and also includes revision notes.

Syllabus covered: uninformed, informed and adversarial search; propositional and predicate logic; conditional independence; exact inference by variable elimination; approximate inference by sampling.

## Rebuild
```
pip install reportlab networkx pypdf
python3 build.py              # N_SETS=5 OUT=test.pdf python3 build.py for a quick build
```
- `gen_search.py`, `gen_games.py`, `gen_logic.py`, `gen_bn.py` generate questions with random parameters. Their answers and traces are computed exactly (search runs, minimax/alpha-beta, truth tables, resolution closure, BN enumeration, VE factor scopes, sampling).
- `banks/` holds about 260 hand-written concept questions with solutions.
- `draw.py` draws the vector diagrams; `notes.py` holds the revision notes; `build.py` assembles the PDF.
