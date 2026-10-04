# GATE DA – Probability & Statistics Mock Test Series

**[GATE_DA_Probability_Statistics_Mock_Tests.pdf](GATE_DA_Probability_Statistics_Mock_Tests.pdf)**: 273 pages, 10 mock tests, 300 original questions.

The book covers Section 1 of the GATE DA syllabus (Probability and Statistics):

- **Part A: Formula handbook.** 14 sections, about 20 diagrams, and a list of high-frequency exam traps.
- **Part B: 10 mock tests.** Each test has 30 questions worth 48 marks: Q1–12 are 1-mark and Q13–30 are 2-mark, split into roughly 14 MCQ, 7 MSQ and 9 NAT. Every test comes with instructions, an answer key, a score tracker and a fully worked solution for each question. Each solution states the concept, shows every step, judges each MSQ option separately, and ends with a trap or shortcut note.
  - Tests 01–02: foundation level, whole syllabus
  - Tests 03–04: standard GATE level, set in data-science contexts
  - Tests 05–08: topic tests
    - 05: counting, Bayes and conditional expectation
    - 06: distributions, PDFs and CDFs
    - 07: CLT, confidence intervals and hypothesis tests
    - 08: descriptive statistics, covariance and correlation
  - Tests 09–10: advanced, multi-concept questions (10 is the grand mock)
- **Part C: Appendix.** Standard normal, t and χ² tables, an overall performance tracker and an error log.

Every numeric answer is computed in code inside its set file, so the key cannot drift from the maths. Each answer was also checked by a separate, independent re-solve.

## Rebuild

```bash
pip install reportlab matplotlib scipy numpy pypdf
python3 build.py                      # full book -> out/GATE_DA_Probability_Statistics_Mock_Tests.pdf
python3 render.py sets/set03.py       # validate and preview a single set
```

Questions live in `sets/setNN.py` as plain Python data. `sets/example_format.py` documents the format.
