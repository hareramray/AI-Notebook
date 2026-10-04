"""Front matter (cover, guide, syllabus, quick-revision handbook, contents) and back matter
(consolidated answer keys, score tracker) for the mock-test book."""
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (CondPageBreak, KeepTogether, NextPageTemplate, PageBreak, Paragraph,
                                Spacer, Table, TableStyle)

MAROON = colors.HexColor("#6b1d1d")
GOLD = colors.HexColor("#f2c14e")
SOFT = colors.HexColor("#f3f4f6")
GRIDC = colors.HexColor("#d1d5db")


def _tbl(rows, widths, ST, header=True, zebra=True, font=8.6):
    cs = ParagraphStyle("c", parent=ST["cell"], fontSize=font, leading=font * 1.3)
    hs = ParagraphStyle("h", parent=ST["cellb"], fontSize=font, leading=font * 1.3)
    from build import md
    data = []
    for r, row in enumerate(rows):
        data.append([Paragraph(md(str(c)), hs if (header and r == 0) else cs) for c in row])
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    st = [("GRID", (0, 0), (-1, -1), 0.4, GRIDC), ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5)]
    if header:
        st.append(("BACKGROUND", (0, 0), (-1, 0), MAROON))
    if zebra:
        for r in range(1 if header else 0, len(rows)):
            if r % 2 == 0:
                st.append(("BACKGROUND", (0, r), (-1, r), SOFT))
    t.setStyle(TableStyle(st))
    return t


def cover(ST, sets):
    W = 210 * mm
    big = ParagraphStyle("cv1", fontName="DejaVuSerif-Bold", fontSize=27, leading=34, textColor=colors.white,
                         alignment=TA_CENTER)
    mid = ParagraphStyle("cv2", fontName="DejaVuSans-Bold", fontSize=16, leading=22, textColor=GOLD,
                         alignment=TA_CENTER)
    sm = ParagraphStyle("cv3", fontName="DejaVuSans", fontSize=11.5, leading=17, textColor=colors.white,
                        alignment=TA_CENTER)
    nq = sum(len(s["questions"]) for s in sets)
    return [
        Spacer(1, 52 * mm),
        Paragraph("GATE DA", ParagraphStyle("cv0", parent=mid, fontSize=20, leading=26)),
        Spacer(1, 6),
        Paragraph("Programming, Data Structures<br/>&amp; Algorithms", big),
        Spacer(1, 14),
        Paragraph("%d FULL MOCK TESTS · %d QUESTIONS · DETAILED SOLUTIONS" % (len(sets), nq), mid),
        Spacer(1, 22),
        Paragraph("Data Science and Artificial Intelligence (DA) — Section 4 Sectional Test Series<br/>"
                  "Python · Stacks · Queues · Linked Lists · Trees · Hash Tables<br/>"
                  "Linear &amp; Binary Search · Selection / Bubble / Insertion Sort<br/>"
                  "Merge Sort · Quicksort · Graph Theory · Traversals · Shortest Paths", sm),
        Spacer(1, 26),
        Paragraph("MCQ · MSQ · NAT in the exact GATE pattern — 1-mark and 2-mark questions<br/>"
                  "Every answer machine-verified · Diagrams for trees, graphs, lists and hash tables<br/>"
                  "Answer keys · Step-by-step solutions · Traps &amp; tips · Quick-revision handbook", sm),
        Spacer(1, 40 * mm),
        Paragraph("Aligned to the GATE 2027 DA syllabus (Section 4)", ParagraphStyle("cv4", parent=sm, fontSize=9.5,
                                                                                      textColor=GOLD)),
    ]


def front_matter(ST, H2TOC, sets, md, paras, CodeBlock, RunningMark, TableOfContents):
    S = []
    S += cover(ST, sets)
    S += [NextPageTemplate("normal"), PageBreak(), RunningMark("Contents")]
    S.append(Paragraph("Contents", ParagraphStyle("ct", parent=ST["h2"], fontSize=20, leading=24)))
    toc = TableOfContents()
    toc.levelStyles = [ParagraphStyle("t0", fontName="DejaVuSans-Bold", fontSize=9.5, leading=12.5,
                                      leftIndent=0, firstLineIndent=0, spaceBefore=2),
                       ParagraphStyle("t1", fontName="DejaVuSans", fontSize=8.6, leading=11,
                                      leftIndent=16, firstLineIndent=0)]
    toc.dotsMinLevel = 0
    S.append(toc)

    # ---------------------------------------------------------- how to use
    S += [PageBreak(), RunningMark("About this book"), Paragraph("How to Use This Book", ST["h1"])]
    S += paras(
        "This book is a complete sectional test series for **Section 4 — Programming, Data Structures and "
        "Algorithms** of the GATE Data Science and Artificial Intelligence (DA) paper. It contains **%d mock tests "
        "of 20 questions each**, built to the pattern, difficulty and question styles of the real GATE DA paper, "
        "followed by an answer key and fully worked solutions for every test.\n\n"
        "The tests are graded in three tiers:\n\n"
        "- **Tests 01–15 (Moderate):** one focus topic per test — ideal while you are still revising a topic. "
        "The rest of each paper still spans the whole section so that you keep earlier topics warm.\n"
        "- **Tests 16–30 (GATE-level):** deeper themes — recursion, generators, closures, complexity, counting "
        "trees, topological orders, hashing analysis, sorting properties, binary-search variants, weighted shortest paths.\n"
        "- **Tests 31–45 (Full-syllabus GATE-level papers)** and **Tests 46–50 (Challenge papers):** balanced, "
        "timed papers exactly like the section you will face in the exam; the challenge papers are deliberately "
        "harder and trap-heavy.\n\n"
        "**Recommended routine.** Sit each test in one go with a timer (54 minutes for 30 marks, the GATE rate of "
        "about 1.8 minutes per mark). Use only rough paper — no IDE. Mark answers on the response grid, score yourself "
        "with the answer key using the GATE marking scheme, and only then read the solutions. Every solution "
        "explains the concept, traces the computation step by step, analyses every option and names the common trap. "
        "Log your score in the tracker at the end of the book and revisit every question you got wrong after a week.\n\n"
        "**Conventions used throughout.** Programs are Python 3. Unless a question says otherwise: arrays/lists are "
        "0-indexed; the *height* of a tree is the number of edges on the longest root-to-leaf path (a single node has "
        "height 0); log means log₂; adjacency lists are explored in the order stated in the question (usually "
        "alphabetical or increasing numerical order); a *comparison* means a key comparison between two array elements."
        % len(sets))

    S += [Paragraph("Exam pattern and marking scheme", ST["h3"])]
    S.append(_tbl([
        ["Question type", "What you do", "Marks", "Negative marking"],
        ["MCQ — Multiple Choice", "Choose the single correct option out of four", "1 or 2",
         "−1/3 for a wrong 1-mark answer, −2/3 for a wrong 2-mark answer"],
        ["MSQ — Multiple Select", "Choose ALL correct options (one or more of four)", "1 or 2",
         "None. No partial credit: you must select exactly the correct set"],
        ["NAT — Numerical Answer", "Type a number using the virtual keypad", "1 or 2",
         "None. Answers given as a range accept any value in the range"],
    ], [92, 150, 40, None], ST))
    S.append(Spacer(1, 6))
    S += paras(
        "The actual GATE DA paper has 65 questions for 100 marks in 180 minutes (General Aptitude: 15 marks; "
        "subject: 85 marks), so roughly one in seven to one in five subject questions comes from this section. "
        "Each mock test here is a 30-mark sectional slice: **Q1–Q10 carry 1 mark** and **Q11–Q20 carry 2 marks**.")

    S += [Paragraph("Score interpretation (per 30-mark test)", ST["h3"])]
    S.append(_tbl([
        ["Score", "Reading", "What to do next"],
        ["24 – 30", "Exam-ready on this material", "Move to the next tier; time yourself more strictly"],
        ["18 – 23.9", "Strong, but leaking marks", "Re-read the traps for every miss; redo after a week"],
        ["12 – 17.9", "Concepts present, execution shaky", "Revise the handbook pages for the weak topics, then retest"],
        ["below 12", "Foundation gap", "Study the topic first; attempt the Moderate tier tests on it"],
    ], [60, 150, None], ST))

    # ---------------------------------------------------------- syllabus
    S += [PageBreak(), RunningMark("Syllabus"), Paragraph("Syllabus and Topic Map", ST["h1"])]
    S += paras("**GATE 2027 DA — Section 4: Programming, Data Structures and Algorithms** (official text):\n\n"
               "*Programming in Python, basic data structures: stacks, queues, linked lists, trees, hash tables; "
               "Search algorithms: linear search and binary search, basic sorting algorithms: selection sort, bubble sort "
               "and insertion sort; divide and conquer: mergesort, quicksort; introduction to graph theory; basic graph "
               "algorithms: traversals and shortest path.*")
    S += [Paragraph("What is examined under each syllabus item", ST["h3"])]
    S.append(_tbl([
        ["Syllabus item", "Sub-topics covered in these tests"],
        ["Programming in Python", "Data types, integer vs float division, `//` and `%` with negatives, strings and "
         "slicing, lists/tuples/dicts/sets, mutability and aliasing, shallow vs deep copy, functions, default arguments, "
         "`*args/**kwargs`, scope (LEGB), `global`/`nonlocal`, closures and late binding, recursion, comprehensions, "
         "generators and iterators, lambda/map/filter/zip/sorted, classes and objects, exceptions and `finally`."],
        ["Stacks", "Push/pop traces, infix→postfix/prefix, postfix evaluation, balanced brackets, stack permutations "
         "(Catalan numbers), recursion as a stack, monotonic stacks, two stacks in one array."],
        ["Queues", "Linear and circular queues (front/rear arithmetic, full/empty tests), deques, queue using two stacks "
         "(amortised cost), stack using queues, priority queues."],
        ["Linked lists", "Singly, doubly and circular lists; insertion/deletion/reversal; cycle detection; middle "
         "element; merging; costs of operations with and without tail pointers."],
        ["Trees", "Binary trees, traversals and reconstruction, height/size bounds, full/complete/perfect trees, BSTs "
         "(search/insert/delete, valid search sequences), number of BSTs/binary trees, binary heaps and heap operations."],
        ["Hash tables", "Division/multiplication hashing, chaining, linear/quadratic probing, double hashing, deletion "
         "with tombstones, load factor and expected probe counts, clustering, collision probabilities."],
        ["Searching", "Linear search (with/without sentinel, expected comparisons), binary search traces, lower/upper "
         "bounds, number of comparisons, searching rotated arrays, binary search on the answer."],
        ["Elementary sorting", "Selection, bubble (with early exit), insertion sort: passes, swaps, comparisons, "
         "inversions, best/worst cases, stability, in-place property, adaptivity."],
        ["Divide and conquer", "Merge sort (merge comparisons, recursion tree, space), quicksort (Lomuto/Hoare "
         "partition, pivot effects, worst/best cases), recurrences and the master theorem, D&C applications."],
        ["Graph theory", "Degree sequences, handshaking lemma, simple/complete/bipartite graphs, trees and forests, "
         "connectivity and components, cycles, representations (matrix/list) and their costs."],
        ["Graph algorithms", "BFS and DFS orders, BFS levels and shortest hops, DFS trees, discovery/finish times, "
         "edge classification, topological sort, connected components, Dijkstra, Bellman–Ford, shortest-path trees."],
    ], [100, None], ST))

    # topic-question map
    S += [CondPageBreak(200), Paragraph("Test-by-test focus", ST["h3"])]
    rows = [["Test", "Title", "Difficulty", "Focus"]]
    for s in sets:
        rows.append(["%02d" % s["number"], s["title"], s.get("difficulty", ""), s.get("focus", "")])
    S.append(_tbl(rows, [30, 150, 62, None], ST, font=8))

    # ---------------------------------------------------------- handbook
    S += handbook(ST, md, paras, CodeBlock, RunningMark)
    return S


def handbook(ST, md, paras, CodeBlock, RunningMark):
    S = [PageBreak(), RunningMark("Quick-revision handbook"), Paragraph("Quick-Revision Handbook", ST["h1"])]
    S += paras("A compact reference of the facts, formulas and Python behaviours that the questions in this book "
               "test most often. Read it before each test tier, and come back to it whenever a solution names a trap.")

    S += [Paragraph("1. Python behaviours that GATE loves to test", ST["h3"])]
    S.append(_tbl([
        ["Behaviour", "Example", "Result / rule"],
        ["Floor division & modulo", "`-7 // 2`, `-7 % 2`, `7 % -3`", "`-4`, `1`, `-2` — `//` floors toward −∞; `a % b` has the sign of b; `a == (a//b)*b + a%b`"],
        ["True division", "`7 / 2`, `4 / 2`", "`3.5`, `2.0` (always float)"],
        ["Slicing", "`s[::-1]`, `s[1:-1]`, `s[5:1:-2]`", "Slices never raise IndexError; stop is exclusive; negative step walks backwards"],
        ["Aliasing", "`b = a; b.append(1)`", "`a` changes too — same object. `a[:]`, `list(a)`, `copy.copy(a)` make shallow copies"],
        ["Shallow copy of nested", "`m = [[0]*3]*3; m[0][0] = 1`", "All three rows change: the inner list is repeated by reference"],
        ["Mutable default", "`def f(x, L=[])`", "Default created once at `def` time and shared across calls"],
        ["`is` vs `==`", "`[1] == [1]`, `[1] is [1]`", "`True`, `False` — identity vs equality"],
        ["Closures (late binding)", "`fs = [lambda: i for i in range(3)]`", "Every `f()` returns 2 — `i` is looked up when called. Fix: `lambda i=i: i`"],
        ["Scope", "assigning to a name inside a function", "makes it local for the whole function → `UnboundLocalError` if read first; use `global`/`nonlocal`"],
        ["Generators", "`g = (x*x for x in range(3))`", "Single pass: `list(g)` twice gives `[0, 1, 4]` then `[]`"],
        ["Short-circuit", "`0 or [] or 'a'`, `1 and 0 and 2`", "`'a'`, `0` — returns the deciding operand, not a bool"],
        ["Strings immutable", "`s[0] = 'x'`", "`TypeError`; `s.replace` returns a new string"],
        ["Dict order", "`{'b':1,'a':2}`", "Insertion order preserved (Python 3.7+); keys must be hashable"],
        ["`sorted` stability", "`sorted(L, key=len)`", "Stable: equal keys keep their original relative order"],
        ["`try/finally`", "`return` inside `try` and `finally`", "`finally` always runs; a `return` in `finally` overrides the earlier one"],
        ["Chained comparison", "`1 < 3 > 2`", "`True` — means `1 < 3 and 3 > 2`"],
        ["Integer size", "`2**100`", "Exact — Python ints are unbounded"],
    ], [92, 120, None], ST, font=8.2))

    S += [CondPageBreak(160), Paragraph("2. Complexity cheat-sheet", ST["h3"])]
    S.append(_tbl([
        ["Structure / operation", "Average", "Worst", "Notes"],
        ["Python list: index, append", "O(1)", "O(1) amortised", "`insert(0,x)`, `pop(0)`, `x in L` are O(n)"],
        ["dict / set: lookup, insert", "O(1)", "O(n)", "Hash-based; worst case under pathological collisions"],
        ["Stack push/pop (array or list)", "O(1)", "O(1)", ""],
        ["Queue via two stacks", "O(1) amortised", "O(n) for one dequeue", "Each element moved at most twice"],
        ["Linked list: insert at head", "O(1)", "O(1)", "Insert at tail O(1) only with a tail pointer"],
        ["Linked list: search / k-th", "O(n)", "O(n)", "Delete a given node in a singly list needs its predecessor"],
        ["BST search/insert/delete", "O(log n)", "O(n)", "Height h ⇒ O(h)"],
        ["Binary heap insert / extract", "O(log n)", "O(log n)", "find-min O(1); build-heap O(n)"],
        ["Hash table (chaining) search", "O(1 + α)", "O(n)", "α = n/m load factor"],
        ["Linear search", "O(n)", "O(n)", "Expected (n+1)/2 comparisons for a successful uniform search"],
        ["Binary search", "O(log n)", "O(log n)", "At most ⌊log₂ n⌋ + 1 probes"],
        ["Graph BFS / DFS", "O(V + E)", "O(V + E)", "O(V²) with an adjacency matrix"],
        ["Dijkstra (binary heap)", "O((V + E) log V)", "", "O(V²) with an array; fails with negative edges"],
        ["Bellman–Ford", "O(VE)", "", "V−1 rounds; detects negative cycles"],
        ["Floyd–Warshall", "O(V³)", "", "All pairs"],
    ], [130, 72, 80, None], ST, font=8.2))

    S += [CondPageBreak(200), Paragraph("3. Sorting at a glance", ST["h3"])]
    S.append(_tbl([
        ["Algorithm", "Best", "Average", "Worst", "Swaps (worst)", "Stable", "In-place", "Adaptive"],
        ["Selection sort", "Θ(n²)", "Θ(n²)", "Θ(n²)", "n − 1", "No*", "Yes", "No"],
        ["Bubble sort (early exit)", "Θ(n)", "Θ(n²)", "Θ(n²)", "n(n−1)/2", "Yes", "Yes", "Yes"],
        ["Insertion sort", "Θ(n)", "Θ(n²)", "Θ(n²)", "n(n−1)/2 shifts", "Yes", "Yes", "Yes"],
        ["Merge sort", "Θ(n log n)", "Θ(n log n)", "Θ(n log n)", "—", "Yes", "No (Θ(n) extra)", "No"],
        ["Quicksort", "Θ(n log n)", "Θ(n log n)", "Θ(n²)", "—", "No", "Yes (stack O(log n)–O(n))", "No"],
        ["Heapsort", "Θ(n log n)", "Θ(n log n)", "Θ(n log n)", "—", "No", "Yes", "No"],
    ], [82, 46, 50, 46, 60, 34, 76, None], ST, font=7.8))
    S += paras(
        "*Selection sort with swapping is unstable; a shifting variant can be made stable.\n\n"
        "- **Inversions:** a pair (i, j) with i < j and A[i] > A[j]. Bubble sort performs exactly one swap per inversion; "
        "insertion sort performs exactly one shift per inversion and at most (n−1) + #inversions comparisons. "
        "Maximum inversions = n(n−1)/2 (reverse order); expected for a random permutation = n(n−1)/4.\n"
        "- **Merging** two sorted lists of sizes m and n takes between min(m, n) and m + n − 1 comparisons.\n"
        "- **Comparison sorting lower bound:** any comparison sort needs ⌈log₂ n!⌉ comparisons in the worst case "
        "= Ω(n log n).\n"
        "- **Quicksort worst case** happens when the pivot is always the minimum or maximum (e.g. sorted input with "
        "first/last-element pivot): T(n) = T(n−1) + Θ(n) = Θ(n²), with n(n−1)/2 comparisons.\n"
        "- **Lomuto partition** (pivot = last): `i = lo−1; for j in lo..hi−1: if A[j] ≤ pivot: i += 1, swap A[i], A[j]`; "
        "finally swap A[i+1], A[hi].  **Hoare partition** uses two inward-moving indices and returns a split point, "
        "not the pivot's final position.", "body")

    S += [CondPageBreak(200), Paragraph("4. Recurrences and the master theorem", ST["h3"])]
    S += paras("For T(n) = a·T(n/b) + f(n), compare f(n) with n^{log_b a}:\n\n"
               "- f(n) = O(n^{log_b a − ε}) ⇒ T(n) = Θ(n^{log_b a}).\n"
               "- f(n) = Θ(n^{log_b a} log^{k} n) ⇒ T(n) = Θ(n^{log_b a} log^{k+1} n).\n"
               "- f(n) = Ω(n^{log_b a + ε}) and regularity ⇒ T(n) = Θ(f(n)).")
    S.append(_tbl([
        ["Recurrence", "Solution", "Where it appears"],
        ["T(n) = T(n/2) + 1", "Θ(log n)", "Binary search"],
        ["T(n) = 2T(n/2) + n", "Θ(n log n)", "Merge sort, balanced quicksort"],
        ["T(n) = T(n−1) + n", "Θ(n²)", "Worst-case quicksort, selection sort"],
        ["T(n) = T(n−1) + 1", "Θ(n)", "Linear recursion, list length"],
        ["T(n) = 2T(n−1) + 1", "Θ(2ⁿ)", "Towers of Hanoi (2ⁿ − 1 moves)"],
        ["T(n) = 2T(n/2) + 1", "Θ(n)", "Tree traversal, max by D&C"],
        ["T(n) = T(n/2) + n", "Θ(n)", "Selection by halving"],
        ["T(n) = 7T(n/2) + n²", "Θ(n^{log₂7})", "Strassen"],
        ["T(n) = T(n−1) + T(n−2) + 1", "Θ(φⁿ)", "Naive Fibonacci; calls = 2F(n+1) − 1"],
    ], [130, 90, None], ST, font=8.4))

    S += [CondPageBreak(200), Paragraph("5. Trees — formulas worth memorising", ST["h3"])]
    S += paras(
        "- A binary tree of height h has at most 2^{h+1} − 1 nodes and at least h + 1 nodes; a binary tree with n "
        "nodes has height between ⌊log₂ n⌋ and n − 1.\n"
        "- In any non-empty binary tree, n₀ = n₂ + 1 (leaves = nodes with two children + 1). A full (strict) binary "
        "tree with i internal nodes has i + 1 leaves and 2i + 1 nodes.\n"
        "- Number of structurally different binary trees (and of BSTs on n distinct keys) is the Catalan number "
        "Cₙ = (2n)! / ((n+1)! n!): 1, 1, 2, 5, 14, 42, 132, 429, 1430 for n = 0..8. Cₙ also counts valid stack "
        "permutations of 1..n and balanced bracket strings with n pairs.\n"
        "- Number of labelled binary trees with n nodes = n!·Cₙ. Number of BSTs of height n−1 on n keys = 2^{n−1}.\n"
        "- Pre-order + in-order (or post-order + in-order) determine a binary tree uniquely; pre-order + post-order "
        "do not (unless the tree is full).\n"
        "- Heap stored in an array (0-indexed): children of i are 2i+1 and 2i+2, parent is ⌊(i−1)/2⌋. Leaves are "
        "indices ⌊n/2⌋ .. n−1. Build-heap is O(n); the k-th smallest element of a min-heap lies at depth < k.\n"
        "- BST in-order traversal is sorted. Deleting a node with two children replaces it by its in-order successor "
        "(minimum of right subtree) or predecessor (maximum of left subtree).")

    S += [CondPageBreak(160), Paragraph("6. Hashing formulas", ST["h3"])]
    S += paras(
        "- Load factor α = n / m. Chaining: expected unsuccessful search 1 + α probes (Θ(1 + α)); successful "
        "≈ 1 + α/2.\n"
        "- Open addressing, uniform hashing: expected probes for unsuccessful search ≤ 1/(1 − α); successful "
        "≤ (1/α)·ln(1/(1 − α)).\n"
        "- Linear probing (Knuth): unsuccessful ≈ ½(1 + 1/(1 − α)²), successful ≈ ½(1 + 1/(1 − α)).\n"
        "- Probe sequences: linear h(k) + i, quadratic h(k) + c₁i + c₂i², double hashing h₁(k) + i·h₂(k) (all mod m). "
        "Quadratic probing may fail to find a free slot even when one exists; double hashing needs h₂(k) ≠ 0 and "
        "coprime with m to visit every slot.\n"
        "- With n keys hashed uniformly into m slots, expected number of colliding pairs = C(n, 2)/m; probability "
        "that all n go to distinct slots = m(m−1)…(m−n+1)/mⁿ; expected empty slots = m(1 − 1/m)ⁿ.\n"
        "- Deletion in open addressing must leave a tombstone (DELETED marker); otherwise later searches stop early.")

    S += [CondPageBreak(160), Paragraph("7. Graph facts", ST["h3"])]
    S += paras(
        "- Handshaking lemma: Σ deg(v) = 2|E|; the number of odd-degree vertices is even. In a digraph "
        "Σ in-deg = Σ out-deg = |E|.\n"
        "- Simple undirected graph on n vertices has at most n(n−1)/2 edges; number of labelled simple graphs is "
        "2^{n(n−1)/2}. K_{m,n} has mn edges; Kₙ has n(n−1)/2.\n"
        "- A tree on n vertices has n − 1 edges; a forest with k components has n − k edges. Number of labelled "
        "trees on n vertices = n^{n−2} (Cayley).\n"
        "- A graph is bipartite ⇔ it has no odd cycle ⇔ BFS 2-colouring never finds an edge inside one level.\n"
        "- A graph with n vertices and k components has at least n − k edges; with more than (n−1)(n−2)/2 edges "
        "a simple graph must be connected.\n"
        "- BFS from s gives shortest hop counts; edges of an undirected graph go between the same or adjacent "
        "BFS levels. DFS in an undirected graph has only tree and back edges; in a digraph, tree/back/forward/cross, "
        "and a back edge exists ⇔ there is a cycle.\n"
        "- Topological order exists ⇔ the digraph is acyclic; reverse post-order of DFS is a topological order.\n"
        "- (A^{k})[i][j] = number of walks of length k from i to j in the adjacency matrix A.\n"
        "- Dijkstra requires non-negative weights; each vertex is finalised once, in non-decreasing order of "
        "distance. Bellman–Ford relaxes all edges V − 1 times; an improvement in round V signals a negative cycle.")

    S += [CondPageBreak(230), Paragraph("8. Reference implementations", ST["h3"])]
    S.append(CodeBlock('''def binary_search(A, x):            # first index with A[i] >= x
    lo, hi = 0, len(A)
    while lo < hi:
        mid = (lo + hi) // 2
        if A[mid] < x: lo = mid + 1
        else:          hi = mid
    return lo

def insertion_sort(A):
    for i in range(1, len(A)):
        key, j = A[i], i - 1
        while j >= 0 and A[j] > key:
            A[j + 1] = A[j]; j -= 1
        A[j + 1] = key

def merge(L, R):
    out, i, j = [], 0, 0
    while i < len(L) and j < len(R):
        if L[i] <= R[j]: out.append(L[i]); i += 1
        else:            out.append(R[j]); j += 1
    return out + L[i:] + R[j:]

def lomuto(A, lo, hi):
    p, i = A[hi], lo - 1
    for j in range(lo, hi):
        if A[j] <= p:
            i += 1; A[i], A[j] = A[j], A[i]
    A[i + 1], A[hi] = A[hi], A[i + 1]
    return i + 1''', "Searching and sorting"))
    S.append(Spacer(1, 6))
    S.append(CodeBlock('''from collections import deque
import heapq

def bfs(G, s):
    dist, q = {s: 0}, deque([s])
    while q:
        u = q.popleft()
        for v in G[u]:
            if v not in dist:
                dist[v] = dist[u] + 1; q.append(v)
    return dist

def dfs(G, u, seen, order):
    seen.add(u); order.append(u)
    for v in G[u]:
        if v not in seen: dfs(G, v, seen, order)

def dijkstra(G, s):                 # G[u] = [(v, w), ...], w >= 0
    d, pq = {s: 0}, [(0, s)]
    while pq:
        du, u = heapq.heappop(pq)
        if du > d[u]: continue
        for v, w in G[u]:
            if du + w < d.get(v, float('inf')):
                d[v] = du + w; heapq.heappush(pq, (d[v], v))
    return d''', "Graph algorithms"))
    return S


def back_matter(ST, H2TOC, sets, RunningMark, fmt_answer):
    S = [NextPageTemplate("normal"), PageBreak(), RunningMark("Consolidated answer keys"),
         Paragraph("Consolidated Answer Keys", ST["h1"])]
    from build import esc
    from reportlab.platypus import Paragraph as P
    cs = ParagraphStyle("ak", parent=ST["cell"], fontSize=7.4, leading=9.2, alignment=TA_CENTER)
    hs = ParagraphStyle("akh", parent=ST["cellb"], fontSize=7.4, leading=9.2, alignment=TA_CENTER)
    for chunk_start in range(0, len(sets), 10):
        chunk = sets[chunk_start:chunk_start + 10]
        header = [P("Q", hs)] + [P("T%02d" % s["number"], hs) for s in chunk]
        rows = [header]
        for qi in range(20):
            row = [P(str(qi + 1), hs)]
            for s in chunk:
                q = s["questions"][qi]
                row.append(P(esc(fmt_answer(q)).replace(", ", ","), cs))
            rows.append(row)
        t = Table(rows, colWidths=[26] + [None] * len(chunk), repeatRows=1)
        st = [("GRID", (0, 0), (-1, -1), 0.4, GRIDC), ("BACKGROUND", (0, 0), (-1, 0), MAROON),
              ("BACKGROUND", (0, 0), (0, -1), MAROON), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
              ("TOPPADDING", (0, 0), (-1, -1), 1.6), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.6),
              ("LEFTPADDING", (0, 0), (-1, -1), 2), ("RIGHTPADDING", (0, 0), (-1, -1), 2),
              ("LINEBELOW", (0, 10), (-1, 10), 1.2, MAROON)]
        for r in range(1, 21):
            if r % 2 == 0:
                st.append(("BACKGROUND", (1, r), (-1, r), SOFT))
        t.setStyle(TableStyle(st))
        S += [KeepTogether([Paragraph("Tests %02d – %02d" % (chunk[0]["number"], chunk[-1]["number"]), ST["h3"]), t]),
              Spacer(1, 8)]
    S += [Paragraph("Rows 1–10 are 1-mark questions and rows 11–20 are 2-mark questions. For NAT answers "
                    "given as a range, any value within the range is correct.", ST["small"])]

    S += [PageBreak(), RunningMark("Score tracker"), Paragraph("Score Tracker", ST["h1"])]
    rows = [["Test", "Date", "Time taken", "Attempted", "Correct", "Wrong MCQs", "Score/30", "Weak topics"]]
    for s in sets:
        rows.append(["%02d" % s["number"], "", "", "", "", "", "", ""])
    t = Table(rows, colWidths=[30, 52, 52, 50, 44, 54, 50, None], repeatRows=1, rowHeights=[16] + [13.2] * len(sets))
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, GRIDC), ("BACKGROUND", (0, 0), (-1, 0), MAROON),
                           ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("FONT", (0, 0), (-1, 0), "DejaVuSans-Bold", 7.6),
                           ("FONT", (0, 1), (-1, -1), "DejaVuSans", 7.6), ("ALIGN", (0, 0), (-2, -1), "CENTER"),
                           ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    S.append(t)
    return S
