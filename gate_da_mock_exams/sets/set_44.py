# Set 44 — Full-Syllabus Mock — Paper 14 (GATE-level)
SET = {
    "number": 44,
    "title": "Full-Syllabus Mock — Paper 14",
    "difficulty": "GATE-level",
    "focus": "balanced paper across the whole Section 4 syllabus",
    "questions": [
        # ---------------------------------------------------------------- Q1
        {
            "type": "MCQ", "marks": 1, "topic": "Python — `+=` versus `+` on lists",
            "text": "What is printed by the following Python program?",
            "code": '''a = [1, 2]
b = a
b += [3]
c = a
c = c + [4]
print(a, c, a is b)''',
            "options": ["`[1, 2] [1, 2, 4] False`", "`[1, 2, 3] [1, 2, 3, 4] True`",
                        "`[1, 2, 3, 4] [1, 2, 3, 4] True`", "`[1, 2, 3] [1, 2, 3, 4] False`"],
            "answer": "B",
            "solution": (
                "**Concept.** For lists, `b += [3]` calls `list.__iadd__`, which **extends the existing list in "
                "place** and rebinds b to the same object. `c = c + [4]` builds a **new** list and rebinds only "
                "c.\n\n"
                "**Trace.**\n"
                "- `b = a`: one list [1, 2], two names.\n"
                "- `b += [3]`: the shared list becomes [1, 2, 3]; a and b still refer to it.\n"
                "- `c = a`, then `c = c + [4]`: a new list [1, 2, 3, 4] is bound to c; a is unchanged.\n"
                "- `a is b` → True.\n\n"
                "Output: `[1, 2, 3] [1, 2, 3, 4] True`.\n\n"
                "**Options.**\n"
                "- (A) treats `+=` like `+` (creating a new list for b).\n"
                "- (C) treats `c = c + [4]` as an in-place change of a.\n"
                "- (D) thinks `+=` rebinds b to a different object.\n\n"
                "**Trap:** for immutable types (int, str, tuple) `x += y` always creates a new object; for "
                "lists it mutates — the same syntax, different semantics."
            ),
            "verify": "assert OUTPUT.strip() == '[1, 2, 3] [1, 2, 3, 4] True' and ANSWER == 'B'",
        },
        # ---------------------------------------------------------------- Q2
        {
            "type": "NAT", "marks": 1, "topic": "Python — dictionary keys and overwriting",
            "text": "What value is printed by the following Python program?",
            "code": '''d = {x % 4: x for x in [3, 8, 11, 14, 7, 20]}
e = {1: 'a', True: 'b', 1.0: 'c'}
print(sum(d.values()) + len(e))''',
            "answer": "42",
            "solution": (
                "**Concept.** In a dict comprehension a repeated key keeps its first insertion position but its "
                "value is overwritten by the *last* assignment. Keys are compared by hash and equality, and "
                "`1 == True == 1.0` with equal hashes, so they are the **same** key.\n\n"
                "**d.** Keys x % 4: 3→3, 8→0, 11→3, 14→2, 7→3, 20→0.\n"
                "- key 3: 3, then 11, then 7 → final 7\n"
                "- key 0: 8, then 20 → final 20\n"
                "- key 2: 14\n"
                "sum(d.values()) = 7 + 20 + 14 = 41.\n\n"
                "**e.** All three keys are equal, so e has a single entry {1: 'c'} (first key object kept, last "
                "value) → len(e) = 1.\n\n"
                "Printed: 41 + 1 = **42**.\n\n"
                "**Trap:** expecting len(e) = 3 (keys look different) or summing all six numbers (63)."
            ),
            "verify": '''
dd = {}
for x in [3, 8, 11, 14, 7, 20]: dd[x % 4] = x
assert sum(dd.values()) + 1 == int(ANSWER) == int(OUTPUT.strip()) and e == {1: 'c'}
''',
        },
        # ---------------------------------------------------------------- Q3
        {
            "type": "MCQ", "marks": 1, "topic": "Stacks — prefix expression evaluation",
            "text": ("The prefix (Polish) expression\n\n`- * + 4 3 2 / 8 ^ 2 2`\n\nis evaluated with a stack by "
                     "scanning the tokens from **right to left** (push operands; on an operator pop the top two "
                     "values x then y and push x op y). Here `/` is integer division and `^` is exponentiation. "
                     "The result is"),
            "options": ["12", "-12", "14", "2"],
            "answer": "A",
            "solution": (
                "**Concept.** Scanning a prefix expression right-to-left makes it behave like postfix, but the "
                "operand order flips: the **first** value popped is the **left** operand.\n\n"
                "**Trace** (stack bottom → top):\n"
                "- 2 → [2]; 2 → [2, 2]\n"
                "- ^ : x = 2, y = 2 → 2 ^ 2 = 4 → [4]\n"
                "- 8 → [4, 8]\n"
                "- / : x = 8, y = 4 → 8 / 4 = 2 → [2]\n"
                "- 2 → [2, 2]; 3 → [2, 2, 3]; 4 → [2, 2, 3, 4]\n"
                "- + : 4 + 3 = 7 → [2, 2, 7]\n"
                "- * : 7 × 2 = 14 → [2, 14]\n"
                "- − : x = 14, y = 2 → 14 − 2 = **12**.\n\n"
                "Infix form: ((4 + 3) × 2) − (8 / (2 ^ 2)) = 14 − 2 = 12.\n\n"
                "**Options.**\n"
                "- (B) −12 swaps the operands of − (computes y − x).\n"
                "- (C) 14 and (D) 2 are the values of the two operand sub-expressions of the outer −.\n\n"
                "**Trap:** with right-to-left scanning, popping order is the reverse of postfix evaluation."
            ),
            "verify": '''
st = []
for t in reversed("- * + 4 3 2 / 8 ^ 2 2".split()):
    if t.isdigit(): st.append(int(t))
    else:
        x, y = st.pop(), st.pop()
        st.append({'+': x + y, '-': x - y, '*': x * y, '/': x // y, '^': x ** y}[t])
assert ["12", "-12", "14", "2"]["ABCD".index(ANSWER)] == str(st[0])
''',
        },
        # ---------------------------------------------------------------- Q4
        {
            "type": "MCQ", "marks": 1, "topic": "Deques — bounded deque in Python",
            "text": "What is printed by the following Python program?",
            "code": '''from collections import deque
dq = deque(maxlen=3)
for x in range(1, 6):
    dq.append(x)
dq.appendleft(0)
dq.rotate(1)
print(list(dq))''',
            "options": ["`[0, 3, 4]`", "`[4, 0, 3]`", "`[5, 0, 3]`", "`[3, 4, 5]`"],
            "answer": "B",
            "solution": (
                "**Concept.** A deque with `maxlen` discards from the **opposite end** when full: `append` "
                "drops the leftmost item, `appendleft` drops the rightmost. `rotate(1)` moves the last element "
                "to the front.\n\n"
                "**Trace.**\n"
                "- Appending 1..5: [1] → [1, 2] → [1, 2, 3] → [2, 3, 4] → [3, 4, 5].\n"
                "- `appendleft(0)`: deque is full, so 5 is dropped from the right → [0, 3, 4].\n"
                "- `rotate(1)`: last element 4 goes to the front → [4, 0, 3].\n\n"
                "**Options.**\n"
                "- (A) forgets the rotation.\n"
                "- (C) assumes appendleft dropped from the left end (the 4) and kept 5.\n"
                "- (D) assumes appendleft is ignored on a full deque.\n\n"
                "**Tip:** a `deque(maxlen=k)` is a ready-made sliding window / circular buffer of the last k "
                "items, with O(1) operations at both ends."
            ),
            "solution_diagrams": [{"type": "queue", "values": [4, 0, 3],
                                   "caption": "Final deque (left → right)"}],
            "verify": "assert OUTPUT.strip() == '[4, 0, 3]' and ANSWER == 'B'",
        },
        # ---------------------------------------------------------------- Q5
        {
            "type": "NAT", "marks": 1, "topic": "Linked lists — middle node with slow/fast pointers",
            "text": "What value is printed by the following Python program?",
            "code": '''class Node:
    def __init__(self, val, nxt=None):
        self.val, self.next = val, nxt

def mid1(h):
    slow = fast = h
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    return slow

def mid2(h):
    slow = fast = h
    while fast.next and fast.next.next:
        slow, fast = slow.next, fast.next.next
    return slow

head = None
for v in reversed([12, 7, 30, 5, 18, 41, 9, 26]):
    head = Node(v, head)
print(mid1(head).val - mid2(head).val)''',
            "diagrams": [{"type": "linkedlist", "values": [12, 7, 30, 5, 18, 41, 9, 26], "head": "head"}],
            "answer": "13",
            "solution": (
                "**Concept.** For a list of even length n, the two loop conditions pick different middles: "
                "`while fast and fast.next` stops with slow at index n/2 (the **second** middle); "
                "`while fast.next and fast.next.next` stops with slow at index n/2 − 1 (the **first** middle).\n\n"
                "**mid1** (indices 0-based): (slow, fast) = (0, 0) → (1, 2) → (2, 4) → (3, 6) → (4, 8 = None). "
                "Loop stops; slow at index 4 → value 18.\n\n"
                "**mid2**: (0, 0) → (1, 2) → (2, 4) → (3, 6); now fast.next is index 7 but fast.next.next is "
                "None → stop. slow at index 3 → value 5.\n\n"
                "Printed: 18 − 5 = **13**.\n\n"
                "**Trap:** both functions agree on odd-length lists; only even lengths reveal the difference. "
                "Merge sort on linked lists usually wants `mid2` so that both halves are non-empty for n = 2."
            ),
            "verify": '''
L = [12, 7, 30, 5, 18, 41, 9, 26]
assert L[len(L) // 2] - L[len(L) // 2 - 1] == int(ANSWER) == int(OUTPUT.strip())
''',
        },
        # ---------------------------------------------------------------- Q6
        {
            "type": "MSQ", "marks": 1, "topic": "BST — possible search paths",
            "text": ("A binary search tree contains integer keys from 1 to 100 (not necessarily all of them), and "
                     "a search for the key **55** is performed. Which of the following could be the sequence of "
                     "keys examined by the search?"),
            "options": ["90, 20, 70, 30, 60, 50, 55", "10, 80, 40, 75, 45, 60, 55",
                        "70, 30, 65, 40, 68, 55", "25, 95, 50, 90, 52, 58, 53, 55"],
            "answer": ["A", "B", "D"],
            "solution": (
                "**Concept.** Maintain the open interval (low, high) of keys still possible. Each examined key "
                "must lie inside the current interval; if it is greater than 55 it becomes the new high, if "
                "smaller the new low.\n\n"
                "- (A) (−∞,∞): 90 → (−∞,90); 20 → (20,90); 70 → (20,70); 30 → (30,70); 60 → (30,60); "
                "50 → (50,60); 55 ✓. **Possible.**\n"
                "- (B) 10 → (10,∞); 80 → (10,80); 40 → (40,80); 75 → (40,75); 45 → (45,75); 60 → (45,60); "
                "55 ✓. **Possible.**\n"
                "- (C) 70 → (−∞,70); 30 → (30,70); 65 → (30,65); 40 → (40,65); **68 is outside (40,65)** — "
                "after going left at 65, every later key must be < 65. **Not possible.**\n"
                "- (D) 25 → (25,∞); 95 → (25,95); 50 → (50,95); 90 → (50,90); 52 → (52,90); 58 → (52,58); "
                "53 → (53,58); 55 ✓. **Possible.**\n\n"
                "**Trap:** checking only the immediate parent (68 > 40, so 'go right' looks fine) misses the "
                "constraint imposed by the earlier ancestor 65."
            ),
            "verify": '''
def ok(seq, key=55):
    lo, hi = float('-inf'), float('inf')
    for x in seq[:-1]:
        if not lo < x < hi: return False
        if x > key: hi = x
        else: lo = x
    return seq[-1] == key and lo < key < hi
opts = [[90, 20, 70, 30, 60, 50, 55], [10, 80, 40, 75, 45, 60, 55],
        [70, 30, 65, 40, 68, 55], [25, 95, 50, 90, 52, 58, 53, 55]]
assert [L for L, s in zip("ABCD", opts) if ok(s)] == sorted(ANSWER)
''',
        },
        # ---------------------------------------------------------------- Q7
        {
            "type": "MCQ", "marks": 1, "topic": "Hashing — linear probing with wrap-around",
            "text": ("Keys 4, 15, 9, 26, 20 are inserted in this order into an empty hash table with slots 0–10, "
                     "using h(k) = (2k + 3) mod 11 and linear probing (slot after 10 is 0). In which slot is "
                     "20 stored?"),
            "options": ["3", "0", "4", "2"],
            "answer": "A",
            "solution": (
                "**Concept.** Linear probing scans h, h+1, h+2, … modulo the table size, so a search that "
                "starts near the end of the table wraps around to slot 0.\n\n"
                "**Hash values.** 4 → 11 mod 11 = 0; 15 → 33 mod 11 = 0; 9 → 21 mod 11 = 10; "
                "26 → 55 mod 11 = 0; 20 → 43 mod 11 = 10.\n\n"
                "**Trace.**\n"
                "- 4 → slot 0.\n- 15 → 0 full → slot 1.\n- 9 → slot 10.\n- 26 → 0, 1 full → slot 2.\n"
                "- 20 → 10 full → 0 → 1 → 2 full → slot **3**.\n\n"
                "**Options.**\n"
                "- (B) 0 is 20's position if wrap-around were applied without checking occupancy.\n"
                "- (C) 4 skips one slot too many.\n"
                "- (D) 2 is 26's slot — it would be 20's only if 20 had been inserted before 26.\n\n"
                "**Insight:** keys with different home slots (0 and 10) merge into one cluster across the "
                "wrap-around — primary clustering does not respect the 'end' of the array."
            ),
            "solution_diagrams": [{"type": "hashtable", "size": 11, "slots": {0: 4, 1: 15, 2: 26, 3: 20, 10: 9},
                                   "caption": "Final table"}],
            "verify": '''
T = [None] * 11
for k in [4, 15, 9, 26, 20]:
    i = (2 * k + 3) % 11
    while T[i] is not None: i = (i + 1) % 11
    T[i] = k
assert ["3", "0", "4", "2"]["ABCD".index(ANSWER)] == str(T.index(20))
''',
        },
        # ---------------------------------------------------------------- Q8
        {
            "type": "MSQ", "marks": 1, "topic": "Bubble sort — passes and swaps",
            "text": ("Bubble sort (each pass scans left to right over the unsorted prefix, swapping adjacent "
                     "out-of-order pairs) is applied to A = [62, 18, 45, 7, 53, 29, 11]. Which of the following "
                     "statements is/are TRUE?"),
            "options": [
                "After 2 passes, A = [18, 7, 45, 29, 11, 53, 62]",
                "The first 2 passes perform 9 swaps in total",
                "After any 2 passes of bubble sort on any array, the two largest elements are in their final "
                "positions",
                "Sorting A completely requires 15 swaps",
            ],
            "answer": ["A", "B", "C"],
            "solution": (
                "**Pass 1:** 62 bubbles to the end, swapping with 18, 45, 7, 53, 29, 11 (6 swaps) → "
                "[18, 45, 7, 53, 29, 11, 62].\n\n"
                "**Pass 2:** 18<45 ok; 45>7 swap; 45<53 ok; 53>29 swap; 53>11 swap (3 swaps) → "
                "[18, 7, 45, 29, 11, 53, 62].\n\n"
                "- (A) **True.**\n"
                "- (B) **True** — 6 + 3 = 9.\n"
                "- (C) **True** — pass k carries the k-th largest element to position n − k; this invariant "
                "holds for every input.\n"
                "- (D) **False** — bubble sort performs exactly one swap per inversion, and A has 14 "
                "inversions (62: 6, 18: 2, 45: 3, 7: 0, 53: 2, 29: 1, 11: 0), so 14 swaps.\n\n"
                "**Trap:** counting comparisons (6 + 5 + 4 + …) instead of swaps, or mis-tallying inversions."
            ),
            "solution_diagrams": [{"type": "matrix", "title": "Array after each pass",
                                   "row_labels": ["start", "pass 1", "pass 2"],
                                   "rows": [[62, 18, 45, 7, 53, 29, 11], [18, 45, 7, 53, 29, 11, 62],
                                            [18, 7, 45, 29, 11, 53, 62]],
                                   "highlight": [[1, 6], [2, 5], [2, 6]]}],
            "verify": '''
A = [62, 18, 45, 7, 53, 29, 11]; sw = 0
for p in range(2):
    for j in range(len(A) - 1 - p):
        if A[j] > A[j + 1]: A[j], A[j + 1] = A[j + 1], A[j]; sw += 1
B = [62, 18, 45, 7, 53, 29, 11]
inv = sum(B[i] > B[j] for i in range(7) for j in range(i + 1, 7))
import random
random.seed(1); okC = True
for _ in range(300):
    X = random.sample(range(100), 8); Y = X[:]
    for p in range(2):
        for j in range(7 - p):
            if Y[j] > Y[j + 1]: Y[j], Y[j + 1] = Y[j + 1], Y[j]
    okC &= Y[-2:] == sorted(X)[-2:]
r = {'A': A == [18, 7, 45, 29, 11, 53, 62], 'B': sw == 9, 'C': okC, 'D': inv == 15}
assert sorted(k for k in r if r[k]) == sorted(ANSWER)
''',
        },
        # ---------------------------------------------------------------- Q9
        {
            "type": "NAT", "marks": 1, "topic": "BFS — counting possible visiting orders",
            "text": ("BFS is run on the undirected graph below starting from P. When a vertex is dequeued, its "
                     "undiscovered neighbours may be enqueued in **any** order. The number of distinct orders "
                     "in which BFS can visit (dequeue) the vertices is ______."),
            "diagrams": [{"type": "graph", "directed": False,
                          "nodes": ["P", "Q", "R", "S", "T", "U", "V", "W"],
                          "edges": [["P", "Q"], ["P", "R"], ["Q", "S"], ["Q", "T"], ["Q", "U"],
                                    ["R", "U"], ["R", "V"], ["S", "W"], ["V", "W"]],
                          "pos": {"P": [3, 4], "Q": [1.5, 2.5], "R": [4.5, 2.5], "S": [0, 1],
                                  "T": [1.5, 1], "U": [3, 1], "V": [4.5, 1], "W": [2.25, -0.5]}}],
            "answer": "10",
            "solution": (
                "**Concept.** A BFS order is fixed once we choose, for every dequeued vertex, the order in which "
                "its *newly discovered* neighbours are enqueued. Branch on these choices.\n\n"
                "**Case 1: Q before R** (level 1 = Q, R).\n"
                "- Q discovers S, T, U → 3! = 6 orders. Then R discovers only V (U already seen).\n"
                "- Level 3: W is discovered by the first of S, V to be dequeued — S (it precedes V). One "
                "way.\n- Subtotal 6.\n\n"
                "**Case 2: R before Q.**\n"
                "- R discovers U, V → 2 orders; Q then discovers S, T → 2 orders.\n"
                "- W is discovered by V (V precedes S). One way.\n- Subtotal 4.\n\n"
                "Total = 6 + 4 = **10**.\n\n"
                "**Trap:** multiplying level sizes (2! × 4! × 1 = 48) ignores that a vertex discovered by one "
                "parent cannot appear among another parent's children — U's position depends on whether Q or "
                "R is dequeued first."
            ),
            "verify": '''
import itertools
E = ["PQ", "PR", "QS", "QT", "QU", "RU", "RV", "SW", "VW"]
G = {}
for a, b in E:
    G.setdefault(a, []).append(b); G.setdefault(b, []).append(a)
res = set()
def rec(order, queue, seen):
    if not queue: res.add("".join(order)); return
    u = queue[0]; new = [v for v in G[u] if v not in seen]
    for p in itertools.permutations(new):
        rec(order + list(p), queue[1:] + list(p), seen | set(new))
rec(['P'], ['P'], {'P'})
assert len(res) == int(ANSWER)
''',
        },
        # ---------------------------------------------------------------- Q10
        {
            "type": "NAT", "marks": 1, "topic": "Recursion — counting calls",
            "text": "How many times is the function `f` called (including the initial call) when `f(8)` is evaluated?",
            "code": '''def f(n):
    if n <= 2:
        return 1
    return f(n - 1) + f(n - 3)

print(f(8))''',
            "answer": "25",
            "solution": (
                "**Concept.** Let C(n) be the number of calls made when evaluating f(n). For n ≤ 2 there is just "
                "the one call; otherwise C(n) = 1 + C(n − 1) + C(n − 3).\n\n"
                "**Table.**\n"
                "- C(0) = C(1) = C(2) = 1 (note f(0) is reached from f(3)).\n"
                "- C(3) = 1 + C(2) + C(0) = 3\n"
                "- C(4) = 1 + C(3) + C(1) = 5\n"
                "- C(5) = 1 + C(4) + C(2) = 7\n"
                "- C(6) = 1 + C(5) + C(3) = 11\n"
                "- C(7) = 1 + C(6) + C(4) = 17\n"
                "- C(8) = 1 + C(7) + C(5) = **25**\n\n"
                "(The printed value f(8) = 13 is a different quantity — it counts leaves, not calls.)\n\n"
                "**Trap:** confusing the return value with the call count, or forgetting the '+1' for the "
                "current call. Memoisation would cut the calls to O(n)."
            ),
            "verify": '''
calls = [0]
def g(n):
    calls[0] += 1
    return 1 if n <= 2 else g(n - 1) + g(n - 3)
g(8)
assert calls[0] == int(ANSWER) and OUTPUT.strip() == "13"
''',
        },
        # ---------------------------------------------------------------- Q11
        {
            "type": "MCQ", "marks": 2, "topic": "Python — class vs instance attributes",
            "text": "What is printed by the following Python program?",
            "code": '''class C:
    items = []
    count = 0

    def add(self, x):
        self.items.append(x)
        self.count += 1

a, b = C(), C()
a.add(1)
b.add(2)
a.add(3)
print(len(C.items), a.count, b.count, C.count)''',
            "options": ["`2 2 1 0`", "`3 3 3 3`", "`3 2 1 0`", "`3 2 1 3`"],
            "answer": "C",
            "solution": (
                "**Concept.** Attribute *lookup* `self.x` searches the instance first, then the class. "
                "Attribute *assignment* `self.x = …` always creates/updates an **instance** attribute.\n\n"
                "- `self.items.append(x)` only *reads* `self.items` (finding the class's single list) and "
                "mutates it — all instances share that list.\n"
                "- `self.count += 1` means `self.count = self.count + 1`: the read finds C.count = 0 the first "
                "time, but the write creates an instance attribute, shadowing the class attribute from then "
                "on. C.count itself is never changed.\n\n"
                "**Trace.**\n"
                "- a.add(1): C.items = [1]; a.count = 0 + 1 = 1 (new instance attribute).\n"
                "- b.add(2): C.items = [1, 2]; b.count = 1.\n"
                "- a.add(3): C.items = [1, 2, 3]; a.count = 2.\n\n"
                "Output: `3 2 1 0`.\n\n"
                "**Options.**\n"
                "- (A) assumes each instance has its own `items`, yet counts them together.\n"
                "- (B) assumes `count` is shared like `items`.\n"
                "- (D) assumes `+=` updated the class attribute.\n\n"
                "**Trap:** mutable class attributes are shared state — initialise per-instance lists in "
                "`__init__`."
            ),
            "verify": "assert OUTPUT.strip() == '3 2 1 0' and ANSWER == 'C'",
        },
        # ---------------------------------------------------------------- Q12
        {
            "type": "NAT", "marks": 2, "topic": "Stacks — monotonic stack (stock span)",
            "text": ("The **span** of day i in a price list P is the number of consecutive days ending at day i "
                     "(including day i) whose price is ≤ P[i]. It is computed with a stack of indices: for each "
                     "i, pop while the price at the stack top is ≤ P[i]; then span = i + 1 if the stack is empty, "
                     "otherwise i − (top index); finally push i. For\n\n"
                     "P = [31, 27, 29, 35, 22, 24, 30, 40, 26]\n\n"
                     "the sum of all nine spans is ______."),
            "diagrams": [{"type": "array", "values": [31, 27, 29, 35, 22, 24, 30, 40, 26], "label": "P"}],
            "answer": "23",
            "solution": (
                "**Concept.** The stack keeps indices of a strictly decreasing sequence of prices; the element "
                "below day i after popping is the previous day with a *higher* price. Each index is pushed and "
                "popped at most once → O(n) total.\n\n"
                "**Trace** (stack shown as indices, prices in brackets):\n"
                "- i=0 (31): empty → span 1; push 0. Stack [0]\n"
                "- i=1 (27): top 31 > 27 → span 1−0 = 1; push. [0, 1]\n"
                "- i=2 (29): pop 1 (27); top 0 (31) → span 2; push. [0, 2]\n"
                "- i=3 (35): pop 2, pop 0 → empty → span 4; push. [3]\n"
                "- i=4 (22): span 1; push. [3, 4]\n"
                "- i=5 (24): pop 4; top 3 → span 2; push. [3, 5]\n"
                "- i=6 (30): pop 5; top 3 → span 3; push. [3, 6]\n"
                "- i=7 (40): pop 6, pop 3 → empty → span 8; push. [7]\n"
                "- i=8 (26): top 40 → span 1. [7, 8]\n\n"
                "Spans: 1, 1, 2, 4, 1, 2, 3, 8, 1 → sum = **23**.\n\n"
                "**Trap:** stopping at the first smaller price to the left (that would be the 'previous "
                "smaller element' problem); the span stops at the first strictly *greater* price."
            ),
            "verify": '''
P = [31, 27, 29, 35, 22, 24, 30, 40, 26]
tot = 0
for i in range(len(P)):
    k = i
    while k >= 0 and P[k] <= P[i]: k -= 1
    tot += i - k
assert tot == int(ANSWER)
''',
        },
        # ---------------------------------------------------------------- Q13
        {
            "type": "MSQ", "marks": 2, "topic": "Heaps — possible positions of keys",
            "text": ("The seven keys 1, 2, 3, 4, 5, 6, 7 are stored in an array-based binary **min**-heap "
                     "H[0..6] (children of index i are 2i + 1 and 2i + 2). Considering **all** valid min-heaps "
                     "on these keys, which of the following statements is/are TRUE?"),
            "diagrams": [{"type": "heap", "values": ["H0", "H1", "H2", "H3", "H4", "H5", "H6"],
                          "caption": "Index layout of a 7-element heap"}],
            "options": [
                "Key 7 is always at one of the indices 3, 4, 5, 6",
                "Key 3 can be at an index of depth 2 (indices 3–6)",
                "Key 2 can be at index 3",
                "Key 6 can be at index 2",
            ],
            "answer": ["A", "B"],
            "solution": (
                "**Concept.** In a min-heap every key is smaller than all keys in its subtree. So a key at a "
                "node whose subtree has s nodes needs at least s − 1 larger keys; and a key can be at depth d "
                "only if its d ancestors are all smaller than it.\n\n"
                "- (A) **True.** 7 is the maximum; if it had a child, the child would have to be larger. So 7 "
                "is at a leaf, i.e. index 3–6.\n"
                "- (B) **True.** Depth 2 needs two smaller ancestors: 1 (root) and 2. Example heap "
                "[1, 2, 4, 3, 5, 6, 7] — 3 is at index 3, child of 2.\n"
                "- (C) **False.** 2 can only have the ancestor 1, so it must be at depth ≤ 1 — in fact it "
                "must be a child of the root (index 1 or 2), since its parent must be 1.\n"
                "- (D) **False.** Index 2 roots a subtree of 3 nodes, so the key there needs 2 larger keys; "
                "only 7 is larger than 6.\n\n"
                "**Fact:** there are exactly 80 distinct min-heaps on 7 distinct keys — enumerating them "
                "confirms (A) and (B) and refutes (C) and (D).\n\n"
                "**Trap:** assuming the k-th smallest must be at depth k − 1 or at depth ⌊log₂ k⌋; the k-th "
                "smallest can be anywhere from depth 1 down to depth k − 1."
            ),
            "verify": '''
import itertools
heaps = [p for p in itertools.permutations(range(1, 8))
         if all(p[(i - 1) // 2] < p[i] for i in range(1, 7))]
assert len(heaps) == 80
r = {'A': all(h.index(7) >= 3 for h in heaps),
     'B': any(h.index(3) >= 3 for h in heaps),
     'C': any(h.index(2) == 3 for h in heaps),
     'D': any(h.index(6) == 2 for h in heaps)}
assert sorted(k for k in r if r[k]) == sorted(ANSWER)
''',
        },
        # ---------------------------------------------------------------- Q14
        {
            "type": "MSQ", "marks": 2, "topic": "Quicksort — Hoare partition",
            "text": ("The Hoare partition below is called as `hoare(A, 0, 8)` on "
                     "A = [6, 11, 3, 9, 2, 8, 5, 1, 10]. Which of the following statements is/are TRUE?"),
            "code": '''def hoare(A, lo, hi):
    p = A[lo]
    i, j = lo - 1, hi + 1
    while True:
        i += 1
        while A[i] < p:
            i += 1
        j -= 1
        while A[j] > p:
            j -= 1
        if i >= j:
            return j
        A[i], A[j] = A[j], A[i]''',
            "run_code": False,
            "options": [
                "The function returns 3",
                "Exactly 3 swaps are performed",
                "After the call, the pivot value 6 is at index 3",
                "After the call, every element of A[0..3] is ≤ every element of A[4..8]",
            ],
            "answer": ["A", "B", "D"],
            "solution": (
                "**Concept.** Hoare's scheme moves i right to an element ≥ pivot and j left to an element ≤ "
                "pivot, swaps them, and repeats until the pointers cross. It returns j such that "
                "A[lo..j] ≤ pivot ≤ A[j+1..hi] — but, unlike Lomuto, it does **not** put the pivot in its "
                "final place.\n\n"
                "**Trace** (pivot 6):\n"
                "- i → 0 (6 ≥ 6), j → 7 (1 ≤ 6): swap → [1, 11, 3, 9, 2, 8, 5, 6, 10] (swap 1)\n"
                "- i → 1 (11), j → 6 (5): swap → [1, 5, 3, 9, 2, 8, 11, 6, 10] (swap 2)\n"
                "- i → 2 (3 < 6) → 3 (9); j → 5 (8 > 6) → 4 (2): swap → [1, 5, 3, 2, 9, 8, 11, 6, 10] (swap 3)\n"
                "- i → 4 (9); j → 3 (2). i ≥ j → return **3**.\n\n"
                "- (A) **True.**\n- (B) **True.**\n"
                "- (C) **False** — 6 ended at index 7; index 3 holds 2.\n"
                "- (D) **True** — left part {1, 5, 3, 2} (max 5), right part {9, 8, 11, 6, 10} (min 6).\n\n"
                "**Trap:** recursing on (lo, j − 1) and (j + 1, hi) as with Lomuto is a bug for Hoare; the "
                "correct calls are (lo, j) and (j + 1, hi)."
            ),
            "verify": '''
def hoare(A, lo, hi):
    global SW
    p = A[lo]; i, j = lo - 1, hi + 1
    while True:
        i += 1
        while A[i] < p: i += 1
        j -= 1
        while A[j] > p: j -= 1
        if i >= j: return j
        A[i], A[j] = A[j], A[i]; SW += 1
SW = 0
A = [6, 11, 3, 9, 2, 8, 5, 1, 10]
q = hoare(A, 0, 8)
r = {'A': q == 3, 'B': SW == 3, 'C': A[3] == 6,
     'D': max(A[:q + 1]) <= min(A[q + 1:])}
assert sorted(k for k in r if r[k]) == sorted(ANSWER)
''',
        },
        # ---------------------------------------------------------------- Q15
        {
            "type": "MCQ", "marks": 2, "topic": "Binary search — rotated arrays (buggy variant)",
            "text": ("The function below is intended to return the minimum of a sorted array of distinct keys "
                     "that has been rotated by an unknown amount. What does the program print?"),
            "code": '''def find_min(A):
    lo, hi = 0, len(A) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if A[mid] >= A[lo]:
            lo = mid + 1
        else:
            hi = mid
    return A[lo]

print(find_min([15, 18, 22, 3, 6, 9, 12]),
      find_min([7, 9, 11, 2, 5]),
      find_min([2, 4, 6, 8, 10]))''',
            "options": ["`3 2 2`", "`3 5 10`", "`3 2 10`", "`22 5 10`"],
            "answer": "B",
            "solution": (
                "**Concept.** The correct algorithm compares A[mid] with A[**hi**]: if A[mid] > A[hi] the "
                "minimum is right of mid, otherwise it is at mid or to its left. Comparing with A[lo] fails "
                "because 'A[mid] ≥ A[lo]' is also true when the range [lo, hi] is already sorted (unrotated), "
                "and it lets lo jump past the minimum.\n\n"
                "**Trace 1** [15, 18, 22, 3, 6, 9, 12]: (0,6) mid 3: 3 ≥ 15? no → hi 3; (0,3) mid 1: 18 ≥ 15 → "
                "lo 2; (2,3) mid 2: 22 ≥ 22 → lo 3; return **3** (correct by luck).\n\n"
                "**Trace 2** [7, 9, 11, 2, 5]: (0,4) mid 2: 11 ≥ 7 → lo 3; (3,4) mid 3: 2 ≥ 2 (mid = lo!) → "
                "lo 4; return **5** — wrong, the minimum 2 was skipped.\n\n"
                "**Trace 3** [2, 4, 6, 8, 10] (rotation 0): every test A[mid] ≥ A[lo] succeeds, lo keeps "
                "moving right; return **10** — the maximum!\n\n"
                "Output: `3 5 10`.\n\n"
                "**Options.** (A) is what a correct implementation prints; (C) and (D) mix correct and "
                "incorrect traces.\n\n"
                "**Trap:** when lo = mid, the test A[mid] ≥ A[lo] is trivially true — a classic off-by-one "
                "hazard in binary-search variants."
            ),
            "verify": '''
assert OUTPUT.strip() == "3 5 10" and ANSWER == 'B'
def good(A):
    lo, hi = 0, len(A) - 1
    while lo < hi:
        m = (lo + hi) // 2
        if A[m] > A[hi]: lo = m + 1
        else: hi = m
    return A[lo]
assert [good(X) for X in ([15, 18, 22, 3, 6, 9, 12], [7, 9, 11, 2, 5],
                          [2, 4, 6, 8, 10])] == [3, 2, 2]
''',
        },
        # ---------------------------------------------------------------- Q16
        {
            "type": "NAT", "marks": 2, "topic": "Graph theory — cut vertices",
            "text": ("A vertex of a connected undirected graph is a **cut vertex** (articulation point) if "
                     "deleting it together with its incident edges disconnects the graph. The number of cut "
                     "vertices in the graph below is ______."),
            "diagrams": [{"type": "graph", "directed": False,
                          "nodes": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
                          "edges": [["A", "B"], ["B", "C"], ["C", "A"], ["C", "D"], ["D", "E"],
                                    ["E", "F"], ["F", "D"], ["D", "G"], ["G", "H"], ["H", "I"],
                                    ["I", "G"], ["F", "J"]],
                          "pos": {"A": [0, 3], "B": [0, 1], "C": [1.5, 2], "D": [3, 2], "E": [4.2, 3.4],
                                  "F": [5.4, 2], "J": [7, 2], "G": [3, 0.3], "H": [2.2, -1.2],
                                  "I": [3.8, -1.2]}}],
            "answer": "4",
            "solution": (
                "**Concept.** A vertex is a cut vertex iff some pair of other vertices has all its connecting "
                "paths passing through it. Vertices inside a cycle are protected by the alternative route "
                "around the cycle; vertices where blocks (cycles/bridges) meet are cut vertices.\n\n"
                "**Structure.** Blocks: triangle ABC, bridge CD, triangle DEF, bridge DG, triangle GHI, "
                "bridge FJ.\n\n"
                "**Check each vertex.**\n"
                "- C: removing it separates {A, B} from the rest → **cut**.\n"
                "- D: separates {A, B, C}, {E, F, J} and {G, H, I} → **cut**.\n"
                "- F: separates J → **cut**.\n"
                "- G: separates {H, I} → **cut**.\n"
                "- A, B, E, H, I: each lies on a triangle with two other vertices that stay connected; J is a "
                "leaf. Removing any of them leaves the graph connected.\n\n"
                "Cut vertices: C, D, F, G → **4**. (The bridges are CD, DG and FJ.)\n\n"
                "**Trap:** a leaf (J) is never a cut vertex — but its neighbour (F) always is, if the graph has "
                "more than two vertices. E is not a cut vertex even though it looks 'central' in the drawing."
            ),
            "verify": '''
E = ["AB", "BC", "CA", "CD", "DE", "EF", "FD", "DG", "GH", "HI", "IG", "FJ"]
G = {}
for a, b in E:
    G.setdefault(a, set()).add(b); G.setdefault(b, set()).add(a)
def connected_without(x):
    vs = [v for v in G if v != x]; seen = {vs[0]}; st = [vs[0]]
    while st:
        u = st.pop()
        for w in G[u]:
            if w != x and w not in seen: seen.add(w); st.append(w)
    return len(seen) == len(vs)
assert sum(not connected_without(v) for v in G) == int(ANSWER)
''',
        },
        # ---------------------------------------------------------------- Q17
        {
            "type": "NAT", "marks": 2, "topic": "Shortest paths — counting shortest weighted paths",
            "text": ("In the weighted directed graph below, the number of distinct shortest paths from S to T "
                     "is ______."),
            "diagrams": [{"type": "graph", "directed": True,
                          "nodes": ["S", "A", "B", "C", "D", "E", "T"],
                          "edges": [["S", "A", 2], ["S", "B", 3], ["A", "C", 3], ["B", "C", 2],
                                    ["A", "D", 4], ["C", "D", 1], ["C", "E", 2], ["D", "T", 2],
                                    ["E", "T", 1], ["B", "E", 6]],
                          "pos": {"S": [0, 2], "A": [2, 3.5], "B": [2, 0.5], "C": [4, 2], "D": [6, 3.5],
                                  "E": [6, 0.5], "T": [8, 2]}}],
            "answer": "5",
            "solution": (
                "**Concept.** Compute distances d(·) (Dijkstra), then count paths along tight edges only "
                "(d(u) + w = d(v)), processing vertices in increasing order of d: "
                "ways(v) = ∑ ways(u) over tight edges (u, v).\n\n"
                "**Distances.** S 0; A 2; B 3; C = min(2 + 3, 3 + 2) = 5; D = min(2 + 4, 5 + 1) = 6; "
                "E = min(5 + 2, 3 + 6) = 7; T = min(6 + 2, 7 + 1) = 8.\n\n"
                "**Counting.**\n"
                "- ways(A) = 1, ways(B) = 1.\n"
                "- C: tight from A (2+3) and B (3+2) → 2.\n"
                "- D: tight from A (2+4 = 6) and C (5+1 = 6) → 1 + 2 = 3.\n"
                "- E: tight from C only (B→E gives 9) → 2.\n"
                "- T: tight from D (6+2) and E (7+1) → 3 + 2 = **5**.\n\n"
                "The five paths (all of length 8): S-A-D-T, S-A-C-D-T, S-B-C-D-T, S-A-C-E-T, S-B-C-E-T.\n\n"
                "**Trap:** Dijkstra's predecessor array stores only one parent per vertex, so reading paths off "
                "the shortest-path tree finds just one of the five."
            ),
            "verify": '''
import itertools
W = {("S", "A"): 2, ("S", "B"): 3, ("A", "C"): 3, ("B", "C"): 2, ("A", "D"): 4,
     ("C", "D"): 1, ("C", "E"): 2, ("D", "T"): 2, ("E", "T"): 1, ("B", "E"): 6}
paths = []
def walk(u, cost, path):
    if u == "T": paths.append(cost); return
    for (a, b), w in W.items():
        if a == u: walk(b, cost + w, path + [b])
walk("S", 0, ["S"])
assert paths.count(min(paths)) == int(ANSWER) and min(paths) == 8
''',
        },
        # ---------------------------------------------------------------- Q18
        {
            "type": "MCQ", "marks": 2, "topic": "Complexity — nested loops with geometric steps",
            "text": "The value returned by `f(n)` below, as a function of n, is",
            "code": '''def f(n):
    c = 0
    i = 1
    while i < n:
        j = i
        while j < n:
            j *= 2
            c += 1
        i *= 3
    return c''',
            "run_code": False,
            "options": ["Θ(log n)", "Θ(log² n)", "Θ(n)", "Θ(n log n)"],
            "answer": "B",
            "solution": (
                "**Concept.** Count iterations exactly, then sum.\n\n"
                "- The outer loop runs for i = 3⁰, 3¹, …, 3^{k} with 3^{k} < n, i.e. about log₃ n times.\n"
                "- For a given i = 3^{t}, the inner loop doubles j from i until j ≥ n: about "
                "log₂(n / 3^{t}) = log₂ n − t·log₂ 3 iterations.\n\n"
                "**Sum.** With L = log₂ n and K = log₃ n = L / log₂ 3:\n"
                "∑_{t=0}^{K} (L − t·log₂ 3) ≈ K·L − log₂ 3 · K²/2 = L²/log₂ 3 − L²/(2 log₂ 3) = "
                "L² / (2 log₂ 3) = Θ(log² n).\n\n"
                "(Numerically, f(2^{40}) = 537 and 537 / 40² ≈ 0.34, close to 1/(2 log₂ 3) ≈ 0.32.)\n\n"
                "**Options.**\n"
                "- (A) counts only the outer loop.\n"
                "- (C) would need the inner loop to be linear in i (e.g. `j += 1`).\n"
                "- (D) confuses this with a loop over all i from 1 to n.\n\n"
                "**Trap:** the inner loop's trip count shrinks as i grows, but only *linearly in t*, so the "
                "sum is still quadratic in log n (an arithmetic series)."
            ),
            "verify": '''
def f(n):
    c, i = 0, 1
    while i < n:
        j = i
        while j < n: j *= 2; c += 1
        i *= 3
    return c
r1 = f(2 ** 40) / 40 ** 2; r2 = f(2 ** 160) / 160 ** 2
assert 0.8 < r1 / r2 < 1.25
assert f(2 ** 160) / 160 > 3 * f(2 ** 40) / 40
assert ANSWER == 'B'
''',
        },
        # ---------------------------------------------------------------- Q19
        {
            "type": "MSQ", "marks": 2, "topic": "Python — string immutability and slicing",
            "text": ("Consider the following Python program (it prints nothing). Which of the following "
                     "statements is/are TRUE after it runs?"),
            "code": '''s = "data"
t = s
s += "base"
u = s[::-1][1::2]
k = s.find("a", 2)''',
            "options": [
                "`t == \"data\"`",
                "`u == \"sbtd\"`",
                "`k == 3`",
                "`s.count(\"a\") == 2`",
            ],
            "answer": ["A", "B", "C"],
            "solution": (
                "**Concept.** Strings are immutable: `s += \"base\"` builds a new string and rebinds s; t still "
                "refers to the old \"data\". Slices create new strings.\n\n"
                "- (A) **True** — t is untouched: \"data\".\n"
                "- (B) s = \"database\"; `s[::-1]` = \"esabatad\"; `[1::2]` takes indices 1, 3, 5, 7 → "
                "s, b, t, d → \"sbtd\". **True.**\n"
                "- (C) `s.find(\"a\", 2)` searches from index 2: d0 a1 **t2 a3** … → first 'a' at or after "
                "index 2 is at index 3. **True.**\n"
                "- (D) \"database\" contains 'a' at indices 1, 3, 5 → count 3. **False.**\n\n"
                "**Trap:** contrasting with lists — had s been a list, `s += [...]` would mutate in place and t "
                "would see the change (compare Q1 of this paper)."
            ),
            "verify": '''
r = {'A': t == "data", 'B': u == "sbtd", 'C': k == 3, 'D': s.count("a") == 2}
assert sorted(x for x in r if r[x]) == sorted(ANSWER)
''',
        },
        # ---------------------------------------------------------------- Q20
        {
            "type": "MCQ", "marks": 2, "topic": "Graph representations — BFS from an adjacency matrix",
            "text": ("An undirected graph on vertices 0–6 is given by the adjacency matrix below. How many "
                     "vertices are at shortest-path distance **exactly 2** from vertex 0?"),
            "diagrams": [{"type": "matrix", "title": "Adjacency matrix M",
                          "row_labels": ["0", "1", "2", "3", "4", "5", "6"],
                          "col_labels": ["0", "1", "2", "3", "4", "5", "6"],
                          "rows": [[0, 1, 0, 0, 1, 0, 0], [1, 0, 1, 0, 0, 0, 1], [0, 1, 0, 1, 0, 0, 0],
                                   [0, 0, 1, 0, 0, 1, 0], [1, 0, 0, 0, 0, 1, 0], [0, 0, 0, 1, 1, 0, 1],
                                   [0, 1, 0, 0, 0, 1, 0]]}],
            "options": ["2", "3", "4", "5"],
            "answer": "B",
            "solution": (
                "**Concept.** Run BFS from 0, reading neighbours of u from row u of the matrix (Θ(V) per "
                "vertex, Θ(V²) total).\n\n"
                "**Adjacency (from rows).** 0: {1, 4}; 1: {0, 2, 6}; 2: {1, 3}; 3: {2, 5}; 4: {0, 5}; "
                "5: {3, 4, 6}; 6: {1, 5}.\n\n"
                "**BFS levels.**\n"
                "- Level 0: {0}\n"
                "- Level 1: {1, 4}\n"
                "- Level 2: from 1 → 2, 6; from 4 → 5 → {2, 5, 6}\n"
                "- Level 3: from 2 → 3 (5's neighbour 3 is also level 3) → {3}\n\n"
                "Vertices at distance exactly 2: 2, 5, 6 → **3**.\n\n"
                "**Options.** (A) misses 5 (reached via 4). (C) counts every vertex not adjacent to 0 (2, 3, 5, "
                "6), but 3 needs three edges. (D) counts all vertices within distance ≤ 2 (1, 4, 2, 5, 6).\n\n"
                "**Alternative view:** (M²)[0][v] > 0 means a walk of length 2 from 0 to v exists; "
                "the vertices at distance exactly 2 are those with (M²)[0][v] > 0, M[0][v] = 0 and v ≠ 0."
            ),
            "solution_diagrams": [{"type": "graph", "directed": False,
                                   "nodes": ["0", "1", "2", "3", "4", "5", "6"],
                                   "edges": [["0", "1"], ["0", "4"], ["1", "2"], ["1", "6"], ["2", "3"],
                                             ["3", "5"], ["4", "5"], ["5", "6"]],
                                   "highlight": ["2", "5", "6"],
                                   "pos": {"0": [0, 2], "1": [2, 3], "4": [2, 1], "2": [4, 4],
                                           "6": [4, 2], "5": [4, 0], "3": [6, 2]},
                                   "caption": "The graph; distance-2 vertices highlighted"}],
            "verify": '''
M = [[0, 1, 0, 0, 1, 0, 0], [1, 0, 1, 0, 0, 0, 1], [0, 1, 0, 1, 0, 0, 0],
     [0, 0, 1, 0, 0, 1, 0], [1, 0, 0, 0, 0, 1, 0], [0, 0, 0, 1, 1, 0, 1],
     [0, 1, 0, 0, 0, 1, 0]]
from collections import deque
d = {0: 0}; q = deque([0])
while q:
    u = q.popleft()
    for v in range(7):
        if M[u][v] and v not in d: d[v] = d[u] + 1; q.append(v)
c = sum(1 for v in d if d[v] == 2)
assert ["2", "3", "4", "5"]["ABCD".index(ANSWER)] == str(c)
''',
        },
    ],
}
