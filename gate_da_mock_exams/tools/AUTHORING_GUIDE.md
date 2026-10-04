# Authoring guide — GATE DA Mock Test Series (Section 4: Programming, Data Structures & Algorithms)

Syllabus (GATE DA 2027, Section 4, verbatim): *Programming in Python, basic data structures: stacks,
queues, linked lists, trees, hash tables; Search algorithms: linear search and binary search, basic
sorting algorithms: selection sort, bubble sort and insertion sort; divide and conquer: mergesort,
quicksort; introduction to graph theory; basic graph algorithms: traversals and shortest path.*
(Heaps / priority queues, BSTs, asymptotic analysis and recurrences are fair game as they underpin
trees, sorting and Dijkstra.)

## Files
- Each set is a Python file `sets/set_NN.py` (NN = two digits) defining `SET = {...}`.
- Format reference with every feature: `tools/EXAMPLE_set.py` — READ IT FIRST.
- Diagram types and their keys: docstring at top of `tools/diagrams.py`.
- Validate: `cd gate_da_mock_exams && python3 tools/validate.py sets/set_NN.py --pdf /tmp/<you>/preview_NN.pdf`
  It checks schema, runs every `code` + `verify` block, renders all diagrams, and builds a preview.
  A set is DONE only when the validator prints no ERROR lines. Fix WARN lines about long code lines too.
  Look at the preview PDF pages (pdftoppm -png -r 60 ...) at least once per set to check diagrams look right.

## Set structure (mirror the real GATE DA paper)
- Exactly **20 questions**. **Q1–Q10 are 1-mark**, **Q11–Q20 are 2-mark** (total 30 marks).
- Type mix per set: about **8 MCQ, 5 MSQ, 7 NAT** (validator minimum 6/3/4). Spread types across both halves.
- MCQ: exactly one correct of 4 options. MSQ: one OR MORE correct of 4 (vary: sometimes 1, often 2–3,
  occasionally all 4). NAT: numeric answer; integers mostly; for non-integers say “rounded off to two
  decimal places” in the text and give answer as a range e.g. `["2.49", "2.51"]`.
- GATE phrasing: “Which of the following statements is/are TRUE?”, “The number of … is ______.”,
  “Consider the following Python program … The output is”.
- Topic spread in every set (it is a sectional test of the whole syllabus) — roughly:
  Python programming 5 · stacks/queues 2–3 · linked lists 1–2 · trees/BST/heaps 3 · hashing 1–2 ·
  searching 1–2 · elementary sorts 2 · merge/quick sort & recurrences 2 · graph theory + traversals +
  shortest paths 3–4 · (complexity can be folded into any of these). The set's **focus** theme should get
  extra weight (≈6–8 questions) while keeping the rest of the spread.

## Quality bar (this is the point of the book)
- GATE-level: questions must require tracing, reasoning or computation — not definitions recall.
  Use realistic GATE styles: program-output tracing, counting (number of swaps/comparisons/probes/
  BSTs/topological orders/stack permutations), statement-truth MSQs, algorithm-trace states,
  complexity of a code fragment, minimum/maximum possible values, “which sequence is possible”.
- 1-mark questions: one key insight, 1–3 minutes. 2-mark: multi-step, 3–5 minutes, may combine topics.
- Python code: Python 3, ≤ 25 lines usually, lines ≤ 72 chars, must actually run (no `input()`).
  Show realistic traps: aliasing, mutable defaults, integer division `//` and `%` with negatives,
  slicing with negative steps, `is` vs `==`, closures late binding, generator exhaustion, `global`/`nonlocal`,
  shallow vs deep copy, dict ordering, set operations, string immutability, recursion depth/returns,
  short-circuit evaluation, `sorted(key=...)` stability, list comprehension scoping, `*args/**kwargs`, `try/finally`.
- Use original numbers and code. Do NOT reuse the example set's questions. Avoid repeating the same
  question idea within your sets; vary data, structure and asked quantity.
- **Diagrams**: at least **6 questions per set** must include a diagram in `diagrams` or
  `solution_diagrams` (trees, graphs, linked lists, hash tables, arrays with pointers, stacks, DP/distance
  tables via `matrix`). Use solution diagrams to show traces (e.g. array state after each pass via
  `matrix`, BFS tree via `graph` with `highlight_edges`, final hash table, rotated/deleted tree).
  For graphs with ≥ 5 nodes give explicit `pos` coordinates for a clean layout (grid-ish, units ~1–2).
- **Solutions must be detailed and teach**: (a) the key concept in one or two sentences, (b) a full
  step-by-step trace/computation (use bullets or a `matrix` table), (c) for MCQ/MSQ an option-by-option
  verdict explaining why each wrong option is wrong, (d) a “Trap/Tip” line naming the common mistake.
  Aim ≥ 90 words for 1-mark and ≥ 150 words for 2-mark solutions. `solution_code` may hold a short
  reference implementation or a printed trace when that helps.
- **Correctness is mandatory**. Every question whose answer is computable must have a `verify`
  block (target ≥ 16 of 20 per set) that independently recomputes the answer with code and asserts
  against `ANSWER` (or against `OUTPUT` for program-output questions). For MCQ/MSQ verify the key option
  AND that the distractors are actually wrong where feasible. Run the validator; never “fix” a failing
  assert by editing the assert — fix the question/answer.
- Python program-output MCQs: compute the real output by running it (verify with `OUTPUT`), make
  distractors plausible mistakes.
- Avoid ambiguity: define height (edges vs nodes), indexing (0/1-based), tie-breaking order for
  BFS/DFS/Dijkstra (“neighbours are visited in alphabetical order”), what counts as a comparison/swap,
  and hash function/probing exactly.

## Markup reminders
`inline code`, **bold**, *italic*, x^{2}, a_{i}; newline = line break; blank line = paragraph;
lines beginning with "- " become bullets. Use unicode for math (Θ, ≤, ⌈ ⌉, log₂, n², ∞, →).
Do not use HTML tags or LaTeX `$...$`. Inside Python triple-quoted strings, escape backslashes properly.
