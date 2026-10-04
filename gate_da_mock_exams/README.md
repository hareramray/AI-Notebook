# GATE DA — Programming, Data Structures & Algorithms: 50 Mock Tests

**[GATE_DA_PDSA_50_Mock_Tests.pdf](GATE_DA_PDSA_50_Mock_Tests.pdf)**: a 910-page book of 50 sectional mock tests for
Section 4 of the GATE Data Science & AI (DA) syllabus. The tests cover Python, stacks, queues, linked lists, trees,
hash tables, searching, elementary sorts, merge sort and quicksort, graph theory, traversals and shortest paths.

- **1000 questions** in the GATE pattern. Each test has 20 questions: Q1–10 are worth 1 mark and Q11–20 are worth 2 marks. Each test has roughly 8 MCQ, 5 MSQ and 7 NAT.
- **Three tiers:** Tests 01–15 are moderate and topic-focused. Tests 16–30 are GATE-level, deeper themes. Tests 31–45 are full-syllabus papers, and tests 46–50 are harder challenge papers.
- **Detailed solutions** for every question. Each one covers the concept, a step-by-step trace, an option-by-option analysis and the common trap.
- **Diagrams** of trees, heaps, graphs (weighted and directed), linked lists, hash tables, stacks, queues, arrays and trace tables.
- **Answers checked by code:** 997 of the 1000 answers are recomputed by a hidden `verify` program, by running the code shown, simulating the algorithm or brute force. The other 3 are conceptual questions with nothing to compute.
- **Front matter:** how to use the book, the exam pattern, the syllabus map and a quick-revision handbook. The back matter has the consolidated answer keys and a score tracker.

## Rebuilding

```bash
pip install reportlab networkx
python3 tools/validate.py sets/set_*.py     # schema + runs every verify block
python3 tools/build.py                      # writes GATE_DA_PDSA_50_Mock_Tests.pdf
```

Each test lives in `sets/set_NN.py`. To add or edit questions, see `tools/AUTHORING_GUIDE.md`, `tools/EXAMPLE_set.py`
and `tools/SET_PLAN.md`.
