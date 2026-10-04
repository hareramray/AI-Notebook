# Set 32 — Full-Syllabus Mock — Paper 2
SET = {
    "number": 32,
    "title": "Full-Syllabus Mock — Paper 2",
    "difficulty": "GATE-level",
    "focus": "balanced paper across the whole Section 4 syllabus",
    "questions": [
        # ------------------------------------------------------------------ Q1
        {
            "type": "MCQ", "marks": 1, "topic": "Python — augmented assignment on a tuple element",
            "text": "Consider the following Python program. What is printed?",
            "code": '''t = ([1], 2)
try:
    t[0] += [3]
except TypeError:
    print("E", end=" ")
print(t)''',
            "options": ["`([1, 3], 2)`", "`E ([1], 2)`", "`E ([1, 3], 2)`", "`([1], 2, 3)`"],
            "answer": "C",
            "solution": (
                "**Concept:** `x[i] += y` is executed as two steps: (1) `tmp = x[i].__iadd__(y)` and "
                "(2) `x[i] = tmp`. For a list, step 1 extends the list **in place**. Step 2 then tries to "
                "assign into the tuple, which is immutable, and raises `TypeError`.\n\n"
                "- Step 1 succeeds: the list inside the tuple becomes `[1, 3]`.\n"
                "- Step 2 fails: `'tuple' object does not support item assignment` → the `except` block "
                "prints `E ` (with `end=\" \"`, no newline).\n"
                "- The tuple still holds the *same* list object, now mutated → `print(t)` shows "
                "`([1, 3], 2)`.\n\n"
                "Output: `E ([1, 3], 2)`.\n\n"
                "**Options:**\n"
                "- (A) assumes no exception is raised.\n"
                "- (B) assumes the failed statement is rolled back — Python has no such rollback; the "
                "in-place extension already happened.\n"
                "- (D) confuses `t[0] += [3]` with tuple concatenation.\n\n"
                "**Trap:** 'immutable tuple' means its *references* cannot change, not that the objects it "
                "refers to cannot be mutated. `t[0].append(3)` would succeed silently."
            ),
            "verify": "assert OUTPUT.strip() == 'E ([1, 3], 2)' and ANSWER == 'C'",
        },
        # ------------------------------------------------------------------ Q2
        {
            "type": "NAT", "marks": 1, "topic": "Queues — round-robin simulation",
            "text": ("Five jobs are scheduled round-robin with time quantum 3 using a FIFO ready queue. "
                     "P1, P2, P3, P4 (bursts 5, 3, 8, 2) are in the queue at time 0 in that order; P5 "
                     "(burst 4) arrives at time 4. A job whose quantum expires is put at the rear of the "
                     "queue, after any jobs that arrived while it was running. Context switches take no "
                     "time. The turnaround time (completion time − arrival time) of P5 is ______."),
            "answer": "16",
            "solution": (
                "**Concept:** round-robin is a queue simulation: dequeue the front job, run it for "
                "min(quantum, remaining), enqueue new arrivals, then re-enqueue the job if unfinished.\n\n"
                "Timeline (queue after each slice, front first):\n"
                "- 0–3 P1 (rem 2) → [P2, P3, P4, P1]\n"
                "- 3–6 P2 done at 6; P5 arrived at 4 → [P3, P4, P1, P5]\n"
                "- 6–9 P3 (rem 5) → [P4, P1, P5, P3]\n"
                "- 9–11 P4 done at 11 → [P1, P5, P3]\n"
                "- 11–13 P1 done at 13 → [P5, P3]\n"
                "- 13–16 P5 (rem 1) → [P3, P5]\n"
                "- 16–19 P3 (rem 2) → [P5, P3]\n"
                "- 19–20 P5 **done at 20** → [P3]\n"
                "- 20–22 P3 done at 22\n\n"
                "Turnaround of P5 = 20 − 4 = **16**.\n\n"
                "**Trap:** reporting the completion time (20) instead of the turnaround time, or "
                "enqueuing P5 at time 0."
            ),
            "solution_diagrams": [{"type": "queue", "values": ["P3", "P4", "P1", "P5"],
                                   "caption": "Ready queue at time 6 (front on the left)"}],
            "verify": '''
from collections import deque
procs = [('P1',0,5),('P2',0,3),('P3',0,8),('P4',0,2),('P5',4,4)]
rem = {p: b for p, a, b in procs}; arr = {p: a for p, a, b in procs}
time, Q, done = 0, deque(['P1','P2','P3','P4']), {}
pending = ['P5']
while Q:
    p = Q.popleft(); r = min(3, rem[p]); time += r; rem[p] -= r
    for x in list(pending):
        if arr[x] <= time:
            Q.append(x); pending.remove(x)
    if rem[p]: Q.append(p)
    else: done[p] = time
assert done['P5'] - 4 == int(ANSWER)
''',
        },
        # ------------------------------------------------------------------ Q3
        {
            "type": "MCQ", "marks": 1, "topic": "Linked lists — recursive pairwise swap",
            "text": "Consider the following Python program. What is printed?",
            "code": '''class N:
    def __init__(s, v, nx=None):
        s.v, s.nx = v, nx

def build(xs):
    h = None
    for x in reversed(xs):
        h = N(x, h)
    return h

def swap_pairs(h):
    if h is None or h.nx is None:
        return h
    second = h.nx
    h.nx = swap_pairs(second.nx)
    second.nx = h
    return second

h = build([1, 2, 3, 4, 5, 6, 7])
h.nx = swap_pairs(h.nx)
out = []
while h:
    out.append(h.v)
    h = h.nx
print(out)''',
            "options": [
                "`[2, 1, 4, 3, 6, 5, 7]`",
                "`[1, 3, 2, 5, 4, 7, 6]`",
                "`[1, 2, 4, 3, 6, 5, 7]`",
                "`[7, 6, 5, 4, 3, 2, 1]`",
            ],
            "answer": "B",
            "solution": (
                "**Concept:** `build` inserts at the head while iterating over the *reversed* input, so the "
                "list keeps the original order 1 → 2 → … → 7. `swap_pairs` swaps nodes in adjacent pairs and "
                "returns the new head; an odd node at the end stays put.\n\n"
                "Here the swap starts at the **second** node (`h.nx`), so node 1 is untouched and the "
                "sublist 2 → 3 → 4 → 5 → 6 → 7 is processed:\n"
                "- pair (2, 3) → 3, 2\n"
                "- pair (4, 5) → 5, 4\n"
                "- pair (6, 7) → 7, 6\n"
                "- Sublist becomes 3 → 2 → 5 → 4 → 7 → 6 and `h.nx` is relinked to its head 3.\n\n"
                "Output: `[1, 3, 2, 5, 4, 7, 6]`.\n\n"
                "**Options:** (A) swaps from the head. (C) shifts the pairing by one more node. (D) is a "
                "full reversal.\n\n"
                "**Trap:** forgetting to store the returned head — calling `swap_pairs(h.nx)` without "
                "assigning it to `h.nx` would leave node 1 pointing at node 2, which is now *second* in its "
                "pair, losing node 3 from the traversal."
            ),
            "solution_diagrams": [{"type": "linkedlist", "values": [1, 3, 2, 5, 4, 7, 6], "head": "h",
                                   "caption": "List after h.nx = swap_pairs(h.nx)"}],
            "verify": "assert OUTPUT.strip() == '[1, 3, 2, 5, 4, 7, 6]' and ANSWER == 'B'",
        },
        # ------------------------------------------------------------------ Q4
        {
            "type": "NAT", "marks": 1, "topic": "Binary search trees — internal path length",
            "text": ("The keys 40, 25, 60, 10, 30, 50, 70, 5, 35, 65, 80, 62 are inserted in this order into an "
                     "initially empty binary search tree. The sum of the depths of all nodes (the root has "
                     "depth 0) is ______."),
            "answer": "26",
            "solution": (
                "**Concept:** the depth of a key is the number of comparisons-with-descent made when it was "
                "inserted. The sum of depths (internal path length) determines the average cost of a "
                "successful search: (sum + n)/n comparisons.\n\n"
                "Insert and record depth:\n"
                "- 40 → depth 0 (root)\n"
                "- 25, 60 → depth 1 (children of 40)\n"
                "- 10, 30 (under 25), 50, 70 (under 60) → depth 2\n"
                "- 5 (left of 10), 35 (right of 30), 65 (left of 70), 80 (right of 70) → depth 3\n"
                "- 62 → 40 → 60 → 70 → 65 → left of 65 → depth 4\n\n"
                "Sum = 0 + 2·1 + 4·2 + 4·3 + 1·4 = 0 + 2 + 8 + 12 + 4 = **26**.\n\n"
                "(Average successful search = (26 + 12)/12 ≈ 3.17 comparisons.)\n\n"
                "**Trap:** taking the root's depth as 1 (which adds n = 12 and gives 38)."
            ),
            "solution_diagrams": [{"type": "bintree",
                                   "tree": [40, [25, [10, [5], None], [30, None, [35]]],
                                            [60, [50], [70, [65, [62], None], [80]]]],
                                   "highlight": [62], "caption": "BST after all insertions; 62 is the only depth-4 node"}],
            "verify": '''
def ins(t, k):
    if t is None: return [k, None, None]
    if k < t[0]: t[1] = ins(t[1], k)
    else: t[2] = ins(t[2], k)
    return t
T = None
for k in [40, 25, 60, 10, 30, 50, 70, 5, 35, 65, 80, 62]: T = ins(T, k)
def ipl(t, d=0): return 0 if t is None else d + ipl(t[1], d + 1) + ipl(t[2], d + 1)
assert ipl(T) == int(ANSWER)
''',
        },
        # ------------------------------------------------------------------ Q5
        {
            "type": "MCQ", "marks": 1, "topic": "Hashing — linear probing with lazy deletion",
            "text": ("A hash table of size 10 uses h(k) = k mod 10 with linear probing. Keys 21, 31, 12, 41, "
                     "15, 25 are inserted in that order. Then 31 is deleted by marking its slot DELETED "
                     "(a tombstone). A search skips over DELETED slots and stops at an EMPTY slot; an "
                     "insertion places the key in the first DELETED or EMPTY slot on its probe sequence.\n\n"
                     "Let p be the number of slots examined when searching for 41 after the deletion, and let s "
                     "be the slot where 51 is stored if it is inserted next. Then (p, s) is"),
            "options": ["(2, 2)", "(3, 2)", "(4, 7)", "(4, 2)"],
            "answer": "D",
            "solution": (
                "**Concept:** with open addressing, a deleted slot cannot simply be emptied — that would cut "
                "probe chains that pass through it. A tombstone keeps searches going but can be reused by "
                "insertions.\n\n"
                "Insertions: 21 → 1; 31 → 1 full → **2**; 12 → 2 full → **3**; 41 → 1, 2, 3 full → **4**; "
                "15 → 5; 25 → 5 full → **6**.\n\n"
                "Delete 31: slot 2 becomes DELETED.\n\n"
                "Search 41: slot 1 (21, no), slot 2 (DELETED, continue), slot 3 (12, no), slot 4 (41, found) "
                "→ **p = 4** slots examined.\n\n"
                "Insert 51: slot 1 occupied, slot 2 DELETED → reuse → **s = 2**.\n\n"
                "Answer (4, 2).\n\n"
                "**Options:** (A) is what happens if deletion *empties* slot 2: the search for 41 stops at "
                "the empty slot 2 after 2 probes and wrongly reports 'absent'. (B) miscounts the probes. "
                "(C) ignores tombstone reuse and places 51 in the first truly empty slot, 7.\n\n"
                "**Tip:** a common refinement first finishes the search (to avoid duplicates) and then "
                "inserts at the first tombstone seen."
            ),
            "solution_diagrams": [{"type": "hashtable", "size": 10,
                                   "slots": {1: 21, 2: "DEL", 3: 12, 4: 41, 5: 15, 6: 25},
                                   "caption": "Table after deleting 31 (before inserting 51)"}],
            "verify": '''
EMPTY, DEL = None, 'DEL'
T = [EMPTY]*10
for k in [21, 31, 12, 41, 15, 25]:
    i = k % 10
    while T[i] is not EMPTY: i = (i + 1) % 10
    T[i] = k
T[T.index(31)] = DEL
p, i = 0, 41 % 10
while True:
    p += 1
    if T[i] == 41 or T[i] is EMPTY: break
    i = (i + 1) % 10
i = 51 % 10
while T[i] not in (EMPTY, DEL): i = (i + 1) % 10
opts = [(2, 2), (3, 2), (4, 7), (4, 2)]
assert opts["ABCD".index(ANSWER)] == (p, i)
''',
        },
        # ------------------------------------------------------------------ Q6
        {
            "type": "NAT", "marks": 1, "topic": "Binary search — average successful comparisons",
            "text": ("Binary search (mid = ⌊(lo + hi)/2⌋, one three-way comparison per probe) is performed on a "
                     "sorted array of 15 distinct keys. Each key is equally likely to be searched for, and "
                     "every search is successful. The average number of probes, rounded off to two decimal "
                     "places, is ______."),
            "answer": ["3.26", "3.28"],
            "solution": (
                "**Concept:** the probes of binary search on n = 2^{k} − 1 keys form a perfectly balanced "
                "decision tree: 1 key is found with 1 probe (the middle), 2 keys with 2 probes, 4 with 3, "
                "8 with 4.\n\n"
                "For n = 15 (k = 4):\n"
                "- level 1: 1 key × 1 probe = 1\n"
                "- level 2: 2 keys × 2 = 4\n"
                "- level 3: 4 keys × 3 = 12\n"
                "- level 4: 8 keys × 4 = 32\n\n"
                "Total = 49 probes over 15 keys → 49/15 = **3.27**.\n\n"
                "Compare: the worst case is ⌊log₂ 15⌋ + 1 = 4 probes, so the average is close to the worst "
                "case because more than half the keys sit on the deepest level.\n\n"
                "**Trap:** averaging the levels (1 + 2 + 3 + 4)/4 = 2.5 ignores that deeper levels hold "
                "exponentially more keys."
            ),
            "solution_diagrams": [{"type": "bintree",
                                   "tree": [8, [4, [2, [1], [3]], [6, [5], [7]]],
                                            [12, [10, [9], [11]], [14, [13], [15]]]],
                                   "caption": "Decision tree of probe positions (1-based) for n = 15"}],
            "verify": '''
def probes(n, idx):
    lo, hi, c = 0, n - 1, 0
    while True:
        mid = (lo + hi) // 2; c += 1
        if mid == idx: return c
        if mid < idx: lo = mid + 1
        else: hi = mid - 1
avg = sum(probes(15, i) for i in range(15)) / 15
assert float(ANSWER[0]) <= avg <= float(ANSWER[1])
''',
        },
        # ------------------------------------------------------------------ Q7
        {
            "type": "MCQ", "marks": 1, "topic": "Bubble sort — state after k passes",
            "text": ("Bubble sort (each pass compares adjacent pairs from left to right and swaps if the left "
                     "element is larger) is applied to [6, 2, 9, 1, 5, 8, 3]. The array after **two** complete "
                     "passes is"),
            "options": [
                "[2, 1, 5, 6, 3, 8, 9]",
                "[1, 2, 6, 5, 3, 8, 9]",
                "[2, 6, 1, 5, 8, 3, 9]",
                "[1, 2, 3, 6, 9, 5, 8]",
            ],
            "answer": "A",
            "solution": (
                "**Concept:** each bubble-sort pass carries the largest remaining element to the end of the "
                "unsorted part; small elements move left by at most one position per pass.\n\n"
                "Pass 1 on [6, 2, 9, 1, 5, 8, 3]:\n"
                "- 6>2 swap → [2, 6, 9, 1, 5, 8, 3]; 6<9; 9>1 swap → [2, 6, 1, 9, 5, 8, 3]; 9>5 swap; 9>8 swap; "
                "9>3 swap → **[2, 6, 1, 5, 8, 3, 9]**\n\n"
                "Pass 2 (up to index 5):\n"
                "- 2<6; 6>1 swap → [2, 1, 6, 5, 8, 3, 9]; 6>5 swap → [2, 1, 5, 6, 8, 3, 9]; 6<8; 8>3 swap → "
                "**[2, 1, 5, 6, 3, 8, 9]**\n\n"
                "Answer (A).\n\n"
                "**Options:** (B) moves 1 from index 3 to index 0 in two passes — impossible, as a small "
                "element moves left by at most one position per pass. (C) is the state after one pass. (D) looks like a selection-sort "
                "state (smallest elements fixed at the front).\n\n"
                "**Tip:** after k passes the last k positions hold the k largest values in order (8, 9 here)."
            ),
            "solution_diagrams": [{"type": "matrix", "title": "Bubble sort passes",
                                   "col_labels": ["0", "1", "2", "3", "4", "5", "6"],
                                   "row_labels": ["start", "pass 1", "pass 2"],
                                   "rows": [[6, 2, 9, 1, 5, 8, 3], [2, 6, 1, 5, 8, 3, 9], [2, 1, 5, 6, 3, 8, 9]],
                                   "highlight": [[1, 6], [2, 5], [2, 6]]}],
            "verify": '''
a = [6, 2, 9, 1, 5, 8, 3]
for p in range(2):
    for j in range(len(a) - 1 - p):
        if a[j] > a[j+1]: a[j], a[j+1] = a[j+1], a[j]
opts = [[2,1,5,6,3,8,9], [1,2,6,5,3,8,9], [2,6,1,5,8,3,9], [1,2,3,6,9,5,8]]
assert opts["ABCD".index(ANSWER)] == a
''',
        },
        # ------------------------------------------------------------------ Q8
        {
            "type": "NAT", "marks": 1, "topic": "Graph theory — leaves of a tree",
            "text": ("A tree has exactly three vertices of degree 4, two vertices of degree 3, one vertex of "
                     "degree 2, and every other vertex has degree 1. The number of vertices of degree 1 "
                     "is ______."),
            "answer": "10",
            "solution": (
                "**Concept:** a tree with n vertices has n − 1 edges, and by the handshaking lemma "
                "Σ deg = 2(n − 1). Equivalently, #leaves = 2 + Σ over vertices of degree ≥ 2 of (deg − 2).\n\n"
                "Let L be the number of leaves. Then n = 3 + 2 + 1 + L = 6 + L.\n\n"
                "Degree sum: 3·4 + 2·3 + 1·2 + L·1 = 20 + L.\n\n"
                "Handshaking: 20 + L = 2(n − 1) = 2(5 + L) = 10 + 2L → **L = 10**.\n\n"
                "Shortcut check: 2 + 3·(4 − 2) + 2·(3 − 2) + 1·(2 − 2) = 2 + 6 + 2 + 0 = 10. ✓\n\n"
                "The tree has 16 vertices and 15 edges.\n\n"
                "**Trap:** forgetting the degree-2 vertex when computing n (giving 9). Note that degree-2 "
                "vertices never change the leaf count — they just subdivide edges."
            ),
            "verify": '''
for L in range(100):
    n = 6 + L
    if 3*4 + 2*3 + 2 + L == 2*(n - 1):
        break
assert L == int(ANSWER)
''',
        },
        # ------------------------------------------------------------------ Q9
        {
            "type": "MSQ", "marks": 1, "topic": "Heaps — min-heap insert and delete",
            "text": ("The array H = [3, 8, 5, 12, 9, 7, 6, 15, 14, 11] (0-based) is a binary min-heap. Which of "
                     "the following statements is/are TRUE? (Each refers to the original H.)"),
            "diagrams": [{"type": "heap", "values": [3, 8, 5, 12, 9, 7, 6, 15, 14, 11],
                          "caption": "Min-heap H"}],
            "options": [
                "Inserting 4 yields [3, 4, 5, 12, 8, 7, 6, 15, 14, 11, 9]",
                "Deleting the minimum yields [5, 8, 6, 12, 9, 7, 11, 15, 14]",
                "The third-smallest key, 6, is a child of the root",
                "H has exactly 5 leaves",
            ],
            "answer": ["A", "B", "D"],
            "solution": (
                "**Concept:** insertion appends and sifts up; delete-min moves the last element to the root "
                "and sifts down towards the **smaller** child.\n\n"
                "- (A) 4 goes to index 10; parent index 4 (9) > 4 → swap; parent index 1 (8) > 4 → swap; "
                "parent index 0 (3) < 4 → stop. Result [3, 4, 5, 12, 8, 7, 6, 15, 14, 11, 9]. **True.**\n"
                "- (B) Move 11 to the root: [11, 8, 5, 12, 9, 7, 6, 15, 14]. Smaller child 5 → swap → 11 at "
                "index 2; children 7, 6 → swap with 6 → 11 at index 6 (leaf). Result "
                "[5, 8, 6, 12, 9, 7, 11, 15, 14]. **True.**\n"
                "- (C) The root's children are 8 and 5; 6 is at index 6, a child of 5. **False.**\n"
                "- (D) A heap with n = 10 nodes has n − ⌊n/2⌋ = 5 leaves (indices 5..9). **True.**\n\n"
                "**Trap:** in (B), sifting towards the *left* child by default (8) would produce an invalid "
                "heap."
            ),
            "verify": '''
import heapq
H = [3, 8, 5, 12, 9, 7, 6, 15, 14, 11]
a = H[:]; heapq.heappush(a, 4)
b = H[:]; heapq.heappop(b)
leaves = sum(1 for i in range(len(H)) if 2*i + 1 >= len(H))
truth = [a == [3,4,5,12,8,7,6,15,14,11,9], b == [5,8,6,12,9,7,11,15,14],
         (H.index(6) - 1) // 2 == 0, leaves == 5]
assert sorted(ANSWER) == [x for x, ok in zip("ABCD", truth) if ok]
''',
        },
        # ------------------------------------------------------------------ Q10
        {
            "type": "MSQ", "marks": 1, "topic": "Python — built-in semantics",
            "text": "Which of the following Python 3 expressions evaluate to `True`?",
            "options": [
                "`sorted(\"BaNaNa\", key=str.lower) == ['a', 'a', 'a', 'B', 'N', 'N']`",
                "`[1, 2, 3] * 2 == [2, 4, 6]`",
                "`{1, 2, 3} ^ {2, 3, 4} == {1, 4}`",
                "`round(2.5) == 3`",
            ],
            "answer": ["A", "C"],
            "solution": (
                "**Concept checks:** key functions and stability of `sorted`, sequence repetition, set "
                "symmetric difference, and Python's rounding rule.\n\n"
                "- (A) Keys: B→b, a→a, N→n, a, N, a. Sorting by key puts the three 'a's first (in original "
                "order), then 'B', then the two 'N's. Result ['a', 'a', 'a', 'B', 'N', 'N']. **True.** "
                "(Without the key, uppercase letters sort before lowercase: ['B', 'N', 'N', 'a', 'a', 'a'].)\n"
                "- (B) `*` on a list means repetition: [1, 2, 3, 1, 2, 3], not element-wise multiplication. "
                "**False.**\n"
                "- (C) `^` is symmetric difference: elements in exactly one set → {1, 4}. **True.**\n"
                "- (D) Python 3 uses round-half-to-even ('banker's rounding'): round(2.5) = 2 "
                "(and round(3.5) = 4). **False.**\n\n"
                "**Trap:** (D) — most people expect 3 from school rounding."
            ),
            "verify": '''
vals = [sorted("BaNaNa", key=str.lower) == ['a','a','a','B','N','N'],
        [1, 2, 3] * 2 == [2, 4, 6], {1, 2, 3} ^ {2, 3, 4} == {1, 4}, round(2.5) == 3]
assert sorted(ANSWER) == [x for x, ok in zip("ABCD", vals) if ok]
''',
        },
        # ------------------------------------------------------------------ Q11
        {
            "type": "NAT", "marks": 2, "topic": "Python — counting recursive calls",
            "text": "Consider the following Python program. The value printed is ______.",
            "code": '''calls = 0

def f(n):
    global calls
    calls += 1
    if n <= 1:
        return 1
    return f(n - 1) + f(n // 2)

f(10)
print(calls)''',
            "answer": "59",
            "solution": (
                "**Concept:** without memoisation every call re-expands its whole recursion tree. The number "
                "of calls satisfies C(n) = 1 + C(n − 1) + C(⌊n/2⌋) for n ≥ 2 and C(0) = C(1) = 1.\n\n"
                "Bottom-up table:\n"
                "- C(0) = C(1) = 1\n"
                "- C(2) = 1 + C(1) + C(1) = 3\n"
                "- C(3) = 1 + C(2) + C(1) = 5\n"
                "- C(4) = 1 + C(3) + C(2) = 9\n"
                "- C(5) = 1 + C(4) + C(2) = 13\n"
                "- C(6) = 1 + C(5) + C(3) = 19\n"
                "- C(7) = 1 + C(6) + C(3) = 25\n"
                "- C(8) = 1 + C(7) + C(4) = 35\n"
                "- C(9) = 1 + C(8) + C(4) = 45\n"
                "- C(10) = 1 + C(9) + C(5) = **59**\n\n"
                "`global calls` makes the increment update the module-level counter (without it, "
                "`calls += 1` would raise UnboundLocalError).\n\n"
                "(The returned value f(10) is 30, but only the call count is printed.)\n\n"
                "**Trap:** forgetting to count the base-case calls (n ≤ 1), which are leaves of the "
                "recursion tree; with lru_cache only 10 distinct calls (n = 1..10) would remain."
            ),
            "verify": '''
assert int(OUTPUT) == int(ANSWER)
C = {0: 1, 1: 1}
for n in range(2, 11): C[n] = 1 + C[n-1] + C[n//2]
assert C[10] == 59
''',
        },
        # ------------------------------------------------------------------ Q12
        {
            "type": "MCQ", "marks": 2, "topic": "Merge sort — bottom-up passes",
            "text": ("Bottom-up merge sort sorts [9, 4, 7, 1, 8, 2, 5]. In the pass with run width w "
                     "(w = 1, 2, 4, …), the array is cut into consecutive blocks of 2w elements starting at "
                     "index 0, and in each block the first w elements are merged with the rest of the block "
                     "(which may be shorter than w, or empty). The array after the passes with w = 1 and "
                     "w = 2 is"),
            "options": [
                "[4, 9, 1, 7, 2, 8, 5]",
                "[1, 4, 7, 9, 2, 5, 8]",
                "[1, 4, 7, 9, 2, 8, 5]",
                "[1, 2, 4, 5, 7, 8, 9]",
            ],
            "answer": "B",
            "solution": (
                "**Concept:** bottom-up merge sort doubles the length of sorted runs each pass; a leftover "
                "short run at the end is merged with whatever partner exists (possibly an empty one).\n\n"
                "**Pass w = 1** (blocks of 2): [9, 4] → [4, 9]; [7, 1] → [1, 7]; [8, 2] → [2, 8]; [5] (alone) "
                "→ [5]. Array: [4, 9, 1, 7, 2, 8, 5].\n\n"
                "**Pass w = 2** (blocks of 4): [4, 9] + [1, 7] → [1, 4, 7, 9]; block starting at index 4 is "
                "[2, 8] + [5] → [2, 5, 8]. Array: **[1, 4, 7, 9, 2, 5, 8]**.\n\n"
                "(Pass w = 4 then merges [1, 4, 7, 9] with [2, 5, 8] to finish.)\n\n"
                "**Options:**\n"
                "- (A) is the state after only the w = 1 pass.\n"
                "- (C) fails to merge the short trailing run [5] with [2, 8].\n"
                "- (D) is the fully sorted array (after w = 4).\n\n"
                "**Tip:** bottom-up merge sort needs ⌈log₂ n⌉ passes — 3 for n = 7."
            ),
            "solution_diagrams": [{"type": "matrix", "title": "Bottom-up merge sort passes",
                                   "col_labels": ["0", "1", "2", "3", "4", "5", "6"],
                                   "row_labels": ["start", "w = 1", "w = 2", "w = 4"],
                                   "rows": [[9, 4, 7, 1, 8, 2, 5], [4, 9, 1, 7, 2, 8, 5],
                                            [1, 4, 7, 9, 2, 5, 8], [1, 2, 4, 5, 7, 8, 9]]}],
            "verify": '''
def merge(L, R):
    out, i, j = [], 0, 0
    while i < len(L) and j < len(R):
        if L[i] <= R[j]: out.append(L[i]); i += 1
        else: out.append(R[j]); j += 1
    return out + L[i:] + R[j:]
a, w = [9, 4, 7, 1, 8, 2, 5], 1
for _ in range(2):
    out = []
    for lo in range(0, len(a), 2 * w):
        out += merge(a[lo:lo + w], a[lo + w:lo + 2 * w])
    a, w = out, 2 * w
opts = [[4,9,1,7,2,8,5], [1,4,7,9,2,5,8], [1,4,7,9,2,8,5], [1,2,4,5,7,8,9]]
assert opts["ABCD".index(ANSWER)] == a
''',
        },
        # ------------------------------------------------------------------ Q13
        {
            "type": "MSQ", "marks": 2, "topic": "Binary search trees — reconstruction from post-order",
            "text": ("The post-order traversal of a binary search tree with distinct keys is\n"
                     "8, 15, 12, 22, 20, 35, 45, 40, 30.\n"
                     "Which of the following statements is/are TRUE? (Height = number of edges on the longest "
                     "root-to-leaf path.)"),
            "options": [
                "The pre-order traversal is 30, 20, 12, 8, 15, 22, 40, 35, 45",
                "The tree has exactly 4 leaves",
                "The height of the tree is 3",
                "If 30 is deleted by replacing it with its in-order predecessor, the new root is 22",
            ],
            "answer": ["A", "C", "D"],
            "solution": (
                "**Concept:** in a BST, the in-order traversal is the sorted key list, so post-order alone "
                "determines the tree: the last element is the root, keys smaller than it form the left "
                "subtree (a contiguous prefix of the post-order), larger keys the right subtree.\n\n"
                "Reconstruction:\n"
                "- Root 30. Left part (< 30): 8, 15, 12, 22, 20 → root 20; its left part 8, 15, 12 → root 12 "
                "with children 8 and 15; its right part 22 → leaf.\n"
                "- Right part (> 30): 35, 45, 40 → root 40 with children 35 and 45.\n\n"
                "**Verdicts:**\n"
                "- (A) pre-order: 30, 20, 12, 8, 15, 22, 40, 35, 45. **True.**\n"
                "- (B) leaves: 8, 15, 22, 35, 45 → **5**, not 4. **False.**\n"
                "- (C) longest path 30 → 20 → 12 → 8 (or → 15) has 3 edges. **True.**\n"
                "- (D) in-order predecessor of 30 = maximum of the left subtree = 22 (a leaf). It is copied "
                "into the root and removed. **True.**\n\n"
                "**Trap:** in (D), taking the predecessor to be the left child (20) — it is the *rightmost* "
                "node of the left subtree."
            ),
            "solution_diagrams": [{"type": "bintree",
                                   "tree": [30, [20, [12, [8], [15]], [22]], [40, [35], [45]]],
                                   "caption": "BST reconstructed from the post-order"}],
            "verify": '''
post = [8, 15, 12, 22, 20, 35, 45, 40, 30]
def build(p):
    if not p: return None
    r = p[-1]
    return [r, build([x for x in p[:-1] if x < r]), build([x for x in p[:-1] if x > r])]
T = build(post)
def pre(t): return [] if t is None else [t[0]] + pre(t[1]) + pre(t[2])
def leaves(t): return 0 if t is None else (1 if t[1] is None and t[2] is None else leaves(t[1]) + leaves(t[2]))
def h(t): return -1 if t is None else 1 + max(h(t[1]), h(t[2]))
def mx(t): return t[0] if t[2] is None else mx(t[2])
truth = [pre(T) == [30,20,12,8,15,22,40,35,45], leaves(T) == 4, h(T) == 3, mx(T[1]) == 22]
assert sorted(ANSWER) == [x for x, ok in zip("ABCD", truth) if ok]
''',
        },
        # ------------------------------------------------------------------ Q14
        {
            "type": "NAT", "marks": 2, "topic": "BFS — shortest path in a grid maze",
            "text": ("In the 5 × 6 grid below, `#` cells are walls. From any open cell one may move up, down, "
                     "left or right to an adjacent open cell (each move costs 1). The minimum number of moves "
                     "needed to go from S (row 0, column 0) to T (row 0, column 5) is ______."),
            "diagrams": [{"type": "matrix",
                          "col_labels": ["0", "1", "2", "3", "4", "5"],
                          "row_labels": ["0", "1", "2", "3", "4"],
                          "rows": [["S", "", "", "", "#", "T"],
                                   ["#", "#", "#", "", "#", ""],
                                   ["", "", "", "", "#", ""],
                                   ["", "#", "", "#", "#", ""],
                                   ["", "", "", "", "", ""]],
                          "highlight": [[0, 4], [1, 0], [1, 1], [1, 2], [1, 4], [2, 4], [3, 1], [3, 3], [3, 4]],
                          "caption": "Maze (highlighted cells are walls)"}],
            "answer": "15",
            "solution": (
                "**Concept:** on an unweighted grid, BFS from S labels every reachable cell with its "
                "shortest distance; the first time T is dequeued its label is the answer.\n\n"
                "The wall column 4 (rows 0–3) separates S from T, so any path must go round through row 4.\n\n"
                "BFS distances (see the solution table):\n"
                "- Row 0: 0, 1, 2, 3 → the only way down is column 3: (1,3) = 4, (2,3) = 5.\n"
                "- From (2,3) go left: (2,2) = 6, (2,1) = 7, (2,0) = 8.\n"
                "- Two ways down to row 4: via (3,2) = 7 → (4,2) = 8, or via (3,0) = 9 → (4,0) = 10.\n"
                "- The shorter one continues (4,3) = 9, (4,4) = 10, (4,5) = 11, then up column 5: "
                "(3,5) = 12, (2,5) = 13, (1,5) = 14, (0,5) = **15**.\n\n"
                "Path: S → (0,3) → (2,3) → (2,2) → (4,2) → (4,5) → T: 3 + 2 + 1 + 2 + 3 + 4 = 15 moves.\n\n"
                "**Trap:** missing the gap at (3,2) and going down at column 0 (19 moves), or computing the "
                "Manhattan distance 5, which ignores the walls."
            ),
            "solution_diagrams": [{"type": "matrix", "title": "BFS distance of every open cell",
                                   "col_labels": ["0", "1", "2", "3", "4", "5"],
                                   "row_labels": ["0", "1", "2", "3", "4"],
                                   "rows": [[0, 1, 2, 3, "#", 15], ["#", "#", "#", 4, "#", 14],
                                            [8, 7, 6, 5, "#", 13], [9, "#", 7, "#", "#", 12],
                                            [10, 9, 8, 9, 10, 11]],
                                   "highlight": [[0, 0], [0, 1], [0, 2], [0, 3], [1, 3], [2, 3], [2, 2], [3, 2],
                                                 [4, 2], [4, 3], [4, 4], [4, 5], [3, 5], [2, 5], [1, 5], [0, 5]]}],
            "verify": '''
from collections import deque
g = ["S...#T", "###.#.", "....#.", ".#.##.", "......"]
dist, q = {(0, 0): 0}, deque([(0, 0)])
while q:
    r, c = q.popleft()
    for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < 5 and 0 <= nc < 6 and g[nr][nc] != '#' and (nr, nc) not in dist:
            dist[(nr, nc)] = dist[(r, c)] + 1; q.append((nr, nc))
assert dist[(0, 5)] == int(ANSWER)
''',
        },
        # ------------------------------------------------------------------ Q15
        {
            "type": "MCQ", "marks": 2, "topic": "Python — class vs instance attributes",
            "text": "Consider the following Python program. What is printed?",
            "code": '''class Node:
    count = 0
    kids = []
    def __init__(self, v):
        self.v = v
        Node.count += 1
        self.count = Node.count * 10
    def add(self, c):
        self.kids.append(c)
        return self

a = Node(1)
b = Node(2).add(a)
c = Node(3)
c.add(b)
c.kids = []
print(Node.count, a.count, len(a.kids), len(c.kids))''',
            "options": ["`3 30 2 0`", "`3 10 0 0`", "`3 10 2 0`", "`3 10 1 0`"],
            "answer": "C",
            "solution": (
                "**Concept:** attribute *lookup* (`self.kids`) searches the instance first and then the "
                "class; attribute *assignment* (`self.count = …`, `c.kids = []`) always creates or rebinds an "
                "**instance** attribute and never touches the class attribute.\n\n"
                "Trace:\n"
                "- `Node(1)`: Node.count = 1; a.count = 10 (instance attribute shadows the class one).\n"
                "- `Node(2)`: Node.count = 2; its count = 20. `.add(a)`: the node has no own `kids`, so "
                "`self.kids` is the class list → class list = [a]. `add` returns the Node(2) object → b.\n"
                "- `Node(3)`: Node.count = 3; c.count = 30. `c.add(b)` → class list = [a, b].\n"
                "- `c.kids = []` gives c its own empty list; the class list is unchanged.\n\n"
                "Printed: Node.count = 3; a.count = 10; `a.kids` (class list) has length 2; `c.kids` "
                "(instance list) has length 0 → `3 10 2 0`.\n\n"
                "**Options:** (A) reads a.count from the class-level counter. (B) assumes each node has its "
                "own `kids` list. (D) forgets `c.add(b)` also appended to the shared list.\n\n"
                "**Trap:** a mutable *class* attribute used as if it were per-instance — the classic "
                "shared-list bug."
            ),
            "verify": "assert OUTPUT.strip() == '3 10 2 0' and ANSWER == 'C'",
        },
        # ------------------------------------------------------------------ Q16
        {
            "type": "NAT", "marks": 2, "topic": "Heaps — streaming k-th largest with a min-heap",
            "text": ("To maintain the 3 largest values of a stream, a min-heap of capacity 3 is used: the "
                     "first 3 values are simply inserted; afterwards, each new value x **replaces the root** "
                     "(pop-min then push x) if x is greater than the current root, and is discarded otherwise. "
                     "The stream is\n\n"
                     "5, 12, 3, 8, 15, 7, 10, 20, 1, 11\n\n"
                     "The number of root replacements performed is ______."),
            "answer": "4",
            "solution": (
                "**Concept:** a min-heap of size k holds the k largest values seen so far, and its root is "
                "the current k-th largest. A new value enters only if it beats the root. Cost: O(n log k).\n\n"
                "Trace (heap contents as a set; root = minimum):\n"
                "- 5, 12, 3 → {3, 5, 12}, root 3\n"
                "- 8 > 3 → replace (1) → {5, 8, 12}, root 5\n"
                "- 15 > 5 → replace (2) → {8, 12, 15}, root 8\n"
                "- 7 < 8 → discard\n"
                "- 10 > 8 → replace (3) → {10, 12, 15}, root 10\n"
                "- 20 > 10 → replace (4) → {12, 15, 20}, root 12\n"
                "- 1 → discard; 11 < 12 → discard\n\n"
                "Replacements = **4**; the final root 12 is the 3rd largest value of the stream (20, 15, 12).\n\n"
                "**Trap:** using a *max*-heap here — its root is the largest value, which tells you nothing "
                "about whether a new value belongs in the top 3."
            ),
            "solution_diagrams": [{"type": "heap", "values": [12, 15, 20],
                                   "caption": "Final min-heap: root 12 is the 3rd largest"}],
            "verify": '''
import heapq
h, rep = [], 0
for x in [5, 12, 3, 8, 15, 7, 10, 20, 1, 11]:
    if len(h) < 3: heapq.heappush(h, x)
    elif x > h[0]:
        heapq.heapreplace(h, x); rep += 1
assert rep == int(ANSWER) and h[0] == 12
''',
        },
        # ------------------------------------------------------------------ Q17
        {
            "type": "MSQ", "marks": 2, "topic": "Graph theory — bridges, cut vertices, bipartiteness",
            "text": "Consider the undirected graph G shown below. Which of the following statements is/are TRUE?",
            "diagrams": [{"type": "graph", "directed": False,
                          "nodes": ["A", "B", "C", "D", "E", "F", "G", "H"],
                          "edges": [["A", "B"], ["A", "C"], ["B", "C"], ["C", "D"], ["D", "E"], ["D", "F"],
                                    ["E", "F"], ["F", "G"], ["G", "H"]],
                          "pos": {"A": [0, 2], "B": [0, 0], "C": [1.5, 1], "D": [3, 1], "E": [4.5, 2],
                                  "F": [4.5, 0], "G": [6, 0], "H": [7.5, 0]}}],
            "options": [
                "G has exactly 3 bridges (edges whose removal disconnects the graph)",
                "G is bipartite",
                "Removing vertex D (with its edges) leaves exactly 2 connected components",
                "G has exactly 3 articulation points (cut vertices)",
            ],
            "answer": ["A", "C"],
            "solution": (
                "**Concept:** an edge is a bridge iff it lies on no cycle; a vertex is a cut vertex iff "
                "removing it increases the number of components. A graph is bipartite iff it has no odd "
                "cycle.\n\n"
                "Cycles: triangle A–B–C and triangle D–E–F. Edges outside every cycle: C–D, F–G, G–H.\n\n"
                "- (A) Bridges are exactly C–D, F–G, G–H → 3. **True.**\n"
                "- (B) Triangles are odd cycles → not bipartite. **False.**\n"
                "- (C) Without D: {A, B, C} and {E, F, G, H} (E–F–G–H still connected). Exactly 2. **True.**\n"
                "- (D) Cut vertices: C (separates A, B), D, F (separates G, H), G (separates H) → **4**. "
                "**False.**\n\n"
                "**Trap:** in (D) forgetting G — an internal vertex of a pendant path is always a cut vertex. "
                "Also note: an endpoint of a bridge is a cut vertex unless it has degree 1 (H is not a cut "
                "vertex).\n\n"
                "**Method tip:** for small graphs, first mark every edge that lies on a cycle (here the six "
                "triangle edges); the remaining edges are exactly the bridges. Then a vertex is a cut vertex "
                "iff it is an endpoint of a bridge with degree ≥ 2, or it joins two cycles that share only "
                "that vertex."
            ),
            "verify": '''
E = [('A','B'),('A','C'),('B','C'),('C','D'),('D','E'),('D','F'),('E','F'),('F','G'),('G','H')]
V = "ABCDEFGH"
def comps(vs, es):
    adj = {v: set() for v in vs}
    for u, v in es:
        if u in adj and v in adj: adj[u].add(v); adj[v].add(u)
    seen, c = set(), 0
    for s in vs:
        if s in seen: continue
        c += 1; st = [s]
        while st:
            u = st.pop()
            if u in seen: continue
            seen.add(u); st += list(adj[u])
    return c
bridges = sum(comps(V, [e for e in E if e != x]) > 1 for x in E)
cuts = sum(comps(V.replace(v, ''), E) > 1 for v in V)
col, bip = {'A': 0}, True
for _ in range(10):
    for u, v in E:
        for a, b in ((u, v), (v, u)):
            if a in col:
                if b in col and col[b] == col[a]: bip = False
                col.setdefault(b, 1 - col[a])
truth = [bridges == 3, bip, comps(V.replace('D', ''), E) == 2, cuts == 3]
assert sorted(ANSWER) == [x for x, ok in zip("ABCD", truth) if ok]
''',
        },
        # ------------------------------------------------------------------ Q18
        {
            "type": "NAT", "marks": 2, "topic": "Hashing — expected number of empty slots",
            "text": ("Six keys are inserted into a hash table with 8 slots using separate chaining. Assume "
                     "simple uniform hashing: each key independently hashes to each slot with probability 1/8. "
                     "The expected number of slots that remain **empty**, rounded off to two decimal places, "
                     "is ______."),
            "answer": ["3.58", "3.60"],
            "solution": (
                "**Concept:** use linearity of expectation with indicator variables — no need to work out the "
                "distribution of empty slots.\n\n"
                "Let X_{j} = 1 if slot j is empty after all insertions. A given key misses slot j with "
                "probability 7/8, and the keys are independent, so\n"
                "P(X_{j} = 1) = (7/8)^{6}.\n\n"
                "E[#empty] = Σ_{j=1}^{8} E[X_{j}] = 8 · (7/8)^{6}.\n\n"
                "Compute: (7/8)^{2} = 0.765625; (7/8)^{3} = 0.669922; (7/8)^{6} = 0.669922² ≈ 0.448795.\n"
                "8 × 0.448795 ≈ **3.59**.\n\n"
                "So on average fewer than half of the 8 slots are used even though there are 6 keys — "
                "collisions are common long before the table is 'full' (birthday paradox).\n\n"
                "**Why not count directly?** The number of empty slots is a dependent sum (if one slot is empty, "
                "the others are slightly more likely to be hit), but linearity of expectation holds "
                "regardless of dependence, so the indicator method is exact.\n\n"
                "**Related quantity:** the expected number of *occupied* slots is 8 − 3.59 ≈ 4.41, and the "
                "expected number of colliding key pairs is C(6, 2)/8 = 1.875.\n\n"
                "**Trap:** answering 8 − 6 = 2 (that assumes no collisions at all), or using (1/8)^{6}."
            ),
            "verify": '''
import itertools
exp = 8 * (7/8)**6
assert float(ANSWER[0]) <= exp <= float(ANSWER[1])
''',
        },
        # ------------------------------------------------------------------ Q19
        {
            "type": "MCQ", "marks": 2, "topic": "Complexity — nested loops with halving and doubling",
            "text": "The function below returns c. As a function of n, the returned value is",
            "code": '''def work(n):
    c = 0
    i = n
    while i > 1:
        j = 1
        while j < i:
            c += 1
            j *= 2
        i //= 2
    return c''',
            "options": ["Θ(log n)", "Θ(log² n)", "Θ(n)", "Θ(n log n)"],
            "answer": "B",
            "solution": (
                "**Concept:** the outer loop halves i, so it runs about log₂ n times; for a given i, the inner "
                "loop doubles j from 1 until it reaches i, i.e. ⌈log₂ i⌉ iterations.\n\n"
                "Take n = 2^{k}. The outer loop sees i = 2^{k}, 2^{k−1}, …, 2 and the inner loop runs "
                "k, k − 1, …, 1 times respectively:\n"
                "c = k + (k − 1) + … + 1 = k(k + 1)/2 = Θ(k²) = **Θ(log² n)**.\n\n"
                "Check: work(2) = 1, work(4) = 3, work(8) = 6, work(16) = 10, work(64) = 21.\n\n"
                "**Options:**\n"
                "- (A) counts only the outer loop.\n"
                "- (C) would hold if the inner loop ran i times (j += 1) — then c = n + n/2 + … ≈ 2n.\n"
                "- (D) would need a linear inner loop with a linear outer loop.\n\n"
                "**Trap:** multiplying 'log n outer × log n inner' gives the right order here, but the "
                "careful sum shows the constant is 1/2: c ≈ (log₂ n)²/2."
            ),
            "verify": '''
vals = [work(2**k) for k in range(1, 15)]
assert vals == [k*(k+1)//2 for k in range(1, 15)] and ANSWER == "B"
''',
        },
        # ------------------------------------------------------------------ Q20
        {
            "type": "MSQ", "marks": 2, "topic": "Linked lists + stacks — palindrome check",
            "text": ("The function below checks whether a singly linked list is a palindrome, using a slow/fast "
                     "pointer pair and a stack. Which of the following statements is/are TRUE?"),
            "code": '''def is_pal(head):
    st, slow, fast = [], head, head
    while fast and fast.nx:
        st.append(slow.v)
        slow = slow.nx
        fast = fast.nx.nx
    if fast:
        slow = slow.nx
    while slow:
        if st.pop() != slow.v:
            return False
        slow = slow.nx
    return True''',
            "run_code": False,
            "options": [
                "It returns True for the list 1 → 2 → 3 → 2 → 1",
                "It returns True for the list 4 → 5 → 5 → 4 → 4",
                "For a list of 9 nodes, the stack never holds more than 4 values",
                "It returns True for the list 1 → 2 → 1 → 2",
            ],
            "answer": ["A", "C"],
            "solution": (
                "**Concept:** the fast pointer moves two steps per iteration, so when it stops, slow is at "
                "the middle and the stack holds the first ⌊n/2⌋ values (in reverse order). For odd n "
                "(`fast` not None) the middle node is skipped. The second half is then compared with the "
                "popped values.\n\n"
                "- (A) n = 5: stack [1, 2]; slow at 3, fast at the last node → skip 3. Compare 2 = pop 2, "
                "1 = pop 1 → True. **True.**\n"
                "- (B) n = 5: stack [4, 5]; skip middle 5; compare 4 with pop 5 → mismatch → False. "
                "**False.** (Reversed it reads 4 4 5 5 4.)\n"
                "- (C) n = 9: the loop runs while fast and fast.nx exist: fast visits nodes 1, 3, 5, 7, 9 → "
                "4 iterations → 4 pushes; afterwards the stack only shrinks. **True.**\n"
                "- (D) n = 4: stack [1, 2]; fast becomes None → no skip; compare 1 with pop 2 → False. "
                "**False.**\n\n"
                "**Trap:** forgetting to skip the middle element for odd lengths — then (A) would compare 3 "
                "against 2 and fail. The `if fast:` line handles exactly that."
            ),
            "verify": '''
class N:
    def __init__(s, v, nx=None): s.v, s.nx = v, nx
def build(xs):
    h = None
    for x in reversed(xs): h = N(x, h)
    return h
peak = [0]
def is_pal(head):
    st, slow, fast = [], head, head
    while fast and fast.nx:
        st.append(slow.v); slow = slow.nx; fast = fast.nx.nx
        peak[0] = max(peak[0], len(st))
    if fast: slow = slow.nx
    while slow:
        if st.pop() != slow.v: return False
        slow = slow.nx
    return True
A = is_pal(build([1, 2, 3, 2, 1])); B = is_pal(build([4, 5, 5, 4, 4]))
peak[0] = 0; is_pal(build([1]*9)); C = peak[0] <= 4
D = is_pal(build([1, 2, 1, 2]))
assert sorted(ANSWER) == [x for x, ok in zip("ABCD", [A, B, C, D]) if ok]
''',
        },
    ],
}
