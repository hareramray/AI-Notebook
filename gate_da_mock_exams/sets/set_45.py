# Set 45 — Full-Syllabus Mock — Paper 15
SET = {
    "number": 45,
    "title": "Full-Syllabus Mock — Paper 15",
    "difficulty": "GATE-level",
    "focus": "balanced paper across the whole Section 4 syllabus",
    "questions": [
        # ------------------------------------------------------------ Q1
        {
            "type": "MCQ", "marks": 1, "topic": "Python — list replication and in-place +=",
            "text": "Consider the following Python program. What is printed?",
            "code": '''a = [[]] * 3
b = [[] for _ in range(3)]
a[0].append(1)
b[0].append(1)
a[1] += [2]
print(sum(map(len, a)), sum(map(len, b)))''',
            "options": [
                "`2 1`",
                "`3 1`",
                "`6 1`",
                "`4 1`",
            ],
            "answer": "C",
            "solution": (
                "**Concept.** `[[]] * 3` copies the *reference* three times: all three slots name "
                "one list object. A comprehension evaluates `[]` afresh for every element. For lists, "
                "`x += y` mutates x in place (like `extend`) and then rebinds the same object.\n\n"
                "- `a[0].append(1)`: the single shared list becomes [1]; a = [[1], [1], [1]].\n"
                "- `b[0].append(1)`: only b[0] changes; b = [[1], [], []].\n"
                "- `a[1] += [2]`: extends the shared list in place → [1, 2]; then stores that same "
                "object back into a[1]. All slots still alias it: a = [[1, 2], [1, 2], [1, 2]].\n\n"
                "Sums of lengths: a → 2 + 2 + 2 = 6; b → 1 + 0 + 0 = 1. Output `6 1` → (C).\n\n"
                "- (B) assumes `+=` creates a new list for a[1] only (true for tuples, not lists).\n"
                "- (A) counts only one copy of the shared list.\n"
                "- (D) treats a[1] as a separate list [1, 2] and the others as [1].\n\n"
                "**Trap:** `a[1] = a[1] + [2]` *would* create a new list and give 1 + 2 + 1 = 4 "
                "(option D) — `+=` and `+` differ for mutable sequences."
            ),
            "verify": '''
assert OUTPUT.strip() == '6 1'
x = [[]] * 3; x[0].append(1); x[1] = x[1] + [2]
assert sum(map(len, x)) == 4
''',
        },
        # ------------------------------------------------------------ Q2
        {
            "type": "NAT", "marks": 1, "topic": "Queues — deque operations in Python",
            "text": "Consider the following Python program. The value printed is ______.",
            "code": '''from collections import deque

d = deque(range(1, 8))
d.rotate(3)
d.appendleft(d.pop())
d.rotate(-2)
print(d[0] * 10 + d[-1])''',
            "answer": "65",
            "solution": (
                "**Concept.** `rotate(k)` with k > 0 moves the last k elements to the front (rotate "
                "right); k < 0 rotates left. `pop()` removes from the right end, `appendleft` adds "
                "at the left end.\n\n"
                "Trace:\n"
                "- start: [1, 2, 3, 4, 5, 6, 7]\n"
                "- rotate(3): [5, 6, 7, 1, 2, 3, 4]\n"
                "- pop() → 4; appendleft(4): [4, 5, 6, 7, 1, 2, 3]  (net effect: one more right "
                "rotation)\n"
                "- rotate(−2): [6, 7, 1, 2, 3, 4, 5]\n\n"
                "d[0] = 6, d[−1] = 5 → 6 × 10 + 5 = **65**.\n\n"
                "**Tip:** the whole sequence is a net right rotation by 3 + 1 − 2 = 2, which "
                "immediately gives [6, 7, 1, 2, 3, 4, 5].\n\n"
                "**Trap:** reading rotate(3) as a left rotation gives [4, 5, 6, 7, 1, 2, 3] and a "
                "different final answer."
            ),
            "solution_diagrams": [{"type": "queue", "values": [6, 7, 1, 2, 3, 4, 5],
                                   "caption": "Final deque (left end → right end)"}],
            "verify": '''
L = list(range(1, 8)); k = 2
L = L[-k:] + L[:-k]
assert L[0] * 10 + L[-1] == int(ANSWER) == int(OUTPUT)
''',
        },
        # ------------------------------------------------------------ Q3
        {
            "type": "MSQ", "marks": 1, "topic": "Trees — full binary trees",
            "text": ("A *full* binary tree is one in which every node has either 0 or 2 children. "
                     "Consider full binary trees with exactly 21 nodes (height = number of edges on "
                     "the longest root-to-leaf path). Which of the following statements is/are TRUE?"),
            "options": ["Every such tree has exactly 11 leaves",
                        "The minimum possible height is 4",
                        "The maximum possible height is 20",
                        "Every such tree has exactly 20 edges"],
            "answer": ["A", "B", "D"],
            "solution": (
                "**Concept.** In a full binary tree with i internal nodes, there are i + 1 leaves, "
                "so n = 2i + 1 is always odd. Height is extreme when the tree is as bushy or as "
                "stringy as possible.\n\n"
                "- (A) n = 21 = 2i + 1 → i = 10 internal nodes, 11 leaves. **True.**\n"
                "- (B) A tree of height h has at most 2^{h+1} − 1 nodes; h = 3 allows only 15 < 21, "
                "while h = 4 allows 31 ≥ 21 (and an odd count 21 is achievable). Minimum height 4. "
                "**True.**\n"
                "- (C) The tallest full tree is a 'caterpillar': each internal node has one leaf "
                "child and one internal child, adding one level per internal node → height = "
                "i = 10, not 20. **False.**\n"
                "- (D) Any tree with n nodes has n − 1 = 20 edges. **True.**\n\n"
                "**Trap:** height 20 would need a path of 21 nodes, each with one child — not "
                "allowed in a full binary tree."
            ),
            "verify": '''
from functools import lru_cache
@lru_cache(None)
def heights(n):
    if n == 1: return frozenset([0])
    hs = set()
    for l in range(1, n - 1, 2):
        r = n - 1 - l
        if r < 1 or r % 2 == 0: continue
        for a in heights(l):
            for b in heights(r): hs.add(1 + max(a, b))
    return frozenset(hs)
H = heights(21)
truth = {"A": (21 + 1) // 2 == 11, "B": min(H) == 4, "C": max(H) == 20, "D": 21 - 1 == 20}
assert max(H) == 10
assert sorted(k for k in truth if truth[k]) == sorted(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q4
        {
            "type": "NAT", "marks": 1, "topic": "Hashing — expected number of empty slots",
            "text": ("Eight keys are inserted into a hash table with 8 slots using separate chaining. "
                     "Assume simple uniform hashing (each key independently hashes to each slot with "
                     "probability 1/8). The expected number of slots that remain empty is ______ "
                     "(rounded off to two decimal places)."),
            "answer": ["2.74", "2.76"],
            "solution": (
                "**Concept.** Linearity of expectation: define an indicator X_{j} = 1 if slot j is "
                "empty. Then E[#empty] = ∑ P(slot j empty), and the slots need not be independent.\n\n"
                "- P(a given key misses slot j) = 7/8.\n"
                "- P(all 8 keys miss slot j) = (7/8)⁸ ≈ 0.3436.\n"
                "- E[#empty] = 8 × (7/8)⁸ ≈ 8 × 0.3436 = **2.75**.\n\n"
                "So even at load factor α = 1, about 34% of the slots stay empty "
                "(≈ e^{−1} for large tables), and some chains must therefore be longer than 1.\n\n"
                "**Trap:** answering 0 (\"8 keys fill 8 slots\") or using 1/8 instead of (7/8)⁸. "
                "No independence between slots is needed — expectation is linear."
            ),
            "verify": '''
from itertools import product
from fractions import Fraction
exact = 8 * Fraction(7, 8) ** 8
assert float(ANSWER[0]) <= float(exact) <= float(ANSWER[1])
''',
        },
        # ------------------------------------------------------------ Q5
        {
            "type": "MCQ", "marks": 1, "topic": "Insertion sort — counting comparisons",
            "text": ("Insertion sort is applied to [3, 1, 2, 6, 4, 5]. When inserting key = A[i], "
                     "it compares key with A[i−1], A[i−2], … moving larger elements right, and stops "
                     "at the first element ≤ key or at the front of the array. Every evaluation of "
                     "`A[j] > key` counts as one comparison. The total number of comparisons is"),
            "options": ["4", "8", "9", "15"],
            "answer": "B",
            "solution": (
                "**Concept.** Inserting A[i] costs (number of shifts) + 1 comparisons, except "
                "when the key travels all the way to the front, where the final failing "
                "comparison is replaced by the boundary check (no key comparison).\n\n"
                "Trace:\n"
                "- i = 1, key 1: 3 > 1 shift; reaches front → 1 comparison. [1, 3, 2, 6, 4, 5]\n"
                "- i = 2, key 2: 3 > 2 shift; 1 > 2? no → 2 comparisons. [1, 2, 3, 6, 4, 5]\n"
                "- i = 3, key 6: 3 > 6? no → 1 comparison.\n"
                "- i = 4, key 4: 6 > 4 shift; 3 > 4? no → 2 comparisons. [1, 2, 3, 4, 6, 5]\n"
                "- i = 5, key 5: 6 > 5 shift; 4 > 5? no → 2 comparisons.\n\n"
                "Total = 1 + 2 + 1 + 2 + 2 = **8** → (B).\n\n"
                "- (A) 4 is the number of shifts (= inversions).\n"
                "- (C) 9 = shifts + (n − 1) wrongly charges a comparison when 1 reaches the front.\n"
                "- (D) 15 = n(n − 1)/2 is the worst case.\n\n"
                "**Trap:** comparisons = inversions + (n − 1) − (number of keys that reach the "
                "front) = 4 + 5 − 1 = 8."
            ),
            "verify": '''
A = [3, 1, 2, 6, 4, 5]; c = 0
for i in range(1, len(A)):
    k, j = A[i], i - 1
    while j >= 0:
        c += 1
        if A[j] > k: A[j+1] = A[j]; j -= 1
        else: break
    A[j+1] = k
assert c == 8 and ANSWER == "B"
''',
        },
        # ------------------------------------------------------------ Q6
        {
            "type": "MCQ", "marks": 1, "topic": "Linked lists — cost of operations",
            "text": ("A singly linked list maintains pointers to both its first node (head) and its "
                     "last node (tail), and nothing else. Which of the following operations "
                     "**cannot** be performed in O(1) worst-case time on a list of n nodes?"),
            "diagrams": [{"type": "linkedlist", "values": [12, 7, 30, 4, 19], "head": "head",
                          "tail": "tail", "caption": "Singly linked list with head and tail"}],
            "options": ["Insert a new node before the first node",
                        "Insert a new node after the last node",
                        "Delete the first node",
                        "Delete the last node"],
            "answer": "D",
            "solution": (
                "**Concept.** An operation is O(1) only if every pointer that must change is "
                "reachable in O(1) steps from head or tail.\n\n"
                "- (A) new.next = head; head = new → O(1).\n"
                "- (B) tail.next = new; tail = new → O(1). (This is why a tail pointer makes a "
                "linked-list queue efficient.)\n"
                "- (C) head = head.next → O(1).\n"
                "- (D) Deleting the last node requires the **predecessor** of tail, so that its next "
                "can be set to None and tail moved to it. In a singly linked list the only way to "
                "find it is to walk from head: Θ(n). **Cannot be O(1).**\n\n"
                "Answer (D).\n\n"
                "**Tip:** a queue (enqueue at tail, dequeue at head) works in O(1) with this "
                "structure; a deque needing removal at both ends needs a doubly linked list.\n\n"
                "**Trap:** having a tail pointer helps insertion at the end, not deletion there."
            ),
        },
        # ------------------------------------------------------------ Q7
        {
            "type": "NAT", "marks": 1, "topic": "Graphs — DFS tree and back edges",
            "text": ("Depth-first search is run on a **connected** simple undirected graph with 12 "
                     "vertices and 20 edges. The number of edges that are **not** edges of the DFS "
                     "tree is ______."),
            "answer": "9",
            "solution": (
                "**Concept.** DFS from one vertex of a connected graph visits every vertex, and each "
                "newly discovered vertex adds exactly one tree edge. So the DFS tree is a spanning "
                "tree with n − 1 edges. In an undirected graph every remaining edge is a back edge "
                "(there are no forward/cross edges in undirected DFS).\n\n"
                "- Tree edges = n − 1 = 11.\n"
                "- Non-tree (back) edges = m − (n − 1) = 20 − 11 = **9**.\n\n"
                "The answer is independent of the start vertex and of the neighbour order — those "
                "change *which* edges are back edges, not how many.\n\n"
                "**Trap:** subtracting n (giving 8). Also note each back edge closes a distinct "
                "cycle with the tree: 9 is the cyclomatic number m − n + 1."
            ),
            "verify": '''
import random
random.seed(7)
n, m = 12, 20
for trial in range(20):
    edges = set((i, random.randrange(i)) for i in range(1, n))
    while len(edges) < m:
        u, v = random.sample(range(n), 2)
        if (u, v) not in edges and (v, u) not in edges: edges.add((u, v))
    adj = {i: [] for i in range(n)}
    for u, v in edges: adj[u].append(v); adj[v].append(u)
    seen, tree = {0}, 0
    def dfs(u):
        global tree
        for v in adj[u]:
            if v not in seen: seen.add(v); tree += 1; dfs(v)
    dfs(0)
    assert len(seen) == n and m - tree == int(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q8
        {
            "type": "MCQ", "marks": 1, "topic": "Complexity — halving loop nest",
            "text": "What is the time complexity of the following function in terms of n?",
            "code": '''def g(n):
    count = 0
    i = n
    while i > 0:
        for j in range(i):
            count += 1
        i //= 2
    return count''',
            "options": [
                "Θ(n log n)",
                "Θ(n)",
                "Θ(log n)",
                "Θ(n²)",
            ],
            "answer": "B",
            "solution": (
                "**Concept.** When the inner loop's length shrinks geometrically, the total work is "
                "a geometric series dominated by its first term.\n\n"
                "The outer loop runs with i = n, n/2, n/4, …, 1 (about log₂ n + 1 times), but the "
                "inner loop runs i times, so\n"
                "count = n + ⌊n/2⌋ + ⌊n/4⌋ + … + 1 < 2n.\n\n"
                "Hence Θ(n) → (B). For n = 1024: 1024 + 512 + … + 1 = 2047.\n\n"
                "- (A) multiplies the number of outer iterations (log n) by the *largest* inner "
                "loop (n) — a valid upper bound, but not tight.\n"
                "- (C) counts only the outer loop.\n"
                "- (D) would need the inner loop to run ~n times on every one of ~n iterations.\n\n"
                "**Trap:** 'two nested loops ⇒ at least n log n'. Always sum the actual inner "
                "lengths."
            ),
            "verify": '''
assert g(1024) == 2047 and g(1000) < 2000 and ANSWER == "B"
''',
        },
        # ------------------------------------------------------------ Q9
        {
            "type": "NAT", "marks": 1, "topic": "Linear search — expected comparisons",
            "text": ("Linear search scans an array of 6 distinct keys from position 1 to 6, making one "
                     "comparison per position examined, and stops when the key is found. The key "
                     "searched for is always present, and it is at position i with probability "
                     "proportional to i (i = 1, …, 6). The expected number of comparisons is ______ "
                     "(rounded off to two decimal places)."),
            "answer": ["4.32", "4.34"],
            "solution": (
                "**Concept.** If the key is at position i, the search makes exactly i comparisons, "
                "so E[comparisons] = ∑ i · P(i).\n\n"
                "- Normalising: P(i) = i / (1 + 2 + … + 6) = i / 21.\n"
                "- E = ∑ i · i/21 = (1 + 4 + 9 + 16 + 25 + 36)/21 = 91/21 ≈ **4.33**.\n\n"
                "Compare with the uniform case (P(i) = 1/6): E = (n + 1)/2 = 3.5. Because "
                "later positions are more likely here, the cost is higher.\n\n"
                "**Tip:** if the access probabilities are known, storing keys in **decreasing** "
                "order of probability minimises the expected cost — reversing this array would give "
                "∑ (7 − i) · i/21 = 56/21 ≈ 2.67.\n\n"
                "**Trap:** using ∑ i/6 or forgetting to normalise the probabilities."
            ),
            "verify": '''
from fractions import Fraction
E = sum(Fraction(i * i, 21) for i in range(1, 7))
assert E == Fraction(91, 21) and float(ANSWER[0]) <= float(E) <= float(ANSWER[1])
''',
        },
        # ------------------------------------------------------------ Q10
        {
            "type": "MCQ", "marks": 1, "topic": "Binary search trees — valid pre-order sequences",
            "text": ("Which of the following sequences can be the pre-order traversal of a binary "
                     "search tree with distinct keys?"),
            "options": ["30, 20, 10, 25, 40, 35, 50", "30, 20, 25, 10, 40",
                        "50, 30, 40, 35, 20", "15, 10, 20, 18, 12"],
            "answer": "A",
            "solution": (
                "**Concept.** In a BST pre-order, after the root r come all keys < r (left subtree) "
                "followed by all keys > r (right subtree), recursively. Equivalently, once a key "
                "larger than some ancestor-to-the-left appears, no later key may drop below that "
                "ancestor.\n\n"
                "- (A) 30 | 20, 10, 25 | 40, 35, 50. Left part: 20 | 10 | 25 ✓; right part: "
                "40 | 35 | 50 ✓. **Valid.**\n"
                "- (B) 30 | 20, 25, 10 | 40: inside the left part, 20 | (nothing smaller first) "
                "25, 10 — after 25 (> 20) we are in 20's right subtree, so 10 < 20 is illegal. "
                "**Invalid.**\n"
                "- (C) 50 | 30, 40, 35, 20: inside 30's subtree, 40 (> 30) starts the right "
                "subtree, so 20 < 30 cannot follow. **Invalid.**\n"
                "- (D) 15 | 10 | 20, 18, 12: after 20 (> 15) we are in 15's right subtree, so 12 < 15 "
                "is illegal. **Invalid.**\n\n"
                "Answer (A).\n\n"
                "**Tip:** a stack-based O(n) check keeps a running lower bound: pop while the "
                "top < current key, raising the bound to each popped value."
            ),
            "solution_diagrams": [{"type": "bintree",
                                   "tree": [30, [20, [10], [25]], [40, [35], [50]]],
                                   "caption": "BST with pre-order (A)"}],
            "verify": '''
def valid(seq):
    st, low = [], float('-inf')
    for x in seq:
        if x < low: return False
        while st and st[-1] < x: low = st.pop()
        st.append(x)
    return True
opts = {"A": [30,20,10,25,40,35,50], "B": [30,20,25,10,40], "C": [50,30,40,35,20],
        "D": [15,10,20,18,12]}
assert [k for k in opts if valid(opts[k])] == [ANSWER]
''',
        },
        # ------------------------------------------------------------ Q11
        {
            "type": "NAT", "marks": 2, "topic": "Python — counting recursive calls",
            "text": "Consider the following Python program. The value printed is ______.",
            "code": '''calls = 0

def f(n):
    global calls
    calls += 1
    if n < 3:
        return n
    return f(n - 1) + f(n - 3)

v = f(8)
print(calls)''',
            "answer": "25",
            "solution": (
                "**Concept.** Without memoisation every call spawns its sub-calls again. Let C(n) be "
                "the number of calls made by f(n), including itself: C(n) = 1 for n < 3, and "
                "C(n) = 1 + C(n − 1) + C(n − 3) otherwise.\n\n"
                "Table:\n"
                "- C(0) = C(1) = C(2) = 1\n"
                "- C(3) = 1 + C(2) + C(0) = 3\n"
                "- C(4) = 1 + C(3) + C(1) = 5\n"
                "- C(5) = 1 + C(4) + C(2) = 7\n"
                "- C(6) = 1 + C(5) + C(3) = 11\n"
                "- C(7) = 1 + C(6) + C(4) = 17\n"
                "- C(8) = 1 + C(7) + C(5) = **25**\n\n"
                "(For reference, f(8) itself returns 15.)\n\n"
                "**Trap:** computing the *value* recurrence f(n) instead of the *call-count* "
                "recurrence, or forgetting the '+1' for the call itself. Note that `global calls` is "
                "required — without it, `calls += 1` raises UnboundLocalError."
            ),
            "solution_diagrams": [{"type": "matrix", "title": "Call counts C(n)",
                                   "col_labels": ["0", "1", "2", "3", "4", "5", "6", "7", "8"],
                                   "row_labels": ["C(n)"],
                                   "rows": [[1, 1, 1, 3, 5, 7, 11, 17, 25]],
                                   "highlight": [[0, 8]]}],
            "verify": '''
from functools import lru_cache
@lru_cache(None)
def C(n): return 1 if n < 3 else 1 + C(n - 1) + C(n - 3)
assert C(8) == int(ANSWER) == int(OUTPUT) and v == 15
''',
        },
        # ------------------------------------------------------------ Q12
        {
            "type": "MSQ", "marks": 2, "topic": "Queues — input-restricted deque permutations",
            "text": ("The values 1, 2, 3, 4, 5 are inserted, in this order, at the **rear** of an "
                     "initially empty deque (no insertion at the front). Deletions may be made from "
                     "**either** end and may be interleaved arbitrarily with the insertions; each "
                     "deleted value is appended to an output sequence. Which of the following output "
                     "sequences is/are possible?"),
            "options": ["5, 1, 4, 2, 3", "5, 3, 1, 2, 4", "3, 1, 5, 2, 4", "4, 2, 1, 3, 5"],
            "answer": ["A", "C"],
            "solution": (
                "**Concept.** The deque content is always a contiguous run of the inserted values "
                "in increasing order with some removed from its two ends. A value can be output "
                "only when it is at the front or at the rear at that moment.\n\n"
                "- (A) Insert 1–5, delete rear 5 → deque [1, 2, 3, 4]; front 1; rear 4; front 2; "
                "then 3. **Possible.**\n"
                "- (B) After outputting 5 first, the deque is [1, 2, 3, 4]; 3 is in the middle and "
                "cannot be deleted next. **Impossible.**\n"
                "- (C) Insert 1, 2, 3; delete rear 3 → [1, 2]; delete front 1 → [2]; insert 4, 5 → "
                "[2, 4, 5]; delete rear 5; delete front 2; delete 4. **Possible.**\n"
                "- (D) 4 first means 1, 2, 3 are all in the deque [1, 2, 3]; 2 is in the middle. "
                "**Impossible.**\n\n"
                "**Tip:** for an input-restricted deque the only way to fail is to need an element "
                "strictly inside the current run. Of the 120 permutations of 1–5, 90 are achievable."
            ),
            "solution_diagrams": [{"type": "queue", "values": [1, 2, 3, 4],
                                   "caption": "Options (A)/(B): deque after 5 is deleted first"}],
            "verify": '''
def outs(n):
    res = set()
    def go(nxt, dq, out):
        if len(out) == n: res.add(tuple(out)); return
        if nxt <= n: go(nxt + 1, dq + [nxt], out)
        if dq:
            go(nxt, dq[1:], out + [dq[0]]); go(nxt, dq[:-1], out + [dq[-1]])
    go(1, [], []); return res
R = outs(5)
opts = {"A": (5,1,4,2,3), "B": (5,3,1,2,4), "C": (3,1,5,2,4), "D": (4,2,1,3,5)}
assert len(R) == 90
assert sorted(k for k in opts if opts[k] in R) == sorted(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q13
        {
            "type": "MCQ", "marks": 2, "topic": "Shortest paths — Dijkstra with tied path costs",
            "text": ("Dijkstra's algorithm is run from S on the weighted directed graph shown. A "
                     "tentative distance (and the stored predecessor) is changed only when a "
                     "**strictly** smaller value is found; when two vertices have equal tentative "
                     "distance, the alphabetically smaller one is extracted first. Which S–T path is "
                     "recorded through the predecessor pointers?"),
            "diagrams": [{"type": "graph", "directed": True,
                          "nodes": ["S", "A", "B", "C", "D", "T"],
                          "edges": [["S", "A", 2], ["S", "B", 3], ["A", "C", 4], ["B", "C", 3],
                                    ["A", "D", 5], ["B", "D", 4], ["C", "T", 3], ["D", "T", 2]],
                          "pos": {"S": [0, 1], "A": [2, 2.2], "B": [2, -0.2], "C": [4, 2.2],
                                  "D": [4, -0.2], "T": [6, 1]}}],
            "options": [
                "S → A → D → T",
                "S → B → C → T",
                "S → A → C → T",
                "S → B → D → T",
            ],
            "answer": "C",
            "solution": (
                "**Concept.** All four S–T paths here cost 9, so *which* one Dijkstra reports is "
                "decided purely by the order of relaxations and the strict-improvement rule.\n\n"
                "Trace:\n"
                "- Extract S (0): A = 2 (pred S), B = 3 (pred S).\n"
                "- Extract A (2): C = 6 (pred A), D = 7 (pred A).\n"
                "- Extract B (3): via B, C would be 3 + 3 = 6 — not < 6, unchanged; D would be "
                "3 + 4 = 7 — not < 7, unchanged.\n"
                "- Extract C (6): T = 9 (pred C).\n"
                "- Extract D (7): via D, T would be 7 + 2 = 9 — not < 9, unchanged.\n"
                "- Extract T (9).\n\n"
                "Predecessors: T ← C ← A ← S, i.e. S → A → C → T → (C).\n\n"
                "- (B) would be recorded if ties replaced the predecessor (≤ instead of <), since "
                "B is relaxed after A.\n"
                "- (A) and (D) need T's predecessor to be D, but C is extracted before D and sets "
                "T = 9 first.\n\n"
                "**Trap:** all four options are genuine shortest paths; the question is about the "
                "algorithm's *recorded* tree, not about optimality."
            ),
            "verify": '''
G = {"S": [("A",2),("B",3)], "A": [("C",4),("D",5)], "B": [("C",3),("D",4)],
     "C": [("T",3)], "D": [("T",2)], "T": []}
INF = 10**9; d = {v: INF for v in G}; d["S"] = 0; par = {}; done = set()
while len(done) < len(G):
    u = min((v for v in G if v not in done), key=lambda v: (d[v], v)); done.add(u)
    for v, w in G[u]:
        if d[u] + w < d[v]: d[v] = d[u] + w; par[v] = u
p, n = ["T"], "T"
while n != "S": n = par[n]; p.append(n)
assert " → ".join(reversed(p)) == "S → A → C → T" and d["T"] == 9 and ANSWER == "C"
''',
        },
        # ------------------------------------------------------------ Q14
        {
            "type": "NAT", "marks": 2, "topic": "Heaps — possible positions of the k-th smallest key",
            "text": ("A binary min-heap holds 15 distinct keys in an array H[0..14] (children of "
                     "index i are 2i + 1 and 2i + 2), so it is a perfect binary tree of 4 levels. "
                     "Over all possible such heaps, the number of distinct array indices at which "
                     "the **3rd smallest** key can appear is ______."),
            "answer": "6",
            "solution": (
                "**Concept.** In a min-heap every ancestor of a key is smaller than it. So the k-th "
                "smallest key can have at most k − 1 ancestors, i.e. it lies at depth ≤ k − 1. "
                "Also it can never be at the root (depth 0) unless k = 1.\n\n"
                "For the 3rd smallest key x₃:\n"
                "- Depth 0 (index 0): impossible — the root is the minimum.\n"
                "- Depth 1 (indices 1, 2): possible, e.g. the 2nd smallest is the other child of "
                "the root (or a child of x₃'s sibling).\n"
                "- Depth 2 (indices 3, 4, 5, 6): possible when its two ancestors are the 1st and "
                "2nd smallest — e.g. H = [1, 2, 4, 3, …] puts 3 at index 3.\n"
                "- Depth 3 (indices 7–14): impossible — it would need three smaller ancestors.\n\n"
                "Possible indices: 2 + 4 = **6**.\n\n"
                "**Trap:** answering 4 (only depth 2) or 2 (only depth 1). In general the k-th "
                "smallest can appear at any depth from 1 to k − 1 (for k ≥ 2)."
            ),
            "solution_diagrams": [{"type": "heap",
                                   "values": [1, 2, 4, 3, 9, 5, 6, 10, 11, 12, 13, 7, 8, 14, 15],
                                   "highlight": [3], "show_index": True,
                                   "caption": "A valid min-heap with the 3rd smallest key at index 3"}],
            "verify": '''
import random, heapq
random.seed(11)
pos = set()
for _ in range(20000):
    a = random.sample(range(15), 15); heapq.heapify(a)
    for i in range(15):
        if 2*i+1 < 15: assert a[i] < a[2*i+1]
    pos.add(a.index(2))
assert pos == {1, 2, 3, 4, 5, 6} and len(pos) == int(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q15
        {
            "type": "MSQ", "marks": 2, "topic": "Graphs — BFS levels and bipartiteness",
            "text": ("BFS is run from A on the undirected graph shown; neighbours are enqueued in "
                     "alphabetical order. Which of the following statements is/are TRUE?"),
            "diagrams": [{"type": "graph", "directed": False,
                          "nodes": ["A", "B", "C", "D", "E", "F", "G", "H"],
                          "edges": [["A", "B"], ["A", "C"], ["B", "D"], ["C", "D"], ["C", "E"],
                                    ["D", "F"], ["E", "F"], ["E", "G"], ["F", "H"], ["G", "H"]],
                          "pos": {"A": [0, 1], "B": [1.5, 2], "C": [1.5, 0], "D": [3, 2],
                                  "E": [3, 0], "F": [4.5, 2], "G": [4.5, 0], "H": [6, 1]}}],
            "options": [
                "The graph is bipartite",
                "H is at BFS level 3",
                "The BFS tree contains the edge C–E",
                "Adding the single edge B–C would make the graph non-bipartite",
            ],
            "answer": ["A", "C", "D"],
            "solution": (
                "**Concept.** BFS levels give a 2-colouring candidate (even/odd level). A connected "
                "graph is bipartite iff no edge joins two vertices on the **same** level "
                "(such an edge closes an odd cycle).\n\n"
                "BFS from A:\n"
                "- Level 0: A. Level 1: B, C.\n"
                "- From B: D (tree edge B–D). From C: D already seen; E (tree edge C–E). Level 2: D, E.\n"
                "- From D: F (tree edge D–F). From E: F seen; G (tree edge E–G). Level 3: F, G.\n"
                "- From F: H (tree edge F–H). Level 4: H.\n\n"
                "Every edge joins consecutive levels (A–B, A–C, B–D, C–D, C–E, D–F, E–F, E–G, F–H, "
                "G–H), so the graph is bipartite with parts {A, D, E, H} and {B, C, F, G}.\n\n"
                "- (A) **True.**\n"
                "- (B) **False** — H is at level 4.\n"
                "- (C) **True** — E is first discovered from C.\n"
                "- (D) **True** — B and C are both on level 1; B–C would create the triangle "
                "A–B–C, an odd cycle.\n\n"
                "**Trap:** the graph has many cycles, but all of them have length 4 or 6 — "
                "cycles alone do not break bipartiteness, only *odd* cycles do."
            ),
            "solution_diagrams": [{"type": "graph", "directed": False,
                                   "nodes": ["A", "B", "C", "D", "E", "F", "G", "H"],
                                   "edges": [["A", "B"], ["A", "C"], ["B", "D"], ["C", "D"], ["C", "E"],
                                             ["D", "F"], ["E", "F"], ["E", "G"], ["F", "H"], ["G", "H"]],
                                   "pos": {"A": [0, 1], "B": [1.5, 2], "C": [1.5, 0], "D": [3, 2],
                                           "E": [3, 0], "F": [4.5, 2], "G": [4.5, 0], "H": [6, 1]},
                                   "highlight": ["A", "D", "E", "H"],
                                   "highlight_edges": [["A", "B"], ["A", "C"], ["B", "D"], ["C", "E"],
                                                       ["D", "F"], ["E", "G"], ["F", "H"]],
                                   "caption": "BFS tree (red); one side of the bipartition highlighted"}],
            "verify": '''
from collections import deque
E = [("A","B"),("A","C"),("B","D"),("C","D"),("C","E"),("D","F"),("E","F"),("E","G"),
     ("F","H"),("G","H")]
def bfs(E):
    adj = {}
    for u, v in E: adj.setdefault(u, []).append(v); adj.setdefault(v, []).append(u)
    lvl, par = {"A": 0}, {}; q = deque("A")
    while q:
        u = q.popleft()
        for v in sorted(adj[u]):
            if v not in lvl: lvl[v] = lvl[u] + 1; par[v] = u; q.append(v)
    bip = all((lvl[u] - lvl[v]) % 2 for u, v in E)
    return lvl, par, bip
lvl, par, bip = bfs(E)
bip2 = bfs(E + [("B","C")])[2]
truth = {"A": bip, "B": lvl["H"] == 3, "C": par["E"] == "C", "D": not bip2}
assert sorted(k for k in truth if truth[k]) == sorted(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q16
        {
            "type": "MSQ", "marks": 2, "topic": "Quicksort — full Lomuto trace",
            "text": ("Quicksort with the Lomuto partition (pivot = last element of the sub-array; "
                     "partitioning m elements costs m − 1 comparisons) sorts "
                     "A = [5, 3, 8, 1, 9, 2, 7]. Sub-arrays with fewer than 2 elements are not "
                     "partitioned. Which of the following statements is/are TRUE?"),
            "code": '''def partition(A, lo, hi):
    pivot, i = A[hi], lo - 1
    for j in range(lo, hi):
        if A[j] <= pivot:
            i += 1
            A[i], A[j] = A[j], A[i]
    A[i + 1], A[hi] = A[hi], A[i + 1]
    return i + 1

def quicksort(A, lo, hi):
    if lo < hi:
        p = partition(A, lo, hi)
        quicksort(A, lo, p - 1)
        quicksort(A, p + 1, hi)''',
            "options": [
                "After the first partition, A = [5, 3, 1, 2, 7, 8, 9]",
                "The total number of key comparisons is 11",
                "The second call to partition uses 5 as its pivot",
                "partition is called exactly 4 times",
            ],
            "answer": ["A", "B", "D"],
            "solution": (
                "**Concept.** Trace partition calls in the order the recursion makes them (left "
                "sub-array first).\n\n"
                "Call 1 — A[0..6], pivot 7: elements ≤ 7 are 5, 3, 1, 2 → moved to the front in "
                "order; 8, 9 end up after. Swaps give [5, 3, 1, 2, 9, 8, 7], then the pivot swap "
                "→ [5, 3, 1, 2, 7, 8, 9], p = 4. Comparisons 6.\n\n"
                "Call 2 — A[0..3] = [5, 3, 1, 2], pivot **2**: only 1 ≤ 2 → [1, 3, 5, 2] → pivot "
                "swap → [1, 2, 5, 3], p = 1. Comparisons 3.\n"
                "- Left [1] (size 1) — no call. Right A[2..3] = [5, 3].\n\n"
                "Call 3 — A[2..3] = [5, 3], pivot 3: 5 > 3 → pivot swap → [3, 5]. Comparisons 1.\n\n"
                "Call 4 — A[5..6] = [8, 9], pivot 9: 8 ≤ 9 → unchanged. Comparisons 1.\n\n"
                "Totals: comparisons 6 + 3 + 1 + 1 = 11; partition calls 4.\n\n"
                "- (A) **True.**\n- (B) **True.**\n"
                "- (C) **False** — the second partition works on [5, 3, 1, 2] whose last element "
                "is 2.\n"
                "- (D) **True.**\n\n"
                "**Trap:** picking the *first* element (5) as pivot out of habit, or counting the "
                "calls on size-0/1 sub-arrays as partition calls."
            ),
            "solution_diagrams": [{"type": "matrix", "title": "Array after each partition call",
                                   "col_labels": ["0", "1", "2", "3", "4", "5", "6"],
                                   "row_labels": ["start", "call 1", "call 2", "call 3", "call 4"],
                                   "rows": [[5, 3, 8, 1, 9, 2, 7], [5, 3, 1, 2, 7, 8, 9],
                                            [1, 2, 5, 3, 7, 8, 9], [1, 2, 3, 5, 7, 8, 9],
                                            [1, 2, 3, 5, 7, 8, 9]],
                                   "highlight": [[1, 4], [2, 1], [3, 2], [4, 6]]}],
            "verify": '''
calls = []
orig = partition
def traced(A, lo, hi):
    calls.append((lo, hi, A[hi], hi - lo)); return orig(A, lo, hi)
partition = traced
A = [5, 3, 8, 1, 9, 2, 7]; snap = []
_p = partition
def traced2(A, lo, hi):
    r = _p(A, lo, hi); snap.append(A[:]); return r
partition = traced2
quicksort(A, 0, 6)
truth = {"A": snap[0] == [5,3,1,2,7,8,9], "B": sum(c[3] for c in calls) == 11,
         "C": calls[1][2] == 5, "D": len(calls) == 4}
assert A == sorted(A)
assert sorted(k for k in truth if truth[k]) == sorted(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q17
        {
            "type": "MCQ", "marks": 2, "topic": "Python — chained generators sharing an iterator",
            "text": "Consider the following Python program. What is printed?",
            "code": '''def evens(it):
    for x in it:
        if x % 2 == 0:
            yield x

def squares(it):
    for x in it:
        yield x * x

src = iter(range(10))
p = squares(evens(src))
first = next(p)
rest = list(zip(p, src))
print(first, rest)''',
            "options": [
                "`0 [(4, 3), (16, 5), (36, 7)]`",
                "`0 [(4, 1), (16, 3), (36, 5), (64, 7)]`",
                "`0 [(4, 0), (16, 1), (36, 2), (64, 3)]`",
                "`0 [(4, 3), (16, 5), (36, 7), (64, 9)]`",
            ],
            "answer": "D",
            "solution": (
                "**Concept.** Generators are lazy and `src` is a single iterator shared by the "
                "pipeline and by `zip`. Every value taken by one consumer is gone for the other. "
                "`zip` pulls from its first argument first, then from the second.\n\n"
                "Trace (src yields 0, 1, …, 9):\n"
                "- `next(p)`: evens takes 0 (even) → squares yields 0. first = 0.\n"
                "- zip round 1: p resumes; evens takes 1 (skip), 2 → yields 4. zip then takes 3 "
                "from src → (4, 3).\n"
                "- round 2: evens takes 4 → 16; src gives 5 → (16, 5).\n"
                "- round 3: evens takes 6 → 36; src gives 7 → (36, 7).\n"
                "- round 4: evens takes 8 → 64; src gives 9 → (64, 9).\n"
                "- round 5: evens finds src exhausted → p raises StopIteration → zip stops.\n\n"
                "Output `0 [(4, 3), (16, 5), (36, 7), (64, 9)]` → (D).\n\n"
                "- (B) assumes zip reads src *before* p in each round.\n"
                "- (C) assumes `src` restarts from 0 for zip (as if it were a range, not an iterator).\n"
                "- (A) stops one round early.\n\n"
                "**Trap:** the odd numbers that zip consumes are exactly the ones evens would have "
                "skipped anyway, so the squares are unaffected — but this is luck of the data, not "
                "a property of the code."
            ),
            "verify": "assert OUTPUT.strip() == '0 [(4, 3), (16, 5), (36, 7), (64, 9)]'",
        },
        # ------------------------------------------------------------ Q18
        {
            "type": "MSQ", "marks": 2, "topic": "Elementary sorting — stability and counts",
            "text": ("The array [4_{a}, 3, 4_{b}, 1] contains two equal keys 4, distinguished by the "
                     "labels a and b. It is sorted in ascending order by (i) selection sort that "
                     "picks the **first** minimum (strict `<`) and swaps it into place, (ii) bubble "
                     "sort that swaps adjacent elements only if the left one is strictly greater, "
                     "and (iii) insertion sort that shifts elements strictly greater than the key. "
                     "Which of the following statements is/are TRUE?"),
            "options": [
                "Selection sort produces 1, 3, 4_{b}, 4_{a}",
                "Selection sort performs exactly 2 swaps (a swap of an element with itself is not counted)",
                "Bubble sort produces 1, 3, 4_{a}, 4_{b}",
                "Insertion sort performs exactly 5 shifts",
            ],
            "answer": ["A", "C"],
            "solution": (
                "**Concept.** Bubble and insertion sort move elements only past *strictly* larger "
                "neighbours, so equal keys never overtake each other (stable). Selection sort's "
                "long-distance swap can jump an element over an equal key (unstable).\n\n"
                "Selection sort:\n"
                "- Pass 0: minimum 1 (index 3) swapped with 4_{a} → [1, 3, 4_{b}, 4_{a}] (1 swap).\n"
                "- Pass 1: minimum of [3, 4_{b}, 4_{a}] is 3 at index 1 → no swap.\n"
                "- Pass 2: minimum of [4_{b}, 4_{a}] with strict `<` is 4_{b} (first) → no swap.\n"
                "- Result 1, 3, 4_{b}, 4_{a} with **1** swap.\n\n"
                "Bubble sort: pass 1: 4_{a}>3 swap → [3, 4_{a}, 4_{b}, 1]; 4_{a} vs 4_{b} no swap; 4_{b}>1 swap → "
                "[3, 4_{a}, 1, 4_{b}]; pass 2: … → [3, 1, 4_{a}, 4_{b}]; pass 3 → [1, 3, 4_{a}, 4_{b}].\n\n"
                "Insertion sort shifts = number of inversions: (4_{a},3), (4_{a},1), (3,1), (4_{b},1) = 4.\n\n"
                "- (A) **True** — the equal keys end up in reversed order.\n"
                "- (B) **False** — only 1 real swap.\n"
                "- (C) **True** — bubble sort is stable.\n"
                "- (D) **False** — 4 shifts (equal keys do not form an inversion).\n\n"
                "**Trap:** counting (4_{a}, 4_{b}) as an inversion, or assuming selection sort is "
                "stable because it uses strict `<`."
            ),
            "verify": '''
A0 = [(4, 'a'), (3, ''), (4, 'b'), (1, '')]
S = A0[:]; sw = 0
for i in range(len(S)):
    m = i
    for j in range(i + 1, len(S)):
        if S[j][0] < S[m][0]: m = j
    if m != i: S[i], S[m] = S[m], S[i]; sw += 1
B = A0[:]
for i in range(len(B)):
    for j in range(len(B) - 1 - i):
        if B[j][0] > B[j+1][0]: B[j], B[j+1] = B[j+1], B[j]
I = A0[:]; sh = 0
for i in range(1, len(I)):
    k, j = I[i], i - 1
    while j >= 0 and I[j][0] > k[0]: I[j+1] = I[j]; j -= 1; sh += 1
    I[j+1] = k
lab = lambda L: [t for _, t in L if t]
truth = {"A": lab(S) == ['b', 'a'], "B": sw == 2, "C": lab(B) == ['a', 'b'], "D": sh == 5}
assert sorted(k for k in truth if truth[k]) == sorted(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q19
        {
            "type": "NAT", "marks": 2, "topic": "Hashing — chaining with insertion at the head",
            "text": ("The keys 15, 22, 9, 36, 30, 43, 12, 26 are inserted in that order into a hash "
                     "table of 7 slots using h(k) = k mod 7 and separate chaining, where each new "
                     "key is inserted at the **head** of its chain. Afterwards, each of the 8 keys "
                     "is searched for exactly once; a search compares the key with chain elements "
                     "from the head until it is found. The total number of key comparisons over "
                     "the 8 searches is ______."),
            "answer": "16",
            "solution": (
                "**Concept.** With head insertion, the most recently inserted key of a chain is "
                "found with 1 comparison, the one before with 2, and so on. A chain of length L "
                "contributes 1 + 2 + … + L = L(L + 1)/2.\n\n"
                "Home slots: 15 → 1, 22 → 1, 9 → 2, 36 → 1, 30 → 2, 43 → 1, 12 → 5, 26 → 5.\n\n"
                "Chains (head first):\n"
                "- slot 1: 43 → 36 → 22 → 15 (L = 4) → 1 + 2 + 3 + 4 = 10\n"
                "- slot 2: 30 → 9 (L = 2) → 3\n"
                "- slot 5: 26 → 12 (L = 2) → 3\n\n"
                "Total = 10 + 3 + 3 = **16**.\n\n"
                "**Tip:** the total is the same for tail insertion — only *which* key is cheap "
                "changes. What matters is the chain-length distribution: ∑ L(L + 1)/2.\n\n"
                "**Trap:** 22, 36 and 43 all reduce to 1 mod 7 (21, 35 and 42 are multiples of 7), "
                "which makes one chain much longer than the load factor 8/7 suggests."
            ),
            "solution_diagrams": [{"type": "hashtable", "size": 7,
                                   "slots": {1: [43, 36, 22, 15], 2: [30, 9], 5: [26, 12]},
                                   "caption": "Chains with head insertion"}],
            "verify": '''
T = {}
for k in [15, 22, 9, 36, 30, 43, 12, 26]: T.setdefault(k % 7, []).insert(0, k)
tot = sum(T[k % 7].index(k) + 1 for k in [15, 22, 9, 36, 30, 43, 12, 26])
assert tot == int(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q20
        {
            "type": "MCQ", "marks": 2, "topic": "Binary trees — reconstruction from level-order and in-order",
            "text": ("A binary tree with distinct labels has\n"
                     "- level-order traversal: P, K, W, C, M, S, F, U\n"
                     "- in-order traversal: C, F, K, M, P, S, U, W\n\n"
                     "What is its post-order traversal?"),
            "options": ["F, C, M, K, U, S, W, P", "F, C, M, K, S, U, W, P",
                        "C, F, M, K, U, S, W, P", "F, C, K, M, U, S, W, P"],
            "answer": "A",
            "solution": (
                "**Concept.** The first level-order symbol is the root. Split the in-order sequence "
                "at the root; for each side, the root of that subtree is the **first** symbol of "
                "the level-order sequence that belongs to that side.\n\n"
                "- Root P. In-order: [C, F, K, M] | P | [S, U, W].\n"
                "- Left side {C, F, K, M}: first in level order is K → root K; in-order "
                "[C, F] | K | [M]. Left of K: {C, F}, first in level order is C → C, with F right of "
                "C in in-order → F is C's right child. Right of K: M.\n"
                "- Right side {S, U, W}: first in level order is W → root W; in-order [S, U] | W, "
                "so W has only a left subtree {S, U} with root S (S precedes U in level order) and "
                "U as S's right child.\n\n"
                "Tree: P(K(C(·, F), M), W(S(·, U), ·)). Post-order: F, C, M, K, U, S, W, P → (A).\n\n"
                "- (B) swaps U and S — U is S's child, so U must come first.\n"
                "- (C) puts C before F, but F is C's child.\n"
                "- (D) puts K before M, but M is K's child.\n\n"
                "**Trap:** the level-order sequence is *not* split into contiguous blocks like "
                "pre-order; you must filter it by subtree membership."
            ),
            "solution_diagrams": [{"type": "bintree",
                                   "tree": ["P", ["K", ["C", None, ["F"]], ["M"]],
                                            ["W", ["S", None, ["U"]], None]],
                                   "caption": "Reconstructed tree"}],
            "verify": '''
def build(level, ino):
    if not ino: return None
    r = next(x for x in level if x in ino); k = ino.index(r)
    L, R = set(ino[:k]), set(ino[k+1:])
    return (r, build([x for x in level if x in L], ino[:k]),
               build([x for x in level if x in R], ino[k+1:]))
def post(t): return [] if t is None else post(t[1]) + post(t[2]) + [t[0]]
def lvl(t):
    out, q = [], [t]
    while q:
        n = q.pop(0)
        if n: out.append(n[0]); q += [n[1], n[2]]
    return out
t = build(list("PKWCMSFU"), list("CFKMPSUW"))
assert lvl(t) == list("PKWCMSFU")
opts = {"A": "FCMKUSWP", "B": "FCMKSUWP", "C": "CFMKUSWP", "D": "FCKMUSWP"}
assert [k for k in opts if list(opts[k]) == post(t)] == [ANSWER]
''',
        },
    ],
}
