# Set 33 — Full-Syllabus Mock — Paper 3
SET = {
    'number': 33,
    'title': 'Full-Syllabus Mock — Paper 3',
    'difficulty': 'GATE-level',
    'focus': 'balanced paper across the whole Section 4 syllabus',
    'questions': [
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Python — closures and late binding',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''fs = []
for i in range(3):
    fs.append(lambda x, i=i: x + i)
    fs.append(lambda x: x * i)
print([f(10) for f in fs])''',
            'options': [
                '`[10, 0, 11, 10, 12, 20]`',
                '`[10, 20, 11, 20, 12, 20]`',
                '`[12, 20, 12, 20, 12, 20]`',
                '`[10, 20, 11, 10, 12, 0]`',
            ],
            'answer': 'B',
            'solution': '''A lambda body looks up free variables **when it is called** (late binding), but a default argument is evaluated **when the lambda is created**.

- `lambda x, i=i: x + i` freezes the current i (0, 1, 2) → 10, 11, 12.
- `lambda x: x * i` reads the global i at call time; after the loop i = 2 → every one gives 10 × 2 = 20.

Interleaved: **[10, 20, 11, 20, 12, 20]**.

- (A) assumes the multiplying lambdas captured i = 0, 1, 2 at creation time.
- (C) assumes the default-argument lambdas are also late-bound.
- (D) mixes the two models in reverse order.

**Trap:** closures capture *variables*, not values. **Fix:** use a default argument or `functools.partial` to freeze a value.''',
            'verify': "ANSWER = {'A': 'B', 'B': 'A'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == '[10, 20, 11, 20, 12, 20]' and ANSWER == 'A'",
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Python — floor division and modulo with negatives',
            'text': 'The value printed by the Python statement `print(-17 // 5 + -17 % 5 * 2 + 17 % -5)` is ______.',
            'answer': '-1',
            'solution': '''Python's `//` rounds toward −∞ and `%` satisfies a == (a // b)·b + a % b, so the remainder takes the **sign of the divisor**. Unary minus binds tighter than `//`, `%`, `*`; and `%`, `*`, `//` share one precedence level (left to right).

- `-17 // 5` = ⌊−3.4⌋ = **−4**
- `-17 % 5` = −17 − (−4)(5) = **3**; then `3 * 2` = 6
- `17 % -5`: 17 // −5 = ⌊−3.4⌋ = −4, remainder 17 − (−4)(−5) = **−3**

Sum: −4 + 6 − 3 = **−1**.

**Trap:** C/Java truncate toward zero, which would give −3 + (−2)·2 + 2 = −5. In Python, `a % b` always has the sign of b.''',
            'verify': 'assert -17 // 5 + -17 % 5 * 2 + 17 % -5 == int(ANSWER)',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Stacks — infix to postfix',
            'text': '''Using the usual precedences (`^` highest and **right**-associative; `*`, `/` next, left-associative; `+`, `-` lowest, left-associative), the postfix form of

`a + b * ( c - d ) / e ^ f ^ g`

is''',
            'options': [
                '`a b c d - * e f g ^ ^ / +`',
                '`a b c d - * e f ^ g ^ / +`',
                '`a b c d - e f g ^ ^ / * +`',
                '`a b c d - * / e f g ^ ^ +`',
            ],
            'answer': 'A',
            'solution': '''Fully parenthesise first: `^` is right-associative, so e ^ f ^ g = e ^ (f ^ g); `*` and `/` are left-associative, so b * (c − d) / X = (b * (c − d)) / X.

Expression: a + ((b * (c − d)) / (e ^ (f ^ g))).

- b * (c − d) → `b c d - *`
- e ^ (f ^ g) → `e f g ^ ^`
- division → `b c d - * e f g ^ ^ /`
- plus a → **`a b c d - * e f g ^ ^ / +`**
- (B) `e f ^ g ^` treats `^` as left-associative ((e ^ f) ^ g).
- (C) groups b * ((c − d) / …), i.e. treats `*` and `/` as right-associative.
- (D) places `/` before its right operand is complete — not a valid postfix of this expression.

**Tip:** in the shunting-yard algorithm, an incoming `^` does **not** pop a `^` on the stack (right associativity), while an incoming `/` does pop a `*` (equal precedence, left).''',
            'verify': '''
def topost(s):
    prec = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}; out = []; st = []
    for t in s.split():
        if t.isalpha(): out.append(t)
        elif t == '(': st.append(t)
        elif t == ')':
            while st[-1] != '(': out.append(st.pop())
            st.pop()
        else:
            while st and st[-1] != '(' and (prec[st[-1]] > prec[t] or (prec[st[-1]] == prec[t] and t != '^')):
                out.append(st.pop())
            st.append(t)
    while st: out.append(st.pop())
    return ' '.join(out)
assert topost("a + b * ( c - d ) / e ^ f ^ g") == "a b c d - * e f g ^ ^ / +" and ANSWER == "A"
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Python — queue and stack interplay',
            'text': 'Consider the following Python program. The value printed is ______.',
            'code': '''from collections import deque
q = deque([1, 2, 3, 4, 5, 6])
st = []
for _ in range(3):
    st.append(q.popleft())
while st:
    q.append(st.pop())
for _ in range(3):
    q.append(q.popleft())
print(int(''.join(map(str, q))))''',
            'answer': '321456',
            'solution': '''A classic 'reverse the first k elements of a queue' routine (k = 3).

- Dequeue 1, 2, 3 and push them: queue [4, 5, 6], stack [1, 2, 3] (top 3).
- Pop the stack into the queue (LIFO reverses): queue [4, 5, 6, 3, 2, 1].
- Rotate n − k = 3 times (dequeue + enqueue): [3, 2, 1, 4, 5, 6].

Joined as digits: **321456**.

**Trap:** forgetting that the final rotation brings the reversed block to the **front** (answer 456321), or reversing twice (123456). **Tip:** the routine costs Θ(n) with one auxiliary stack of size k.''',
            'verify': 'assert OUTPUT.strip() == ANSWER',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Doubly linked list — deletion',
            'text': 'In the doubly linked list below every node has fields `prev`, `val`, `next`. The pointer p refers to the node with value 30 (neither first nor last). Which code fragment correctly unlinks p, so that the list reads 10, 20, 40, 50 in both directions?',
            'diagrams': [
                {
                    'type': 'linkedlist',
                    'values': [10, 20, 30, 40, 50],
                    'doubly': True,
                    'head': 'head',
                    'tail': 'tail',
                },
            ],
            'options': [
                '`p.next.prev = p.prev; p.prev = p.next`',
                '`p.prev.next = p.next; p.next.prev = p.prev.next`',
                '`p.prev.next = p.next; p.next.prev = p.prev`',
                '`p.prev.next = p.next.next; p.next.prev = p.prev`',
            ],
            'answer': 'C',
            'solution': '''To unlink p, its predecessor must point forward to p's successor and its successor must point back to p's predecessor. The two assignments are independent, so either order works.

- (A) 40.prev = 20 is right, but `p.prev = p.next` only changes p's own field; 20.next still points to 30, so the forward list is unchanged.
- (B) after the first statement p.prev.next **is** 40, so the second sets 40.prev = 40 — a self-loop; backward traversal breaks.
- (C) 20.next = 40 and 40.prev = 20. **Correct.**
- (D) 20.next = 50 skips 40 in the forward direction.

**Trap:** (B) — after modifying a link, an expression that goes *through* that link no longer means what it did. **Tip:** deletion is Θ(1) in a doubly linked list given p; a singly linked list needs the predecessor.''',
            'verify': '''ANSWER = {'A': 'C', 'C': 'A'}.get(ANSWER, ANSWER)

class Nd:
    def __init__(s, v): s.val, s.prev, s.next = v, None, None
def build():
    ns = [Nd(v) for v in [10, 20, 30, 40, 50]]
    for a, b in zip(ns, ns[1:]): a.next, b.prev = b, a
    return ns[0], ns[-1], ns[2]
def fwd(h):
    out = []
    while h and len(out) < 10: out.append(h.val); h = h.next
    return out
def bwd(t):
    out = []
    while t and len(out) < 10: out.append(t.val); t = t.prev
    return out
codes = ["p.prev.next = p.next; p.next.prev = p.prev",
         "p.prev.next = p.next; p.next.prev = p.prev.next",
         "p.next.prev = p.prev; p.prev = p.next",
         "p.prev.next = p.next.next; p.next.prev = p.prev"]
ok = []
for c in codes:
    h, t, p = build(); exec(c, {"p": p})
    ok.append(fwd(h) == [10, 20, 40, 50] and bwd(t) == [50, 40, 20, 10])
assert [x for x, o in zip("ABCD", ok) if o] == [ANSWER]
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Binary trees — node counting',
            'text': 'A binary tree has exactly 20 leaves and exactly 9 nodes that have exactly one child. The total number of nodes in the tree is ______.',
            'answer': '48',
            'solution': '''Let n₀, n₁, n₂ be the numbers of nodes with 0, 1, 2 children. Counting edges two ways:

- edges = n − 1 = n₀ + n₁ + n₂ − 1 (every node except the root has a parent edge)
- edges = n₁ + 2n₂ (child pointers)

Equating gives **n₂ = n₀ − 1** — independent of n₁.

So n₂ = 19 and n = 20 + 9 + 19 = **48**.

**Trap:** thinking the one-child nodes change the n₂ = n₀ − 1 relation, or adding 1 for the root separately. **Tip:** a *full* binary tree (n₁ = 0) with L leaves has exactly 2L − 1 nodes.''',
            'verify': '''
import random
random.seed(11)
def grow():
    # random binary tree; returns (n0, n1, n2)
    kids = {0: []}; nxt = 1; frontier = [0]
    while nxt < 60:
        u = random.choice(frontier)
        if len(kids[u]) < 2:
            kids[u].append(nxt); kids[nxt] = []; frontier.append(nxt); nxt += 1
    c = [0, 0, 0]
    for u in kids: c[len(kids[u])] += 1
    return c
for _ in range(50):
    n0, n1, n2 = grow(); assert n2 == n0 - 1
assert 20 + 9 + (20 - 1) == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Hashing — choice of table size',
            'text': 'The 20 keys 4, 8, 12, …, 80 (all multiples of 4) are inserted into a hash table of size m = 12 with h(k) = k mod 12 and separate chaining. The number of non-empty slots and the length of the longest chain are, respectively,',
            'options': ['3 and 7', '12 and 2', '3 and 6', '4 and 5'],
            'answer': 'A',
            'solution': '''4k mod 12 = 4·(k mod 3), so only slots **0, 4, 8** can ever be used — gcd(4, 12) = 4 means the stride shares a factor with m and only m / gcd = 3 slots are reachable.

For k = 1 … 20:

- k ≡ 1 (mod 3): k = 1, 4, …, 19 → 7 keys → slot 4
- k ≡ 2 (mod 3): k = 2, 5, …, 20 → 7 keys → slot 8
- k ≡ 0 (mod 3): k = 3, 6, …, 18 → 6 keys → slot 0

Non-empty slots = **3**, longest chain = **7**.

- (B) is what a well-spread hash would give.
- (C) gets the slot count right but miscounts the chains.
- (D) assumes m / gcd = 4 reachable slots.

**Tip:** choose m prime (e.g. 13) so that arithmetic patterns in the keys do not collapse onto a few slots; with m = 13 these keys would occupy all 13 slots.''',
            'solution_diagrams': [
                {
                    'type': 'hashtable',
                    'size': 12,
                    'slots': {
                        0: [12, 24, 36, 48, 60, 72],
                        4: [4, 16, 28, 40, 52, 64, 76],
                        8: [8, 20, 32, 44, 56, 68, 80],
                    },
                    'caption': 'Only three chains are used',
                },
            ],
            'verify': '''
from collections import Counter
c = Counter(k % 12 for k in range(4, 81, 4))
assert (len(c), max(c.values())) == (3, 7) and ANSWER == "A"
assert len({k % 13 for k in range(4, 81, 4)}) == 13
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Binary search — termination bug',
            'text': 'Consider the following function on the sorted list `a = [2, 4, 6, 8, 10]`. For which of the following calls does the `while` loop run **forever**?',
            'code': '''def bs(a, x):
    lo, hi = 0, len(a) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < x:
            lo = mid
        else:
            hi = mid
    return lo''',
            'run_code': False,
            'options': ['`bs(a, 10)`', '`bs(a, 7)`', '`bs(a, 2)`', '`bs(a, 6)`'],
            'answer': ['A', 'B', 'D'],
            'solution': '''The bug: `lo = mid` instead of `lo = mid + 1`. When hi = lo + 1, mid = lo (floor), and if a[lo] < x the assignment `lo = mid` changes nothing → infinite loop.

- (A) x = 10: mid 2 → lo 2; mid 3 (8 < 10) → lo 3; lo 3, hi 4 → mid 3 forever. **Loops.**
- (B) x = 7: mid 2 (6 < 7) → lo 2; mid 3 (8 ≥ 7) → hi 3; lo 2, hi 3 → mid 2 → lo 2 forever. **Loops.**
- (C) x = 2: mid 2 → hi 2; mid 1 (4 ≥ 2) → hi 1; mid 0 (2 ≥ 2) → hi 0 → stop. Terminates.
- (D) x = 6: mid 2 (6 ≥ 6) → hi 2; mid 1 (4 < 6) → lo 1; now lo 1, hi 2 → mid 1 again → lo 1 forever. **Loops.**

**Rule:** with mid = ⌊(lo + hi)/2⌋ the lower bound must move to mid + 1; with mid = ⌈(lo + hi)/2⌉ the upper bound must move to mid − 1. Otherwise a 2-element range can stall.''',
            'verify': '''_m = {'B': 'D', 'D': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'C', 'C': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

def bs(a, x, cap=100):
    lo, hi = 0, len(a) - 1; it = 0
    while lo < hi:
        it += 1
        if it > cap: return None
        mid = (lo + hi) // 2
        if a[mid] < x: lo = mid
        else: hi = mid
    return lo
a = [2, 4, 6, 8, 10]
loops = [bs(a, x) is None for x in (2, 6, 10, 7)]
assert sorted(ANSWER) == [c for c, t in zip("ABCD", loops) if t]
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Sorting — stability',
            'text': 'The records (3,a), (1,b), (3,c), (2,d), (1,e) are sorted by their **numeric key only** (letters are just labels). Selection sort is the standard version (find the minimum of A[i..n−1] with strict `<`, then swap it with A[i]); insertion sort shifts while the key is strictly greater. Which of the following statements is/are TRUE?',
            'options': [
                'Selection sort outputs (1,b) before (1,e)',
                'Selection sort outputs (3,c) before (3,a)',
                'Insertion sort outputs (3,a) before (3,c)',
                'Selection sort is stable on this input',
            ],
            'answer': ['A', 'B', 'C'],
            'solution': '''A sort is *stable* if equal keys keep their input order. Insertion sort (strict >) is stable; selection sort's long-distance swap can jump an element over an equal one.

Selection sort trace:

- i=0: min key 1 is (1,b) at index 1 → swap with (3,a): (1,b) (3,a) (3,c) (2,d) (1,e)
- i=1: min of the rest is (1,e) at index 4 → swap with (3,a): (1,b) (1,e) (3,c) (2,d) (3,a)
- i=2: min (2,d) → swap with (3,c): (1,b) (1,e) (2,d) (3,c) (3,a)
- i=3: (3,c) vs (3,a): no strictly smaller → stays

Result: (1,b) (1,e) (2,d) **(3,c) (3,a)**.

- (A) **True** — the 1-keys happen to keep their order.
- (B) **True** — (3,a) was carried to the end by the swap at i=1.
- (C) insertion sort gives (1,b) (1,e) (2,d) (3,a) (3,c). **True.**
- (D) the 3-keys are reordered. **False.**

**Trap:** concluding stability from one pair that happens to stay in order (A).''',
            'verify': '''_m = {'A': 'C', 'C': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'B', 'B': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

R = [(3, 'a'), (1, 'b'), (3, 'c'), (2, 'd'), (1, 'e')]
A = R[:]
for i in range(len(A) - 1):
    m = i
    for j in range(i + 1, len(A)):
        if A[j][0] < A[m][0]: m = j
    A[i], A[m] = A[m], A[i]
B = R[:]
for i in range(1, len(B)):
    k = B[i]; j = i - 1
    while j >= 0 and B[j][0] > k[0]: B[j + 1] = B[j]; j -= 1
    B[j + 1] = k
truth = [A.index((3, 'c')) < A.index((3, 'a')), B.index((3, 'a')) < B.index((3, 'c')),
         A.index((1, 'b')) < A.index((1, 'e')), A == sorted(R, key=lambda r: r[0])]
assert sorted(ANSWER) == [c for c, t in zip("ABCD", truth) if t]
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Graph traversal — tree and non-tree edges',
            'text': 'An undirected simple graph G has 12 vertices, 20 edges and exactly 3 connected components. A complete DFS (restarting from an unvisited vertex until every vertex is visited) is run on G. The number of edges of G that are **not** tree edges of the resulting DFS forest is',
            'options': ['12', '9', '8', '11'],
            'answer': 'D',
            'solution': '''A DFS (or BFS) forest contains one spanning tree per connected component. A spanning tree on c vertices has c − 1 edges, so the forest has Σ(cᵢ − 1) = n − k edges.

- Tree edges = 12 − 3 = 9
- Non-tree edges = 20 − 9 = **11**

(In an undirected DFS every non-tree edge is a back edge.)

- (A) 12 = 20 − 8 follows from wrongly taking n − k − 1 = 8 tree edges.
- (B) 9 is the number of tree edges.
- (C) 8 uses n − 1 = 11 tree edges *and* subtracts one more.

**Tip:** the answer does not depend on the traversal order or on BFS vs DFS — only on n, |E| and the number of components.''',
            'verify': '''ANSWER = {'A': 'D', 'D': 'A'}.get(ANSWER, ANSWER)

import random, itertools
random.seed(4)
sizes = [6, 3, 3]; V = []; start = 0; E = set()
for s in sizes:
    vs = list(range(start, start + s)); start += s
    for a, b in zip(vs, vs[1:]): E.add((a, b))
    V.append(vs)
pool = [p for vs in V for p in itertools.combinations(vs, 2) if p not in E]
random.shuffle(pool)
while len(E) < 20: E.add(pool.pop())
adj = {v: [] for v in range(12)}
for a, b in E: adj[a].append(b); adj[b].append(a)
seen = set(); tree = 0
def dfs(u):
    global tree
    seen.add(u)
    for w in adj[u]:
        if w not in seen: tree += 1; dfs(w)
for v in range(12):
    if v not in seen: dfs(v)
assert len(E) - tree == 11 and ANSWER == "A"
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Python — counting recursive calls',
            'text': 'Consider the following Python program. The value printed is ______.',
            'code': '''calls = 0

def f(n):
    global calls
    calls += 1
    if n <= 2:
        return n
    return f(n - 1) + f(n - 3)

f(9)
print(calls)''',
            'answer': '37',
            'solution': '''Let C(n) be the number of calls made by f(n), including itself. Then C(n) = 1 for n ≤ 2 and C(n) = 1 + C(n − 1) + C(n − 3) for n ≥ 3 (f(0) is reached from f(3), so n never goes negative).

- C(0) = C(1) = C(2) = 1
- C(3) = 1 + C(2) + C(0) = 3
- C(4) = 1 + 3 + 1 = 5
- C(5) = 1 + 5 + 1 = 7
- C(6) = 1 + 7 + 3 = 11
- C(7) = 1 + 11 + 5 = 17
- C(8) = 1 + 17 + 7 = 25
- C(9) = 1 + 25 + 11 = **37**

(The returned value f(9) = 22 is not printed.)

**Trap:** writing C(n) = C(n − 1) + C(n − 3) without the +1 for the current call, or confusing the call count with the return value. `global calls` is required — without it `calls += 1` raises UnboundLocalError.''',
            'verify': '''
C = {0: 1, 1: 1, 2: 1}
for n in range(3, 10): C[n] = 1 + C[n - 1] + C[n - 3]
assert OUTPUT.strip() == ANSWER == str(C[9])
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'BST — reconstruction from pre-order',
            'text': '''The pre-order traversal of a binary search tree with distinct keys is

30, 20, 10, 25, 22, 28, 40, 35, 50, 45

Which of the following statements is/are TRUE?''',
            'options': [
                'The in-order successor of 28 is 35',
                'The tree has exactly 4 leaves',
                'The post-order traversal ends with 45, 50, 40, 30',
                'The level-order traversal is 30, 20, 40, 10, 25, 35, 50, 22, 28, 45',
            ],
            'answer': ['C', 'D'],
            'solution': '''In a BST the pre-order sequence determines the tree: the first key is the root; the following keys smaller than it form the left subtree's pre-order, the larger ones the right subtree's. (Equivalently, insert the keys in pre-order sequence into an empty BST.)

- Root 30; left part 20, 10, 25, 22, 28; right part 40, 35, 50, 45.
- Left: 20 with left 10 and right 25 (whose children are 22 and 28).
- Right: 40 with left 35 and right 50 (whose left child is 45).

Post-order: 10, 22, 28, 25, 20, 35, 45, 50, 40, 30.

- (A) 28 has no right child, so its successor is the nearest ancestor for which 28 lies in the left subtree: **30**, not 35. **False.**
- (B) leaves: 10, 22, 28, 35, 45 → **5**. **False.**
- (C) **True.**
- (D) levels: [30] [20, 40] [10, 25, 35, 50] [22, 28, 45]. **True.**

**Tip:** the in-order sequence of a BST is just the sorted keys — 28's successor is the next larger key, 30.''',
            'solution_diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        30,
                        [
                            20,
                            [10],
                            [
                                25,
                                [22],
                                [28],
                            ],
                        ],
                        [
                            40,
                            [35],
                            [
                                50,
                                [45],
                                None,
                            ],
                        ],
                    ],
                    'caption': 'Reconstructed BST',
                },
            ],
            'verify': '''_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'C', 'C': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

def ins(t, k):
    if t is None: return [k, None, None]
    if k < t[0]: t[1] = ins(t[1], k)
    else: t[2] = ins(t[2], k)
    return t
seq = [30, 20, 10, 25, 22, 28, 40, 35, 50, 45]
t = None
for k in seq: t = ins(t, k)
def pre(t): return [] if t is None else [t[0]] + pre(t[1]) + pre(t[2])
def post(t): return [] if t is None else post(t[1]) + post(t[2]) + [t[0]]
def lv(t): return 0 if t is None else (1 if not t[1] and not t[2] else lv(t[1]) + lv(t[2]))
q, lev = [t], []
while q:
    u = q.pop(0); lev.append(u[0]); q += [c for c in u[1:] if c]
assert pre(t) == seq
s = sorted(seq)
truth = [post(t)[-4:] == [45, 50, 40, 30], lv(t) == 4,
         lev == [30, 20, 40, 10, 25, 35, 50, 22, 28, 45], s[s.index(28) + 1] == 35]
assert sorted(ANSWER) == [c for c, x in zip("ABCD", truth) if x]
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Heaps — bottom-up build-heap',
            'text': 'The array [3, 9, 2, 14, 7, 1, 11, 20, 5, 16] (0-based) is converted into a **max**-heap with the bottom-up build-heap algorithm: for i = ⌊n/2⌋ − 1 down to 0, sift A[i] down, each step swapping it with its larger child while that child is larger. The total number of swaps performed is ______.',
            'diagrams': [
                {
                    'type': 'heap',
                    'values': [3, 9, 2, 14, 7, 1, 11, 20, 5, 16],
                    'caption': 'Input array viewed as a complete binary tree',
                },
            ],
            'answer': '8',
            'solution': '''Build-heap processes internal nodes from the last one (index 4) back to the root; each sift-down may cascade several levels.

- i=4 (7): child 16 → swap (1) → [3, 9, 2, 14, 16, 1, 11, 20, 5, 7]
- i=3 (14): children 20, 5 → swap with 20 (2) → [3, 9, 2, 20, 16, 1, 11, 14, 5, 7]
- i=2 (2): children 1, 11 → swap with 11 (3) → [3, 9, 11, 20, 16, 1, 2, 14, 5, 7]
- i=1 (9): children 20, 16 → swap with 20 (4); now at index 3, children 14, 5 → swap with 14 (5) → [3, 20, 11, 14, 16, 1, 2, 9, 5, 7]
- i=0 (3): swap with 20 (6); at index 1 children 14, 16 → swap with 16 (7); at index 4 child 7 → swap (8) → [20, 16, 11, 14, 7, 1, 2, 9, 5, 3]

Total = **8** swaps.

**Trap:** stopping each sift-down after one level (that gives 5), or using repeated insertion (sift-up) instead, which performs a different set of swaps. **Tip:** build-heap is Θ(n) overall because most nodes are near the bottom.''',
            'solution_diagrams': [
                {
                    'type': 'heap',
                    'values': [20, 16, 11, 14, 7, 1, 2, 9, 5, 3],
                    'caption': 'Resulting max-heap',
                },
            ],
            'verify': '''
a = [3, 9, 2, 14, 7, 1, 11, 20, 5, 16]; n = len(a); sw = 0
for i in range(n // 2 - 1, -1, -1):
    j = i
    while True:
        l, r, m = 2 * j + 1, 2 * j + 2, j
        if l < n and a[l] > a[m]: m = l
        if r < n and a[r] > a[m]: m = r
        if m == j: break
        a[j], a[m] = a[m], a[j]; sw += 1; j = m
assert sw == int(ANSWER) and a == [20, 16, 11, 14, 7, 1, 2, 9, 5, 3]
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Quicksort — Hoare partition',
            'text': 'The Hoare partition scheme below (pivot = A[lo]) is called as `hoare(A, 0, 7)` on A = [6, 3, 9, 6, 1, 8, 2, 7]. What are the contents of A and the returned value afterwards?',
            'code': '''def hoare(A, lo, hi):
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
            'options': [
                'A = [1, 3, 2, 6, 9, 8, 6, 7], returns 3',
                'A = [2, 3, 1, 6, 9, 8, 6, 7], returns 4',
                'A = [2, 3, 1, 6, 9, 8, 6, 7], returns 3',
                'A = [2, 3, 1, 6, 6, 8, 9, 7], returns 3',
            ],
            'answer': 'C',
            'solution': '''Hoare's scheme moves i right past elements < p and j left past elements > p, then swaps. It returns j such that every element of A[lo..j] ≤ p ≤ every element of A[j+1..hi]; the pivot is **not** necessarily at position j.

p = 6.

- Round 1: i stops at 0 (6 is not < 6); j: 7 (7 > 6) → 6 (2) stops. Swap → [2, 3, 9, 6, 1, 8, 6, 7]
- Round 2: i: 1 (3 < 6) → 2 (9) stops; j: 5 (8 > 6) → 4 (1) stops. Swap → [2, 3, 1, 6, 9, 8, 6, 7]
- Round 3: i: 3 (6) stops; j: 3 (6) stops. i ≥ j → **return 3**.

Left part A[0..3] = 2, 3, 1, 6 (all ≤ 6); right part A[4..7] = 9, 8, 6, 7 (all ≥ 6).

- (A) gets the first swap wrong (1 is not reached by j in round 1).
- (B) is right about A but returns i + 1-style index 4 (that is Lomuto thinking).
- (D) moves the second 6 next to the first, as if the pivot were placed in final position.

**Trap:** with Hoare partition, recursion must be on [lo, j] and [j+1, hi] — **not** [lo, j−1] — because the pivot may sit anywhere in the left part.''',
            'solution_diagrams': [
                {
                    'type': 'array',
                    'values': [2, 3, 1, 6, 9, 8, 6, 7],
                    'pointers': {
                        'j': 3,
                    },
                    'label': 'A',
                    'caption': 'After partition: A[0..3] ≤ 6 ≤ A[4..7]',
                },
            ],
            'verify': '''ANSWER = {'A': 'C', 'C': 'A'}.get(ANSWER, ANSWER)

A = [6, 3, 9, 6, 1, 8, 2, 7]; r = hoare(A, 0, 7)
assert (A, r) == ([2, 3, 1, 6, 9, 8, 6, 7], 3) and ANSWER == "A"
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'DAGs — counting topological orders',
            'text': 'The number of distinct topological orderings of the directed acyclic graph below is ______.',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F'],
                    'edges': [
                        ['A', 'C'],
                        ['B', 'C'],
                        ['B', 'D'],
                        ['C', 'E'],
                        ['D', 'E'],
                        ['D', 'F'],
                    ],
                    'pos': {
                        'A': [0, 2],
                        'B': [0, 0],
                        'C': [2, 2],
                        'D': [2, 0],
                        'E': [4, 2],
                        'F': [4, 0],
                    },
                },
            ],
            'answer': '14',
            'solution': '''A topological order lists each vertex after all its predecessors. Count by branching on which source is output next (only vertices with no remaining in-edges may be chosen).

Constraints: A→C, B→C, B→D, C→E, D→E, D→F. Initial sources: A, B.

**Case 1 — A first.** Now only B is a source → B second. Remaining C, D, E, F with C→E, D→E, D→F:

- C next: then D, then E and F in either order → 2
- D next: remaining C, E, F with only C→E → 3 orders (F can be in any of 3 slots)
- Case 1 total = 5

**Case 2 — B first.** Sources now A, D:

- A next: remaining C, D, E, F with C→E, D→E, D→F → 5 (same as above)
- D next: remaining A, C, E, F with A→C→E and F free → F can go in any of 4 slots → 4
- Case 2 total = 9

Total = 5 + 9 = **14**.

**Trap:** multiplying independent-looking choices (e.g. 2 × 2 × …) — the choices interact, so systematic case analysis (or DP over subsets) is needed.''',
            'verify': '''
import itertools
E = [("A", "C"), ("B", "C"), ("B", "D"), ("C", "E"), ("D", "E"), ("D", "F")]
cnt = sum(all(p.index(a) < p.index(b) for a, b in E) for p in itertools.permutations("ABCDEF"))
assert cnt == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Complexity of a loop nest',
            'text': 'What is the time complexity of `work(n)` as a function of n (count the `c += 1` steps)?',
            'code': '''def work(n):
    c = 0
    i = 1
    while i <= n:
        j = 1
        while j <= n:
            c += 1
            j += i
        i *= 2
    return c''',
            'options': ['Θ(n log n)', 'Θ(n)', 'Θ(n²)', 'Θ(log² n)'],
            'answer': 'B',
            'solution': '''The outer loop takes i = 1, 2, 4, …, 2^{k} ≤ n (about log₂ n + 1 iterations). For a given i the inner loop steps j by i from 1 to n, so it runs ⌈n / i⌉ times.

Total ≈ n/1 + n/2 + n/4 + … ≤ 2n — a **geometric** series, so work(n) = **Θ(n)**.

Concretely, work(2^{10}) = 2047 and work(2^{14}) = 32767, i.e. 2n − 1 for powers of two.

- (A) Θ(n log n) is what you get if i ran over **all** integers 1 … n (harmonic series n·H_{n}) — but here i doubles.
- (C) Θ(n²) would need the inner loop to do n steps for each of n outer values.
- (D) Θ(log² n) ignores that the inner loop does n/i steps, not log n.

**Trap:** seeing two nested loops plus a log-style outer loop and multiplying n × log n without checking how the inner bound depends on i.''',
            'verify': '''ANSWER = {'A': 'B', 'B': 'A'}.get(ANSWER, ANSWER)

assert work(2 ** 10) == 2 * 2 ** 10 - 1 and work(2 ** 14) == 2 * 2 ** 14 - 1
r = [work(n) / n for n in (1000, 10000, 100000)]
assert max(r) < 2.1 and min(r) > 1.5 and ANSWER == "A"
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Merge sort — counting inversions',
            'text': 'Inversions of A = [5, 9, 2, 7, 1, 8, 3, 6] are counted with the divide-and-conquer merge-sort method: inversions inside the left half + inside the right half + *split* inversions (pairs with one element in each half) counted during the final merge. The number of split inversions counted during the **final** merge (left half [5, 9, 2, 7], right half [1, 8, 3, 6]) is ______.',
            'answer': '10',
            'solution': '''A split inversion is a pair (x, y) with x in the left half, y in the right half and x > y. During the merge of the **sorted** halves L = [2, 5, 7, 9] and R = [1, 3, 6, 8], each time an element of R is output, it forms an inversion with every element still remaining in L.

- output 1 (from R): L remaining = 4 → +4
- output 2 (L), then 3 (R): L remaining {5, 7, 9} → +3
- output 5 (L), then 6 (R): L remaining {7, 9} → +2
- output 7 (L), then 8 (R): L remaining {9} → +1
- output 9

Split inversions = 4 + 3 + 2 + 1 = **10**.

Check directly: 5 > 1, 3; 9 > 1, 8, 3, 6; 2 > 1; 7 > 1, 3, 6 → 2 + 4 + 1 + 3 = 10. (Total inversions = 3 in the left half + 2 in the right half + 10 = 15.)

**Trap:** adding 1 per R-element output instead of 'number of remaining L elements'. **Tip:** the whole count runs in Θ(n log n).''',
            'verify': '''
A = [5, 9, 2, 7, 1, 8, 3, 6]
L, R = A[:4], A[4:]
split = sum(x > y for x in L for y in R)
inv = lambda a: sum(a[i] > a[j] for i in range(len(a)) for j in range(i + 1, len(a)))
assert split == int(ANSWER) and inv(A) == inv(L) + inv(R) + split == 15
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'DFS and BFS trees of an undirected graph',
            'text': 'DFS and BFS are each run from vertex A on the undirected graph below, visiting neighbours in alphabetical order. Which of the following statements is/are TRUE?',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
                    'edges': [
                        ['A', 'B'],
                        ['A', 'C'],
                        ['B', 'D'],
                        ['C', 'D'],
                        ['D', 'E'],
                        ['E', 'F'],
                        ['E', 'G'],
                        ['F', 'G'],
                        ['C', 'F'],
                    ],
                    'pos': {
                        'A': [0, 1.5],
                        'B': [1.5, 3],
                        'C': [1.5, 0],
                        'D': [3, 1.5],
                        'E': [4.5, 2.5],
                        'F': [4.5, 0],
                        'G': [6, 1.25],
                    },
                },
            ],
            'options': [
                'In the DFS, G is discovered before E',
                'The DFS produces exactly 3 back edges',
                'Every vertex of the DFS tree has at most one child (the DFS tree is a path)',
                'In the BFS tree the largest distance (level) of any vertex from A is 3',
            ],
            'answer': ['B', 'C', 'D'],
            'solution': '''**DFS (recursive, alphabetical):** A → B (A's first neighbour) → D (B's next unvisited) → C (D's neighbours B, C, E: B visited, so C) → F (C's neighbours A, D visited, F new) → E (F's neighbours C, E, G → E first) → G (E's neighbours D, F visited, G new). Then everything backtracks.

Tree edges: AB, BD, DC, CF, FE, EG — the tree is the path A-B-D-C-F-E-G. The other 9 − 6 = 3 edges (AC, DE, FG) are back edges.

**BFS from A:** level 1 {B, C}; level 2 {D (via B), F (via C)}; level 3 {E (via D), G (via F)}.

- (A) E is discovered from F before G. **False.**
- (B) **True** — in an undirected DFS every non-tree edge is a back edge; 9 − (7 − 1) = 3.
- (C) **True.**
- (D) **True** — E and G are at distance 3.

**Contrast:** the DFS tree has depth 6 while the BFS tree has depth 3 — BFS trees are shortest-path trees; DFS trees can be as deep as n − 1.''',
            'solution_diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
                    'edges': [
                        ['A', 'B'],
                        ['A', 'C'],
                        ['B', 'D'],
                        ['C', 'D'],
                        ['D', 'E'],
                        ['E', 'F'],
                        ['E', 'G'],
                        ['F', 'G'],
                        ['C', 'F'],
                    ],
                    'pos': {
                        'A': [0, 1.5],
                        'B': [1.5, 3],
                        'C': [1.5, 0],
                        'D': [3, 1.5],
                        'E': [4.5, 2.5],
                        'F': [4.5, 0],
                        'G': [6, 1.25],
                    },
                    'highlight_edges': [
                        ['A', 'B'],
                        ['B', 'D'],
                        ['D', 'C'],
                        ['C', 'F'],
                        ['F', 'E'],
                        ['E', 'G'],
                    ],
                    'caption': 'DFS tree (highlighted) is a Hamiltonian path',
                },
            ],
            'verify': '''_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'C', 'C': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

E = [("A","B"),("A","C"),("B","D"),("C","D"),("D","E"),("E","F"),("E","G"),("F","G"),("C","F")]
adj = {}
for a, b in E:
    adj.setdefault(a, []).append(b); adj.setdefault(b, []).append(a)
for v in adj: adj[v].sort()
order, tree = [], []
def dfs(u):
    order.append(u)
    for w in adj[u]:
        if w not in order: tree.append((u, w)); dfs(w)
dfs("A")
kids = {}
for u, w in tree: kids[u] = kids.get(u, 0) + 1
from collections import deque
dist = {"A": 0}; q = deque("A")
while q:
    u = q.popleft()
    for w in adj[u]:
        if w not in dist: dist[w] = dist[u] + 1; q.append(w)
truth = [max(kids.values()) == 1, len(E) - len(tree) == 3, max(dist.values()) == 3,
         order.index("G") < order.index("E")]
assert sorted(ANSWER) == [c for c, t in zip("ABCD", truth) if t]
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Linear probing — clustering effects',
            'text': 'Keys 25, 47, 14, 36, 58, 70, 3 are inserted in that order into an initially empty hash table of size 11 with h(k) = k mod 11 and linear probing (step +1). Probes are counted as slots inspected, including the final one. Which of the following statements is/are TRUE?',
            'options': [
                'An unsuccessful search for a key whose home slot is 3 makes 8 probes',
                'The average number of probes over the seven successful searches is 27/7',
                'Key 70 is stored in slot 8',
                'The table contains a run of 8 consecutive occupied slots',
            ],
            'answer': ['A', 'B', 'C'],
            'solution': '''Homes: 25→3, 47→3, 14→3, 36→3, 58→3, 70→4, 3→3 — six keys share home 3!

- 25 → 3 (1 probe); 47 → 4 (2); 14 → 5 (3); 36 → 6 (4); 58 → 7 (5)
- 70: home 4 is inside the cluster → 4, 5, 6, 7 full → **8** (5 probes)
- 3: 3 … 8 full → 9 (7 probes)

Final: slots 3–9 occupied (a run of 7), slots 0, 1, 2, 10 empty.

- (A) from slot 3: slots 3 … 9 full (7 probes), slot 10 empty (8th probe). **True.**
- (B) a successful search for a key repeats its insertion probes: 1 + 2 + 3 + 4 + 5 + 5 + 7 = 27 → 27/7 ≈ 3.86. **True.**
- (C) **True.**
- (D) the run is slots 3–9, length **7**. **False.**

**Insight:** key 70 had a *different* home slot yet paid 5 probes — primary clustering penalises every key whose home falls inside a cluster, not just keys with the same home.''',
            'solution_diagrams': [
                {
                    'type': 'hashtable',
                    'size': 11,
                    'slots': {
                        3: 25,
                        4: 47,
                        5: 14,
                        6: 36,
                        7: 58,
                        8: 70,
                        9: 3,
                    },
                    'caption': 'Final table: one cluster, slots 3–9',
                },
            ],
            'verify': '''_m = {'A': 'C', 'C': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

T = [None] * 11; pr = {}
for k in [25, 47, 14, 36, 58, 70, 3]:
    i, c = k % 11, 1
    while T[i] is not None: i = (i + 1) % 11; c += 1
    T[i] = k; pr[k] = c
i, c = 3, 1
while T[i] is not None: i = (i + 1) % 11; c += 1
run = best = 0
for x in T + T:
    run = run + 1 if x is not None else 0; best = max(best, run)
from fractions import Fraction
truth = [T[8] == 70, Fraction(sum(pr.values()), 7) == Fraction(27, 7), c == 8, best == 8]
assert sorted(ANSWER) == [x for x, t in zip("ABCD", truth) if t]
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Python — generator and iterator exhaustion',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''g = (x * x for x in range(5))
a = sum(g)
b = sum(g)
it = iter([1, 2, 3, 4])
pairs = list(zip(it, it))
print(a, b, pairs)''',
            'options': [
                '`30 0 [(1, 1), (2, 2), (3, 3), (4, 4)]`',
                '`30 30 [(1, 1), (2, 2), (3, 3), (4, 4)]`',
                '`30 30 [(1, 2), (3, 4)]`',
                '`30 0 [(1, 2), (3, 4)]`',
            ],
            'answer': 'D',
            'solution': '''Generators and iterators are **single-pass**: once consumed they yield nothing more.

- `a = sum(g)` consumes the generator: 0 + 1 + 4 + 9 + 16 = **30**.
- `b = sum(g)`: g is exhausted → sum of nothing = **0**.
- `zip(it, it)` pulls from the **same** iterator for both positions: first pair takes 1 then 2, the next pair 3 then 4 → **[(1, 2), (3, 4)]**.

Output: **30 0 [(1, 2), (3, 4)]**.

- (A) gets exhaustion right but treats the two `it` arguments as independent copies.
- (B) treats g as re-iterable and `it` as two independent iterators.
- (C) gets zip right but assumes the generator restarts.

**Tip:** `zip(*[iter(seq)] * k)` is the standard idiom for chunking a sequence into k-tuples — it works precisely because all k arguments are the same iterator.''',
            'verify': "ANSWER = {'A': 'D', 'D': 'A'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == '30 0 [(1, 2), (3, 4)]' and ANSWER == 'A'",
        },
    ],
}
