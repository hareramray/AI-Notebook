# Set 21 — Counting & Structure of Trees

SET = {
    "number": 21,
    "title": "Counting & Structure of Trees",
    "difficulty": "GATE-level",
    "focus": "number of BSTs/binary trees, complete/full trees, height bounds",
    "questions": [
        # ------------------------------------------------------------ Q1
        {
            "type": "NAT", "marks": 1, "topic": "Counting BSTs with a fixed root",
            "text": ("The number of distinct binary search trees that can be formed with the keys "
                     "1, 2, 3, 4, 5, 6 and whose **root is 3** is ______."),
            "answer": "10",
            "solution": (
                "In a BST the root splits the keys: everything smaller goes to the left subtree, "
                "everything larger to the right, and the two subtrees can be chosen independently. "
                "The number of BSTs on m keys is the Catalan number C_{m} = (2m)! / ((m+1)! m!): "
                "C_{0} = 1, C_{1} = 1, C_{2} = 2, C_{3} = 5, C_{4} = 14, C_{5} = 42.\n\n"
                "- Root 3 → left subtree on {1, 2} (2 keys): C_{2} = 2 shapes.\n"
                "- Right subtree on {4, 5, 6} (3 keys): C_{3} = 5 shapes.\n\n"
                "Total = 2 × 5 = **10**.\n\n"
                "Sanity check: summing over all six roots gives C_{0}C_{5} + C_{1}C_{4} + C_{2}C_{3} + "
                "C_{3}C_{2} + C_{4}C_{1} + C_{5}C_{0} = 42 + 14 + 10 + 10 + 14 + 42 = 132 = C_{6}.\n\n"
                "**Trap:** adding instead of multiplying (2 + 5 = 7) — the choices for the two "
                "subtrees are independent, so the counts multiply."
            ),
            "verify": '''
def bsts(keys):
    if not keys: return [None]
    out = []
    for i, r in enumerate(keys):
        for L in bsts(keys[:i]):
            for R in bsts(keys[i + 1:]): out.append((r, L, R))
    return out
allt = bsts([1, 2, 3, 4, 5, 6])
assert len(allt) == 132
assert sum(1 for t in allt if t[0] == 3) == int(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q2
        {
            "type": "MCQ", "marks": 1, "topic": "Binary trees — node-degree counting",
            "text": ("A binary tree has 20 leaves and exactly 9 nodes that have exactly one child. "
                     "The total number of nodes in the tree is"),
            "options": ["47", "48", "39", "57"],
            "answer": "B",
            "solution": (
                "Let n₀, n₁, n₂ be the numbers of nodes with 0, 1, 2 children. Counting edges two ways: "
                "every node except the root has one parent edge, so n − 1 = n₁ + 2n₂, and "
                "n = n₀ + n₁ + n₂. Subtracting gives the key identity **n₀ = n₂ + 1**.\n\n"
                "- n₂ = n₀ − 1 = 20 − 1 = 19.\n"
                "- n = n₀ + n₁ + n₂ = 20 + 9 + 19 = **48** → (B).\n\n"
                "Check with edges: n − 1 = 47 = n₁ + 2n₂ = 9 + 38. ✓\n\n"
                "Option analysis:\n\n"
                "- (A) 47 is the number of edges, not nodes.\n"
                "- (C) 39 ignores the one-child nodes (20 + 19).\n"
                "- (D) 57 uses n₂ = n₀ + n₁ − 1 = 28 (wrong identity) giving 20 + 9 + 28.\n\n"
                "**Tip:** the number of one-child nodes never affects n₂; it just adds to n."
            ),
            "verify": '''
n0, n1 = 20, 9; n2 = n0 - 1; n = n0 + n1 + n2
assert n - 1 == n1 + 2 * n2 and n == 48 and ANSWER == "B"
''',
        },
        # ------------------------------------------------------------ Q3
        {
            "type": "MCQ", "marks": 1, "topic": "Python — recursion on a tuple-encoded tree",
            "text": ("A binary tree is encoded as nested tuples `(value, left, right)`. Consider the "
                     "following Python program. What is printed?"),
            "code": '''def f(t, d=0):
    if t is None:
        return 0
    v, l, r = t
    return v * d + f(l, d + 1) + f(r, d + 1)

T = (5, (3, None, (4, None, None)),
        (8, (7, None, None), None))
print(f(T), f(T, 1))''',
            "options": ["`33 55`", "`27 60`", "`33 60`", "`60 93`"],
            "answer": "C",
            "solution": (
                "`f(t, d)` returns ∑ value × (d + depth of the node), i.e. a depth-weighted sum where "
                "the root is given weight d.\n\n"
                "Depths: 5 at 0; 3 and 8 at 1; 4 and 7 at 2.\n\n"
                "- f(T) (d = 0): 5·0 + 3·1 + 8·1 + 4·2 + 7·2 = 0 + 3 + 8 + 8 + 14 = 33.\n"
                "- f(T, 1): every weight is one larger, so the result increases by the sum of all "
                "values 5 + 3 + 8 + 4 + 7 = 27: 33 + 27 = 60.\n\n"
                "Output `33 60` → (C).\n\n"
                "- (A) adds only 22 (forgets the root's own contribution 5·1).\n"
                "- (B) prints the plain sum of values 27 for the first call.\n"
                "- (D) shifts both calls by one level.\n\n"
                "**Tip:** f(T, d + 1) − f(T, d) always equals the sum of all values — a quick "
                "consistency check."
            ),
            "verify": "assert OUTPUT.strip() == '33 60' and ANSWER == 'C'",
        },
        # ------------------------------------------------------------ Q4
        {
            "type": "MSQ", "marks": 1, "topic": "Height bounds and complete binary trees",
            "text": ("Height is the number of **edges** on the longest root-to-leaf path. Which of the "
                     "following statements is/are TRUE?"),
            "options": [
                "Every binary tree with 50 nodes has height at least 5",
                "A complete binary tree with 50 nodes has exactly 25 leaves",
                "A complete binary tree with 50 nodes has exactly one node with exactly one child",
                "Inserting 50 distinct keys into an empty BST can produce a tree of height 50",
            ],
            "answer": ["A", "B", "C"],
            "solution": (
                "A binary tree of height h has at most 2^{h+1} − 1 nodes, so n nodes force "
                "h ≥ ⌈log₂(n + 1)⌉ − 1.\n\n"
                "- (A) Height 4 allows at most 31 nodes < 50, height 5 allows 63. So h ≥ 5. **TRUE.**\n"
                "- (B) In the array layout (0-indexed) node i has a child iff 2i + 1 < n, i.e. "
                "i ≤ 24. So nodes 0 … 24 are internal and 25 … 49 are leaves: 25 leaves "
                "(⌈n/2⌉ in general). **TRUE.**\n"
                "- (C) Node 24 has left child 49 but no right child (index 50 does not exist); every "
                "other internal node has two children. Exactly one node with one child (n even). **TRUE.**\n"
                "- (D) A degenerate BST (sorted insertion) is a path of 50 nodes, which has **49** "
                "edges. Height 50 is impossible. **FALSE.**\n\n"
                "**Trap:** mixing up height in edges vs nodes — 50 is the height counted in nodes."
            ),
            "verify": '''
n = 50
h = 0
while 2 ** (h + 1) - 1 < n: h += 1
leaves = sum(1 for i in range(n) if 2 * i + 1 >= n)
one = sum(1 for i in range(n) if 2 * i + 1 < n <= 2 * i + 2)
assert h == 5 and leaves == 25 and one == 1
assert sorted(ANSWER) == ["A", "B", "C"]
''',
        },
        # ------------------------------------------------------------ Q5
        {
            "type": "NAT", "marks": 1, "topic": "Stacks — postfix evaluation",
            "text": ("The postfix expression below is evaluated with an operand stack (for a binary "
                     "operator, the first value popped is the **right** operand; `/` is exact "
                     "division and all intermediate results here are integers):\n\n"
                     "`7 3 - 2 4 * 5 - * 12 6 / 3 + +`\n\n"
                     "The value of the expression is ______."),
            "answer": "17",
            "solution": (
                "Scan left to right: push operands; for an operator pop b (right) then a (left) "
                "and push a op b.\n\n"
                "- 7, 3 → [7, 3]; `-` → 7 − 3 = 4 → [4]\n"
                "- 2, 4 → [4, 2, 4]; `*` → 8 → [4, 8]\n"
                "- 5 → [4, 8, 5]; `-` → 8 − 5 = 3 → [4, 3]\n"
                "- `*` → 4 × 3 = 12 → [12]\n"
                "- 12, 6 → [12, 12, 6]; `/` → 2 → [12, 2]\n"
                "- 3 → [12, 2, 3]; `+` → 5 → [12, 5]\n"
                "- `+` → 17 → [17]\n\n"
                "Value = **17**. (The stack never holds more than 3 values.)\n\n"
                "The expression tree's infix form is ((7 − 3) × (2 × 4 − 5)) + (12 / 6 + 3).\n\n"
                "**Trap:** popping in the wrong order gives 3 − 7 = −4 and 6/12, producing a "
                "completely different value."
            ),
            "verify": '''
st = []
for tok in "7 3 - 2 4 * 5 - * 12 6 / 3 + +".split():
    if tok in "+-*/":
        b = st.pop(); a = st.pop()
        st.append({"+": a + b, "-": a - b, "*": a * b, "/": a / b}[tok])
    else: st.append(int(tok))
assert st == [int(ANSWER)]
''',
        },
        # ------------------------------------------------------------ Q6
        {
            "type": "MCQ", "marks": 1, "topic": "Queues — Python deque operations",
            "text": "Consider the following Python program. What is printed?",
            "code": '''from collections import deque
d = deque([1, 2, 3, 4, 5])
d.rotate(2)
d.appendleft(d.pop())
d.extend([6, 7])
d.rotate(-3)
x = d.popleft() + d.pop()
print(list(d), x)''',
            "options": ["`[2, 6, 7, 3, 4] 6`", "`[1, 6, 7, 2, 3] 9`",
                        "`[6, 7, 3, 4, 5] 3`", "`[2, 6, 7, 3, 4] 8`"],
            "answer": "A",
            "solution": (
                "`rotate(k)` with k > 0 moves the last k elements to the front (right rotation); "
                "k < 0 rotates left. `pop()` removes from the right, `popleft()` from the left.\n\n"
                "- Start: [1, 2, 3, 4, 5]\n"
                "- rotate(2): [4, 5, 1, 2, 3]\n"
                "- appendleft(pop()): pop() = 3 → [3, 4, 5, 1, 2]\n"
                "- extend([6, 7]): [3, 4, 5, 1, 2, 6, 7]\n"
                "- rotate(−3): [1, 2, 6, 7, 3, 4, 5]\n"
                "- x = popleft() + pop() = 1 + 5 = 6 → d = [2, 6, 7, 3, 4]\n\n"
                "Output `[2, 6, 7, 3, 4] 6` → (A).\n\n"
                "- (B) treats rotate(2) as a left rotation.\n"
                "- (C) treats rotate(−3) as a right rotation.\n"
                "- (D) has the right deque but adds 1 + 7 (the last element before the rotate).\n\n"
                "**Tip:** a right rotation by k of length n equals a left rotation by n − k."
            ),
            "verify": "assert OUTPUT.strip() == '[2, 6, 7, 3, 4] 6' and ANSWER == 'A'",
        },
        # ------------------------------------------------------------ Q7
        {
            "type": "NAT", "marks": 1, "topic": "Hashing — quadratic probing",
            "text": ("The keys 22, 33, 14, 44, 25, 3, 36 are inserted in that order into an initially "
                     "empty table of 11 slots using quadratic probing: the i-th probe (i = 0, 1, 2, …) "
                     "for key k examines slot (k mod 11 + i²) mod 11. The index of the slot in which "
                     "36 is stored is ______."),
            "answer": "6",
            "solution": (
                "Quadratic probing visits h, h + 1, h + 4, h + 9, h + 16, h + 25, … (mod 11), so keys "
                "with the same home slot follow the same probe sequence (secondary clustering).\n\n"
                "- 22 → h = 0 → slot 0.\n"
                "- 33 → h = 0 occupied; 0 + 1 = 1 → slot 1.\n"
                "- 14 → h = 3 → slot 3.\n"
                "- 44 → h = 0: 0, 1 occupied; 0 + 4 = 4 → slot 4.\n"
                "- 25 → h = 3: 3, 4 occupied; 3 + 4 = 7 → slot 7.\n"
                "- 3 → h = 3: 3, 4, 7 occupied; 3 + 9 = 12 ≡ 1 occupied; 3 + 16 = 19 ≡ 8 → slot 8.\n"
                "- 36 → h = 3: probes 3, 4, 7, 1, 8 all occupied; 3 + 25 = 28 ≡ **6** → slot 6.\n\n"
                "36 needs 6 probes even though the table is only about half full — the keys 14, 25, "
                "3, 36 all share home slot 3 and hence the same probe sequence.\n\n"
                "**Trap:** using linear steps (h + i) would put 36 in slot 5."
            ),
            "solution_diagrams": [{"type": "hashtable", "size": 11,
                                   "slots": {0: 22, 1: 33, 3: 14, 4: 44, 6: 36, 7: 25, 8: 3},
                                   "caption": "Final table"}],
            "verify": '''
T = [None] * 11
for k in [22, 33, 14, 44, 25, 3, 36]:
    i = 0
    while T[(k % 11 + i * i) % 11] is not None: i += 1
    T[(k % 11 + i * i) % 11] = k
assert T.index(36) == int(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q8
        {
            "type": "MCQ", "marks": 1, "topic": "Binary search — decision tree structure",
            "text": ("Binary search with `mid = (lo + hi) // 2` (three-way comparison at each probe, "
                     "counted as one comparison) is performed on a sorted array of 20 distinct keys, "
                     "once for each key in the array. For how many of the 20 keys does the "
                     "successful search use **exactly 5** comparisons?"),
            "options": ["4", "5", "6", "8"],
            "answer": "B",
            "solution": (
                "The probes made by binary search form a *decision tree*: the first mid is the root, "
                "the left/right halves are its subtrees, and a key found at depth d needs d + 1 "
                "comparisons. Because the halves differ in size by at most one at every step, this "
                "tree is balanced: all levels except the last are full.\n\n"
                "- Depth 0: 1 key (1 comparison)\n"
                "- Depth 1: 2 keys (2 comparisons)\n"
                "- Depth 2: 4 keys (3)\n"
                "- Depth 3: 8 keys (4)\n"
                "- Depth 4: the remaining 20 − 15 = **5** keys (5 comparisons)\n\n"
                "So 5 keys need exactly 5 comparisons → (B). (Average successful cost = "
                "(1 + 4 + 12 + 32 + 25)/20 = 3.7.)\n\n"
                "- (A) and (C) are off by one in the level counts.\n"
                "- (D) is the size of the last full level (depth 3).\n\n"
                "**Tip:** for n keys, the worst case is ⌊log₂ n⌋ + 1 = 5 and the number of keys on "
                "the last level is n − (2^{⌊log₂ n⌋} − 1)."
            ),
            "verify": '''
from collections import Counter
cnt = Counter()
for key in range(20):
    lo, hi, c = 0, 19, 0
    while lo <= hi:
        m = (lo + hi) // 2; c += 1
        if m == key: break
        if m < key: lo = m + 1
        else: hi = m - 1
    cnt[c] += 1
assert cnt[5] == 5 and ANSWER == "B"
''',
        },
        # ------------------------------------------------------------ Q9
        {
            "type": "MCQ", "marks": 1, "topic": "Bubble sort — number of swaps",
            "text": ("Bubble sort (repeatedly swapping adjacent out-of-order elements until no swap "
                     "occurs) is used to sort [3, 7, 1, 8, 2, 6] into ascending order. "
                     "The total number of swaps performed is"),
            "options": ["5", "6", "7", "8"],
            "answer": "C",
            "solution": (
                "Each adjacent swap of an out-of-order pair removes **exactly one** inversion, and the "
                "algorithm stops when no inversions remain. Therefore #swaps = #inversions, no matter "
                "in which order the passes visit the pairs.\n\n"
                "Inversions of [3, 7, 1, 8, 2, 6]:\n\n"
                "- 3 > 1, 2 → 2\n"
                "- 7 > 1, 2, 6 → 3\n"
                "- 1 → 0\n"
                "- 8 > 2, 6 → 2\n"
                "- 2 → 0\n\n"
                "Total = **7** → (C).\n\n"
                "Pass-by-pass check: pass 1 swaps (7,1), (8,2), (8,6) → [3, 1, 7, 2, 6, 8]; pass 2 "
                "swaps (3,1), (7,2), (7,6) → [1, 3, 2, 6, 7, 8]; pass 3 swaps (3,2) → sorted. "
                "3 + 3 + 1 = 7.\n\n"
                "- (A), (B), (D) come from counting passes or comparisons instead of swaps.\n\n"
                "**Tip:** insertion sort also performs exactly #inversions shifts."
            ),
            "verify": '''
a = [3, 7, 1, 8, 2, 6]; sw = 0; ch = True
while ch:
    ch = False
    for j in range(len(a) - 1):
        if a[j] > a[j + 1]: a[j], a[j + 1] = a[j + 1], a[j]; sw += 1; ch = True
assert sw == 7 and ANSWER == "C"
''',
        },
        # ------------------------------------------------------------ Q10
        {
            "type": "MSQ", "marks": 1, "topic": "Graph theory — trees",
            "text": ("G is a **connected** simple undirected graph with 10 vertices and 9 edges. "
                     "Which of the following statements is/are TRUE for every such G?"),
            "options": [
                "G contains no cycle",
                "G has at least two vertices of degree 1",
                "The sum of the degrees of the vertices of G is 20",
                "G has a vertex of degree at least 3",
            ],
            "answer": ["A", "B"],
            "solution": (
                "A connected graph on n vertices with n − 1 edges is a **tree** (connected + n − 1 "
                "edges ⇔ connected + acyclic).\n\n"
                "- (A) Trees are acyclic. **TRUE.**\n"
                "- (B) Every tree with n ≥ 2 vertices has at least two leaves: the two endpoints of a "
                "longest path cannot have any other neighbour (that would extend the path or close a "
                "cycle). **TRUE.**\n"
                "- (C) ∑deg = 2|E| = 18, not 20. **FALSE.**\n"
                "- (D) The path P₁₀ is a tree with maximum degree 2. **FALSE.**\n\n"
                "Extra: since ∑deg = 18 = 2(n − 1), the average degree is 1.8 < 2, which is "
                "another way to see that some vertices must have degree 1.\n\n"
                "**Trap:** confusing |E| = n − 1 with |E| = n (which would give 20 in (C) and force a cycle)."
            ),
            "verify": '''
n, m = 10, 9
assert 2 * m == 18 != 20
path = {i: [j for j in (i - 1, i + 1) if 0 <= j < n] for i in range(n)}
assert max(len(v) for v in path.values()) == 2
assert sum(1 for v in path.values() if len(v) == 1) >= 2
assert sorted(ANSWER) == ["A", "B"]
''',
        },
        # ------------------------------------------------------------ Q11
        {
            "type": "NAT", "marks": 2, "topic": "Counting BSTs of maximum height",
            "text": ("Height is measured in edges. The number of distinct binary search trees on the "
                     "keys 1, 2, …, 7 that have height exactly 6 is ______."),
            "answer": "64",
            "solution": (
                "Height 6 with 7 nodes means the tree is a **path**: every node except the last has "
                "exactly one child.\n\n"
                "Build the path from the root downward. At each step the current node splits the "
                "remaining keys into smaller and larger ones; for the tree to stay a path, all "
                "remaining keys must lie on one side, so the current node must be the **minimum or "
                "the maximum** of the keys still remaining.\n\n"
                "- Root: 2 choices (1 or 7).\n"
                "- Each of the next nodes: again min or max of what remains → 2 choices.\n"
                "- The last node (one key left): 1 choice.\n\n"
                "Total = 2^{6} = **64** (in general 2^{n−1} BSTs of height n − 1).\n\n"
                "Example: root 7 → 1 → 2 → 6 → 3 → 5 → 4 is valid (the zig-zag path), while root 4 "
                "is impossible because both sides would be non-empty.\n\n"
                "These are exactly the shapes produced by the 2^{n−1} insertion orders in which every "
                "inserted key is the current min or max of the not-yet-inserted keys.\n\n"
                "**Trap:** answering 2 (only the two sorted orders) or 7! / something — zig-zag "
                "paths count too."
            ),
            "verify": '''
def bsts(keys):
    if not keys: return [None]
    out = []
    for i, r in enumerate(keys):
        for L in bsts(keys[:i]):
            for R in bsts(keys[i + 1:]): out.append((r, L, R))
    return out
def h(t): return -1 if t is None else 1 + max(h(t[1]), h(t[2]))
assert sum(1 for t in bsts(list(range(1, 8))) if h(t) == 6) == int(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q12
        {
            "type": "NAT", "marks": 2, "topic": "Counting binary trees by height (Python DP)",
            "text": ("The function `c(n, h)` below counts binary trees (shapes) with n nodes and "
                     "height at most h, where height is in edges and the empty tree has height −1. "
                     "The value printed is ______."),
            "code": '''from functools import lru_cache

@lru_cache(None)
def c(n, h):
    if n == 0:
        return 1
    if h < 0:
        return 0
    return sum(c(k, h - 1) * c(n - 1 - k, h - 1)
               for k in range(n))

print(c(7, 3) - c(7, 2))''',
            "answer": "68",
            "solution": (
                "`c(7, 3) − c(7, 2)` is the number of 7-node binary trees of height **exactly 3**.\n\n"
                "- c(7, 2) = 1: height ≤ 2 holds at most 7 nodes, so only the perfect tree qualifies.\n"
                "- c(7, 3): root + a left subtree of k nodes and a right subtree of 6 − k nodes, each "
                "of height ≤ 2.\n\n"
                "First tabulate a(m) = c(m, 2) (trees with m nodes and height ≤ 2) and b(m) = c(m, 1):\n\n"
                "- b(0..3) = 1, 1, 2, 1 (height ≤ 1 holds at most 3 nodes).\n"
                "- a(m) = ∑_{k} b(k) b(m−1−k): a(0) = 1, a(1) = 1, a(2) = 2, a(3) = 5, a(4) = 6, "
                "a(5) = 6, a(6) = 4, a(7) = 1.\n\n"
                "Then c(7, 3) = ∑_{k=0..6} a(k) a(6−k) = 1·4 + 1·6 + 2·6 + 5·5 + 6·2 + 6·1 + 4·1 "
                "= 4 + 6 + 12 + 25 + 12 + 6 + 4 = 69.\n\n"
                "Answer = 69 − 1 = **68**.\n\n"
                "Sanity checks: a(3) = 5 = C₃ (all 3-node trees have height ≤ 2); a(4) = 6 because "
                "of the C₄ = 14 four-node trees, 8 are paths of height 3.\n\n"
                "**Trap:** forgetting that the empty subtree (k = 0) is allowed — its count is 1, "
                "not 0 — which drops the k = 0 and k = 6 terms."
            ),
            "verify": '''
import itertools
def shapes(n):
    if n == 0: return [None]
    return [(L, R) for k in range(n) for L in shapes(k) for R in shapes(n - 1 - k)]
def ht(t): return -1 if t is None else 1 + max(ht(t[0]), ht(t[1]))
assert sum(1 for t in shapes(7) if ht(t) == 3) == int(ANSWER) == int(OUTPUT)
''',
        },
        # ------------------------------------------------------------ Q13
        {
            "type": "MCQ", "marks": 2, "topic": "Tree reconstruction from traversals",
            "text": ("A binary tree with nine distinct labels has\n"
                     "pre-order: G, C, A, E, K, J, H, B, F\n"
                     "in-order: A, E, C, K, G, H, J, F, B\n"
                     "Its post-order traversal is"),
            "options": [
                "A, E, K, C, H, F, B, J, G",
                "E, A, K, C, F, B, H, J, G",
                "E, A, K, C, H, F, B, J, G",
                "E, A, C, K, H, B, F, J, G",
            ],
            "answer": "C",
            "solution": (
                "The first pre-order element is the root; its position in the in-order sequence "
                "splits the remaining labels into left and right subtrees. Recurse.\n\n"
                "- Root G. In-order left of G: A, E, C, K; right: H, J, F, B.\n"
                "- Left subtree: pre-order C, A, E, K → root C; in-order A, E | C | K → left {A, E}, "
                "right {K}. In {A, E}: pre-order A, E → root A; in-order A, E → E is A's **right** child.\n"
                "- Right subtree: pre-order J, H, B, F → root J; in-order H | J | F, B → left {H}, right "
                "{F, B}. In {F, B}: pre-order B, F → root B; in-order F, B → F is B's **left** child.\n\n"
                "Post-order (left, right, root): E, A, K, C | H, F, B, J | G → (C).\n\n"
                "Option analysis:\n\n"
                "- (A) lists A before its child E — a parent always follows its children in post-order.\n"
                "- (B) visits J's right subtree (F, B) before its left child H.\n"
                "- (C) **Correct.**\n"
                "- (D) puts C before K, but K is in C's subtree, and B before F.\n\n"
                "**Tip:** the last post-order element must equal the first pre-order element (G); "
                "use such checks to eliminate options quickly."
            ),
            "solution_diagrams": [{"type": "bintree",
                                   "tree": ["G", ["C", ["A", None, ["E"]], ["K"]],
                                            ["J", ["H"], ["B", ["F"], None]]],
                                   "caption": "Reconstructed tree"}],
            "verify": '''
def build(pre, ino):
    if not pre: return None
    r = pre[0]; i = ino.index(r)
    return (r, build(pre[1:i + 1], ino[:i]), build(pre[i + 1:], ino[i + 1:]))
def post(t): return [] if t is None else post(t[1]) + post(t[2]) + [t[0]]
t = build(list("GCAEKJHBF"), list("AECKGHJFB"))
assert post(t) == list("EAKCHFBJG") and ANSWER == "C"
''',
        },
        # ------------------------------------------------------------ Q14
        {
            "type": "MSQ", "marks": 2, "topic": "Heaps — array layout of a complete tree",
            "text": ("A binary max-heap stores 100 **distinct** keys in an array A[0 … 99] (children "
                     "of index i at 2i + 1 and 2i + 2; depth of the root is 0). Which of the following "
                     "statements is/are TRUE?"),
            "options": [
                "The children of index 24 are at indices 49 and 50",
                "The deepest level (depth 6) contains exactly 36 keys",
                "Index 49 holds a leaf",
                "Depending on the keys, the minimum key can be at any of exactly 50 indices, and at no other index",
            ],
            "answer": ["A", "D"],
            "solution": (
                "In a complete tree with n = 100 nodes, depths 0 … 5 are full (1 + 2 + … + 32 = 63 nodes) "
                "and the remaining 37 nodes sit on depth 6. Node i is internal iff 2i + 1 ≤ n − 1 = 99, "
                "i.e. i ≤ 49.\n\n"
                "- (A) 2·24 + 1 = 49 and 2·24 + 2 = 50. **TRUE.**\n"
                "- (B) Depth 6 contains 100 − 63 = **37** keys, not 36. **FALSE.**\n"
                "- (C) Index 49 has a left child at 99 (but no right child, since 100 is out of range). "
                "It is an internal node. **FALSE.**\n"
                "- (D) In a max-heap every internal node is larger than its child, so the minimum must "
                "be a leaf: indices 50 … 99, i.e. 50 positions. Conversely each leaf can hold the "
                "minimum (no ordering constraint between a leaf and other leaves). **TRUE.**\n\n"
                "**Trap:** in (C), index 49 has exactly one child — the unique one-child node of a "
                "complete tree with an even number of nodes — so it is *not* a leaf."
            ),
            "solution_diagrams": [{"type": "matrix", "title": "Nodes per depth for n = 100",
                                   "col_labels": ["0", "1", "2", "3", "4", "5", "6"],
                                   "row_labels": ["nodes"],
                                   "rows": [[1, 2, 4, 8, 16, 32, 37]]}],
            "verify": '''
n = 100
depth = lambda i: (i + 1).bit_length() - 1
assert sum(1 for i in range(n) if depth(i) == 6) == 37
assert (2 * 24 + 1, 2 * 24 + 2) == (49, 50) and 2 * 49 + 1 < n
leaves = [i for i in range(n) if 2 * i + 1 >= n]
assert leaves == list(range(50, 100))
assert sorted(ANSWER) == ["A", "D"]
''',
        },
        # ------------------------------------------------------------ Q15
        {
            "type": "NAT", "marks": 2, "topic": "Counting insertion orders that yield a BST",
            "text": ("The number of distinct orderings of the keys {20, 30, 35, 40, 50, 70, 80} which, "
                     "when inserted one by one into an initially empty binary search tree, produce "
                     "exactly the BST shown below is ______."),
            "diagrams": [{"type": "bintree",
                          "tree": [50, [30, [20], [40, [35], None]], [70, None, [80]]],
                          "caption": "Target BST"}],
            "answer": "45",
            "solution": (
                "An insertion order produces a given BST iff every node is inserted **before all of its "
                "descendants**. Equivalently, the root comes first, and the orders for the left and "
                "right subtrees can be interleaved arbitrarily. So\n"
                "N(T) = C(|L| + |R|, |L|) × N(L) × N(R).\n\n"
                "- Subtree 40 (child 35): 40 must precede 35 → N = 1.\n"
                "- Subtree 30: left {20} (size 1), right {40, 35} (size 2) → C(3, 1) × 1 × 1 = 3.\n"
                "- Subtree 70 (child 80): N = 1.\n"
                "- Root 50: left size 4, right size 2 → C(6, 2) × 3 × 1 = 15 × 3 = **45**.\n\n"
                "Check by the hook-length style formula: N = n! / ∏(subtree sizes) = "
                "7! / (7 · 4 · 1 · 2 · 1 · 2 · 1) = 5040 / 112 = 45. ✓\n\n"
                "**Trap:** counting only the interleavings at the root (15) and forgetting the factor 3 "
                "from the 30-subtree, or treating the order within each subtree as free (giving "
                "6!/(…) too large)."
            ),
            "verify": '''
import itertools
def ins(t, k):
    if t is None: return (k, None, None)
    v, l, r = t
    return (v, ins(l, k), r) if k < v else (v, l, ins(r, k))
def build(seq):
    t = None
    for k in seq: t = ins(t, k)
    return t
target = build([50, 30, 70, 20, 40, 80, 35])
cnt = sum(1 for p in itertools.permutations([20, 30, 35, 40, 50, 70, 80]) if build(p) == target)
assert cnt == int(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q16
        {
            "type": "MCQ", "marks": 2, "topic": "Quicksort — comparisons via the recursion tree",
            "text": ("Consider the following quicksort, which uses the first element as the pivot and "
                     "builds the two partitions with list comprehensions (preserving relative order). "
                     "Each call on a list of length m is charged m − 1 comparisons. "
                     "What is printed?"),
            "code": '''cmp = 0

def qs(a):
    global cmp
    if len(a) <= 1:
        return a
    p = a[0]
    cmp += len(a) - 1
    lo = [x for x in a[1:] if x < p]
    hi = [x for x in a[1:] if x > p]
    return qs(lo) + [p] + qs(hi)

qs([5, 3, 8, 1, 4, 7, 9, 2, 6])
print(cmp)''',
            "options": ["13", "16", "21", "36"],
            "answer": "B",
            "solution": (
                "With the first element as pivot and order-preserving partitions, the pivots of the "
                "recursive calls form exactly the **BST obtained by inserting the input in order** "
                "5, 3, 8, 1, 4, 7, 9, 2, 6. A call whose pivot is node v handles v's whole subtree, "
                "charging (subtree size − 1). Summing over all nodes, each key is charged once per "
                "proper ancestor, so\n"
                "total comparisons = ∑ depth(v) = internal path length of the BST.\n\n"
                "BST: 5 → left 3 (left 1 → right 2; right 4), right 8 (left 7 → left 6; right 9).\n\n"
                "- Depth 1: 3, 8 → 2\n"
                "- Depth 2: 1, 4, 7, 9 → 8\n"
                "- Depth 3: 2, 6 → 6\n\n"
                "Total = 2 + 8 + 6 = **16** → (B).\n\n"
                "Call-by-call: [9 keys] 8, [3,1,4,2] 3, [1,2] 1, [8,7,9,6] 3, [7,6] 1 → 8 + 3 + 1 + 3 + 1 = 16.\n\n"
                "- (A) 13 is impossible: any 9-node binary tree has internal path length at least "
                "0 + 1·2 + 2·4 + 3·2 = 16, so this input is in fact a best case.\n"
                "- (C) 21 charges m instead of m − 1 for each of the 5 calls with m ≥ 2.\n"
                "- (D) 36 = 9·8/2 is the worst case (sorted input).\n\n"
                "**Tip:** quicksort's comparison count and BST-insertion cost are the same random "
                "variable — which is why both average Θ(n log n)."
            ),
            "solution_diagrams": [{"type": "bintree",
                                   "tree": [5, [3, [1, None, [2]], [4]], [8, [7, [6], None], [9]]],
                                   "caption": "Recursion tree of pivots (= BST of the input order)"}],
            "verify": '''
assert OUTPUT.strip() == "16" and ANSWER == "B"
def ins(t, k):
    if t is None: return [k, None, None]
    if k < t[0]: t[1] = ins(t[1], k)
    else: t[2] = ins(t[2], k)
    return t
t = None
for k in [5, 3, 8, 1, 4, 7, 9, 2, 6]: t = ins(t, k)
def ipl(t, d=0): return 0 if t is None else d + ipl(t[1], d + 1) + ipl(t[2], d + 1)
assert ipl(t) == 16
''',
        },
        # ------------------------------------------------------------ Q17
        {
            "type": "MSQ", "marks": 2, "topic": "Dijkstra — shortest-path tree",
            "text": ("Dijkstra's algorithm is run from S on the weighted undirected graph below. "
                     "Which of the following statements is/are TRUE?"),
            "diagrams": [{"type": "graph", "directed": False,
                          "nodes": ["S", "A", "B", "C", "D", "E", "F"],
                          "edges": [["S", "A", 3], ["S", "B", 6], ["A", "B", 2], ["A", "C", 7],
                                    ["B", "C", 4], ["B", "D", 9], ["C", "D", 1], ["C", "E", 6],
                                    ["D", "F", 3], ["E", "F", 2], ["D", "E", 4]],
                          "pos": {"S": [0, 1], "A": [1.5, 2], "B": [1.5, 0], "C": [3, 2],
                                  "D": [3, 0], "E": [4.5, 2], "F": [4.5, 0]}}],
            "options": [
                "The shortest-path distance from S to F is 13",
                "The edge A–B belongs to the shortest-path tree",
                "E is finalised (extracted) before F",
                "The shortest-path tree has exactly two leaves",
            ],
            "answer": ["A", "B", "D"],
            "solution": (
                "Run Dijkstra (tentative distances updated on extraction):\n\n"
                "- S (0): A = 3, B = 6.\n"
                "- A (3): B = min(6, 5) = 5 (parent A), C = 10.\n"
                "- B (5): C = min(10, 9) = 9 (parent B), D = 14.\n"
                "- C (9): D = min(14, 10) = 10 (parent C), E = 15.\n"
                "- D (10): F = 13, E = min(15, 14) = 14 (parent D).\n"
                "- F (13): E = min(14, 15) = 14 (unchanged).\n"
                "- E (14).\n\n"
                "Final: S 0, A 3, B 5, C 9, D 10, F 13, E 14. Tree edges: S–A, A–B, B–C, C–D, D–F, D–E.\n\n"
                "- (A) d(F) = 13. **TRUE.**\n"
                "- (B) B's parent is A (3 + 2 = 5 < 6). **TRUE.**\n"
                "- (C) F (13) is extracted before E (14). **FALSE.**\n"
                "- (D) The tree is the path S–A–B–C–D with two branches F and E hanging off D: leaves "
                "are E and F only. **TRUE.**\n\n"
                "**Trap:** taking the direct edges S–B (6) or C–E (6) at face value; both are improved "
                "by longer, cheaper routes."
            ),
            "solution_diagrams": [{"type": "graph", "directed": False,
                                   "nodes": ["S", "A", "B", "C", "D", "E", "F"],
                                   "edges": [["S", "A", 3], ["S", "B", 6], ["A", "B", 2], ["A", "C", 7],
                                             ["B", "C", 4], ["B", "D", 9], ["C", "D", 1], ["C", "E", 6],
                                             ["D", "F", 3], ["E", "F", 2], ["D", "E", 4]],
                                   "pos": {"S": [0, 1], "A": [1.5, 2], "B": [1.5, 0], "C": [3, 2],
                                           "D": [3, 0], "E": [4.5, 2], "F": [4.5, 0]},
                                   "highlight_edges": [["S", "A"], ["A", "B"], ["B", "C"], ["C", "D"],
                                                       ["D", "F"], ["D", "E"]],
                                   "caption": "Shortest-path tree (highlighted)"}],
            "verify": '''
import heapq
E = [("S","A",3),("S","B",6),("A","B",2),("A","C",7),("B","C",4),("B","D",9),
     ("C","D",1),("C","E",6),("D","F",3),("E","F",2),("D","E",4)]
G = {}
for u, v, w in E: G.setdefault(u, []).append((v, w)); G.setdefault(v, []).append((u, w))
d = {v: 10 ** 9 for v in G}; d["S"] = 0; par = {}; pq = [(0, "S")]; order = []
while pq:
    du, u = heapq.heappop(pq)
    if u in order: continue
    order.append(u)
    for v, w in G[u]:
        if du + w < d[v]: d[v] = du + w; par[v] = u; heapq.heappush(pq, (d[v], v))
assert d["F"] == 13 and par["B"] == "A" and order.index("F") < order.index("E")
leaves = [v for v in G if v not in par.values()]
assert sorted(leaves) == ["E", "F"]
assert sorted(ANSWER) == ["A", "B", "D"]
''',
        },
        # ------------------------------------------------------------ Q18
        {
            "type": "MSQ", "marks": 2, "topic": "Merge sort — shape of the recursion tree",
            "text": ("Top-down merge sort is called on an array of n = 37 elements. Each call on a "
                     "subarray of length m ≥ 2 makes two recursive calls on lengths ⌊m/2⌋ and ⌈m/2⌉ "
                     "and then one merge; a call on length 1 returns immediately. Consider the "
                     "recursion tree (one node per call; the root is at depth 0). "
                     "Which of the following statements is/are TRUE?"),
            "options": [
                "The recursion tree has exactly 73 nodes",
                "The recursion tree has height 5",
                "Exactly 27 of the length-1 calls occur at depth 5",
                "Exactly 18 of the merges combine two runs of equal length",
            ],
            "answer": ["A", "C"],
            "solution": (
                "The tree is a full binary tree whose leaves are the n length-1 calls, so it has "
                "n − 1 = 36 internal nodes (merges) and 2n − 1 nodes. Splitting into ⌊m/2⌋ and ⌈m/2⌉ keeps "
                "all leaves within two consecutive depths, ⌊log₂ n⌋ and ⌈log₂ n⌉.\n\n"
                "- (A) 2 · 37 − 1 = 73. **TRUE.**\n"
                "- (B) 2^{5} = 32 < 37, so some length-2 calls still exist at depth 5 and their "
                "children lie at depth 6 = ⌈log₂ 37⌉. Height 6. **FALSE.**\n"
                "- (C) Depth 5 has 32 nodes (all depths ≤ 5 are full). Let x of them have length 2; "
                "then the 32 sizes add to 37, so x = 5. Those 5 calls create 10 leaves at depth 6, "
                "and the other 32 − 5 = **27** depth-5 calls are leaves. **TRUE.**\n"
                "- (D) Equal-length merges happen exactly at the internal calls with **even** m. "
                "Sizes by depth: 37 | 18, 19 | 9, 9, 9, 10 | 4,5 ×3 and 5,5 | … Counting all internal "
                "calls with even m gives 21, not 18. **FALSE.**\n\n"
                "**Trap:** assuming the tree for 37 elements has height ⌊log₂ 37⌋ = 5 — the leftover "
                "length-2 subarrays add one more level."
            ),
            "solution_diagrams": [{"type": "matrix", "title": "Calls per depth (n = 37)",
                                   "col_labels": ["0", "1", "2", "3", "4", "5", "6"],
                                   "row_labels": ["calls", "leaves"],
                                   "rows": [[1, 2, 4, 8, 16, 32, 10],
                                            [0, 0, 0, 0, 0, 27, 10]]}],
            "verify": '''
from collections import Counter
acc = []
def rec(n, d):
    acc.append((n, d))
    if n > 1: rec(n // 2, d + 1); rec(n - n // 2, d + 1)
rec(37, 0)
assert len(acc) == 73 and max(d for _, d in acc) == 6
lv = Counter(d for n, d in acc if n == 1)
assert lv[5] == 27 and lv[6] == 10
assert sum(1 for n, d in acc if n > 1 and n % 2 == 0) == 21
per = Counter(d for _, d in acc); assert [per[i] for i in range(7)] == [1, 2, 4, 8, 16, 32, 10]
assert sorted(ANSWER) == ["A", "C"]
''',
        },
        # ------------------------------------------------------------ Q19
        {
            "type": "MCQ", "marks": 2, "topic": "Building a balanced BST from a sorted array",
            "text": "Consider the following Python program. What is printed?",
            "code": '''def build(a, lo, hi):
    if lo > hi:
        return None
    m = (lo + hi + 1) // 2
    return (a[m], build(a, lo, m - 1),
            build(a, m + 1, hi))

def pre(t):
    if t is None:
        return []
    return [t[0]] + pre(t[1]) + pre(t[2])

a = list(range(10, 101, 10))
print(pre(build(a, 0, len(a) - 1)))''',
            "options": [
                "`[50, 20, 10, 30, 40, 80, 60, 70, 90, 100]`",
                "`[60, 30, 20, 10, 50, 40, 90, 80, 70, 100]`",
                "`[60, 30, 20, 10, 40, 50, 90, 80, 70, 100]`",
                "`[60, 30, 10, 20, 50, 40, 90, 70, 80, 100]`",
            ],
            "answer": "B",
            "solution": (
                "`m = (lo + hi + 1) // 2` picks the **upper** middle of each range. The result is a "
                "height-balanced BST; pre-order lists each root before its subtrees.\n\n"
                "a = [10, 20, …, 100], indices 0 … 9.\n\n"
                "- build(0, 9): m = 5 → 60; left = build(0, 4), right = build(6, 9).\n"
                "- build(0, 4): m = 2 → 30; left build(0, 1): m = 1 → 20 with left child 10; "
                "right build(3, 4): m = 4 → 50 with left child 40.\n"
                "- build(6, 9): m = 8 → 90; left build(6, 7): m = 7 → 80 with left child 70; "
                "right build(9, 9) → 100.\n\n"
                "Pre-order: 60, 30, 20, 10, 50, 40, 90, 80, 70, 100 → (B).\n\n"
                "- (A) is the result with the lower middle `(lo + hi) // 2`.\n"
                "- (C) lists 40 before its parent 50.\n"
                "- (D) makes 10 the parent of 20 (lower middle at one level only).\n\n"
                "The tree has height 3 (edges) = ⌈log₂ 11⌉ − 1, the minimum for 10 nodes.\n\n"
                "**Trap:** with an even-length range the choice of middle changes the whole shape."
            ),
            "solution_diagrams": [{"type": "bintree",
                                   "tree": [60, [30, [20, [10], None], [50, [40], None]],
                                            [90, [80, [70], None], [100]]],
                                   "caption": "Tree built with the upper middle"}],
            "verify": '''
assert OUTPUT.strip() == "[60, 30, 20, 10, 50, 40, 90, 80, 70, 100]" and ANSWER == "B"
def b2(a, lo, hi):
    if lo > hi: return None
    m = (lo + hi) // 2
    return (a[m], b2(a, lo, m - 1), b2(a, m + 1, hi))
assert pre(b2(a, 0, 9)) == [50, 20, 10, 30, 40, 80, 60, 70, 90, 100]
''',
        },
        # ------------------------------------------------------------ Q20
        {
            "type": "NAT", "marks": 2, "topic": "Linked lists — reversal in groups",
            "text": "Consider the following Python program. The value printed is ______.",
            "code": '''class N:
    def __init__(self, v, nxt=None):
        self.v, self.n = v, nxt

def rev_k(h, k):
    prev, cur, cnt = None, h, 0
    while cur and cnt < k:
        cur.n, prev, cur = prev, cur, cur.n
        cnt += 1
    if cur:
        h.n = rev_k(cur, k)
    return prev

head = None
for v in reversed([4, 9, 1, 7, 3, 8, 2, 5]):
    head = N(v, head)
head = rev_k(head, 3)
s = 0
while head:
    s = s * 10 + head.v
    head = head.n
print(s)''',
            "answer": "19483752",
            "solution": (
                "`rev_k` reverses the first k nodes in place, then (if nodes remain) recursively "
                "processes the rest and hangs it after the old first node `h`, which is now the "
                "last node of its group. A final short group is also reversed.\n\n"
                "The tuple assignment `cur.n, prev, cur = prev, cur, cur.n` is safe: the right side "
                "(old prev, old cur, old cur.n) is evaluated completely first, and the targets are "
                "then assigned left to right — `cur.n` is set while `cur` still names the old node.\n\n"
                "The list is 4 → 9 → 1 → 7 → 3 → 8 → 2 → 5. Groups of 3:\n\n"
                "- [4, 9, 1] → 1, 9, 4\n"
                "- [7, 3, 8] → 8, 3, 7\n"
                "- [2, 5] (short group) → 5, 2\n\n"
                "Result: 1 → 9 → 4 → 8 → 3 → 7 → 5 → 2, and the loop reads it as the decimal number "
                "**19483752**.\n\n"
                "**Traps:**\n\n"
                "- Leaving the final short group unreversed (LeetCode-style) would give 19483725.\n"
                "- Writing the assignment as `cur, cur.n, prev = cur.n, prev, cur` breaks the list: "
                "`cur` is rebound first, so `cur.n = prev` modifies the wrong node."
            ),
            "solution_diagrams": [{"type": "linkedlist", "values": [1, 9, 4, 8, 3, 7, 5, 2],
                                   "head": "head", "caption": "After rev_k(head, 3)"}],
            "verify": '''
xs = [4, 9, 1, 7, 3, 8, 2, 5]; ys = []
for i in range(0, len(xs), 3): ys += xs[i:i + 3][::-1]
assert int("".join(map(str, ys))) == int(ANSWER) and OUTPUT.strip() == ANSWER
''',
        },
    ],
}
