# Set 46 — Challenge Mock — Paper 1 (Hard)
# Q1-Q10: 1 mark, Q11-Q20: 2 marks.

SET = {
    'number': 46,
    'title': 'Challenge Mock — Paper 1',
    'difficulty': 'Hard',
    'focus': 'hardest, multi-concept, trap-heavy 2-mark questions',
    'questions': [
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Python — short-circuit values, chained comparisons, identity',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''a = 0 or [] or 'GATE'[1:3]
b = 1 < 3 > 2 == 2
c = [] is not [] and not 0
print(a, b, c, (5 > 3) + (2 > 1) * 2)''',
            'options': ['`AT False True 3`', '`AT True True 3`', '`True True False 2`', '`AT True False 3`'],
            'answer': 'B',
            'solution': '''Four independent traps:

- `or` returns the **first truthy operand** (or the last one): 0 and [] are falsy, so `a = 'GATE'[1:3]` = `'AT'` (indices 1 and 2) — a string, not `True`.
- Chained comparison `1 < 3 > 2 == 2` means `1 < 3 and 3 > 2 and 2 == 2` → **True** (it is *not* `(1 < 3) > 2`, which would be False).
- Each `[]` literal creates a new list, so `[] is not []` is True; `not 0` is True; `and` returns the last evaluated operand → **True**.
- Booleans are integers: True + True * 2 = 1 + 2 = **3**.

Output: `AT True True 3`.

- (A) evaluates the chain left to right as `(1 < 3) > 2`.
- (C) treats `or` as returning a bool and adds without precedence.
- (D) thinks two empty lists are the same object.

**Trap:** `and`/`or` return operands, not booleans; `is` compares identity, not equality.''',
            'verify': '''ANSWER = {'A': 'B', 'B': 'A'}.get(ANSWER, ANSWER)

assert OUTPUT.split() == ['AT', 'True', 'True', '3'] and ANSWER == 'A'
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Stack permutations — counting with a constraint',
            'text': 'The integers 1, 2, 3, 4, 5 are pushed in this order onto an initially empty stack, with pops interleaved arbitrarily; each popped value is output and the stack is empty at the end. The number of possible output sequences whose **first** element is 3 is ______.',
            'answer': '9',
            'solution': '''To output 3 first, we must push 1, 2, 3 and pop 3 immediately. Now the stack holds [1, 2] (2 on top) and 4, 5 are still to be pushed.

Count the ways to finish. Think of it as interleaving: 2 must come out before 1 (stack order), and 4, 5 can be pushed/popped in between.

Enumerate by when 4 is pushed relative to popping 2 and 1:
- Pop 2, pop 1, then 4/5: {4 5, 5 4} → 2 sequences (3 2 1 4 5, 3 2 1 5 4).
- Pop 2, then 4/5 activity, then 1 at some point: 3 2 4 1 5, 3 2 4 5 1, 3 2 5 4 1 → 3.
- Push 4 before popping 2: 3 4 2 1 5, 3 4 2 5 1, 3 4 5 2 1, 3 5 4 2 1 → 4.

Total = 2 + 3 + 4 = **9**.

Check by the pattern rule: a sequence is achievable iff it has no a…b…c with c < a < b. After the leading 3, the remaining 4 values must avoid the pattern and keep 2 before 1.

**Trap:** answering C₄ = 14 (as if the stack were empty after outputting 3) ignores that 1 and 2 are already stacked in a fixed order.''',
            'solution_diagrams': [
                {
                    'type': 'stack',
                    'values': [1, 2],
                    'label': 'after popping 3',
                    'caption': '2 must be popped before 1',
                },
            ],
            'verify': '''
from itertools import permutations
def ok(out):
    st, nxt = [], 1
    for x in out:
        while nxt <= x: st.append(nxt); nxt += 1
        if not st or st[-1] != x: return False
        st.pop()
    return True
assert sum(ok(p) for p in permutations(range(1, 6)) if p[0] == 3) == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Complexity — doubling outer loop',
            'text': 'The time complexity of the following fragment, as a function of n, is',
            'code': '''i, s = 1, 0
while i < n:
    for j in range(i):
        s += 1
    i *= 2''',
            'options': ['Θ(log n)', 'Θ(n log n)', 'Θ(n)', 'Θ(n²)'],
            'answer': 'C',
            'solution': '''The outer loop runs about log₂ n times, but the inner loop's length **doubles** each time (i = 1, 2, 4, …, < n). Total inner iterations:
1 + 2 + 4 + … + 2^{k} where 2^{k} < n ≤ 2^{k+1} → sum = 2^{k+1} − 1 < 2n.
Hence the work is **Θ(n)** (a geometric series is dominated by its last term).

- (A) counts only outer iterations.
- (B) multiplies log n iterations by the *maximum* inner length n — an upper bound that is not tight.
- (D) has no basis.

**Trap:** 'a loop inside a log-loop' is not automatically n log n; sum the actual inner lengths.''',
            'verify': '''ANSWER = {'B': 'C', 'C': 'B'}.get(ANSWER, ANSWER)

def work(n):
    i, s = 1, 0
    while i < n:
        for j in range(i): s += 1
        i *= 2
    return s
for n in (1000, 4096, 50000):
    assert n / 2 <= work(n) < 2 * n
assert ANSWER == 'B'
''',
            'run_code': False,
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Queue using two stacks',
            'text': '''A queue is implemented with two stacks IN and OUT: `enqueue(x)` pushes x on IN; `dequeue()` first, **only if OUT is empty**, pops every element of IN and pushes it on OUT, and then pops OUT. Starting empty, the operations are:
enq 1, enq 2, enq 3, deq, enq 4, enq 5, deq, deq, deq, enq 6, deq.
Which of the following statements is/are TRUE?''',
            'options': [
                'At the end, OUT is empty and IN contains only 6',
                'No single dequeue performs more than 5 push/pop operations',
                'In total, 5 elements are moved from IN to OUT',
                'The second dequeue moves elements from IN to OUT',
            ],
            'answer': ['A', 'C'],
            'solution': '''Elements are transferred only when OUT is empty, which is what makes the amortised cost O(1).

- enq 1, 2, 3 → IN [1, 2, 3].
- deq #1: OUT empty → move 3 elements (OUT [3, 2, 1], top 1); pop 1. Cost 3 pops + 3 pushes + 1 pop = **7** operations.
- enq 4, 5 → IN [4, 5].
- deq #2: OUT = [3, 2] not empty → pop 2 (no transfer).
- deq #3: pop 3. OUT empty.
- deq #4: OUT empty → move 4, 5 (OUT [5, 4]); pop 4.
- enq 6 → IN [6].
- deq #5: OUT = [5] → pop 5. OUT empty; IN = [6].

- (A) True.
- (B) False — the first dequeue performs 7 push/pop operations.
- (C) 3 + 2 = **5** transfers. True.
- (D) False — OUT still held 2 and 3.

**Trap:** transferring on *every* dequeue (not only when OUT is empty) would break FIFO order.''',
            'solution_diagrams': [
                {
                    'type': 'stack',
                    'values': [3, 2, 1],
                    'label': 'OUT after deq #1 transfer',
                    'caption': 'Reversal puts the oldest element (1) on top',
                },
            ],
            'verify': '''_m = {'B': 'A', 'A': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'B': 'C', 'C': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

IN, OUT = [], []; moves = 0; costs = []; transfers_at = []
def enq(x): IN.append(x)
def deq():
    global moves
    c = 0; t = False
    if not OUT:
        while IN: OUT.append(IN.pop()); moves += 1; c += 2; t = True
    c += 1; costs.append(c); transfers_at.append(t)
    return OUT.pop()
enq(1); enq(2); enq(3); deq(); enq(4); enq(5); deq(); deq(); deq(); enq(6); deq()
truth = {'A': transfers_at[1], 'B': moves == 5, 'C': OUT == [] and IN == [6], 'D': max(costs) <= 5}
assert sorted(k for k in truth if truth[k]) == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Hashing — expected number of empty slots',
            'text': '12 keys are inserted into a hash table with 8 slots using separate chaining. Assume simple uniform hashing (each key independently hashes to each slot with probability 1/8). The expected number of slots that remain **empty** is ______ (rounded off to two decimal places).',
            'answer': ['1.60', '1.62'],
            'solution': '''Use linearity of expectation with an indicator for each slot.

P(a particular slot is empty) = P(none of the 12 keys hashes there) = (1 − 1/8)^{12} = (7/8)^{12}.

(7/8)^{2} = 0.765625; (7/8)^{4} ≈ 0.586182; (7/8)^{8} ≈ 0.343609; (7/8)^{12} ≈ 0.343609 × 0.586182 ≈ 0.201417.

E[empty slots] = 8 × 0.201417 ≈ **1.61**.

**Trap:** the events 'slot i empty' are *not* independent, but linearity of expectation does not need independence. Also, n > m does not mean every slot is used — about 20% of slots are still empty on average.''',
            'verify': '''
from itertools import product
e = 8 * (7 / 8) ** 12
assert float(ANSWER[0]) <= round(e, 2) <= float(ANSWER[1])
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Graph theory — graphical degree sequences',
            'text': 'Which of the following is **not** the degree sequence of any simple undirected graph?',
            'options': [
                '(5, 5, 4, 3, 2, 2, 1)',
                '(5, 5, 5, 3, 2, 1, 1)',
                '(6, 5, 4, 3, 2, 2, 2)',
                '(4, 4, 3, 3, 2, 2, 2)',
            ],
            'answer': 'B',
            'solution': '''All four have an even sum and maximum degree ≤ 6 = n − 1, so the quick checks pass. Use **Havel–Hakimi**: remove the largest degree d and subtract 1 from the next d degrees; repeat.

(B) (5, 5, 5, 3, 2, 1, 1): remove 5 → (4, 4, 2, 1, 0, 1) → sort (4, 4, 2, 1, 1, 0); remove 4 → (3, 1, 0, 0, 0) → remove 3 → needs three positive entries after it, but we get (0, −1, −1) → **not graphical**.
(Erdős–Gallai at k = 3: 5 + 5 + 5 = 15 > 3·2 + min(3,3) + min(2,3) + 1 + 1 = 13.) Intuitively, three vertices of degree 5 each need 3 neighbours outside the trio, but the other four vertices have total degree only 7 and two of them have degree 1.

- (A) remove 5 → (4, 3, 2, 1, 1, 1) → remove 4 → (2, 1, 0, 0, 1) → (2, 1, 1, 0, 0) → (0, 0, 0, 0) ✓ graphical.
- (C) remove 6 → (4, 3, 2, 1, 1, 1) → same as above ✓.
- (D) remove 4 → (3, 2, 2, 1, 2, 2) → (3, 2, 2, 2, 2, 1) → (1, 1, 1, 2, 1) → … ✓.

**Trap:** 'even sum and max degree ≤ n − 1' is necessary but **not sufficient**.''',
            'verify': '''ANSWER = {'C': 'B', 'B': 'C'}.get(ANSWER, ANSWER)

def graphical(seq):
    s = sorted(seq, reverse=True)
    while s and s[0] > 0:
        d = s.pop(0)
        if d > len(s): return False
        for i in range(d): s[i] -= 1
        if min(s) < 0: return False
        s.sort(reverse=True)
    return True
opts = [(5,5,4,3,2,2,1), (6,5,4,3,2,2,2), (5,5,5,3,2,1,1), (4,4,3,3,2,2,2)]
assert [L for L, s in zip('ABCD', opts) if not graphical(s)] == [ANSWER]
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Binary search on the answer',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''N = 1000
lo, hi, it = 0, N, 0
while lo < hi:
    it += 1
    m = (lo + hi + 1) // 2
    if m * m <= N:
        lo = m
    else:
        hi = m - 1
print(lo, it)''',
            'options': ['`32 9`', '`31 10`', '`31 9`', '`31 11`'],
            'answer': 'C',
            'solution': '''This finds the **largest m with m² ≤ N** (integer square root). Using the *upper* middle `(lo+hi+1)//2` together with `lo = m` guarantees progress (with the lower middle the loop could stick at hi = lo + 1).

Trace (lo, hi) → m:
- (0, 1000) m=500 > → hi=499
- (0, 499) m=250 > → hi=249
- (0, 249) m=125 > → hi=124
- (0, 124) m=62 > → hi=61
- (0, 61) m=31: 961 ≤ 1000 → lo=31
- (31, 61) m=46 > → hi=45
- (31, 45) m=38 > → hi=37
- (31, 37) m=34 > → hi=33
- (31, 33) m=32: 1024 > → hi=31 → loop ends.

9 iterations, lo = 31. Output `31 9`.

- (A) 32 would be the ceiling square root; 32² = 1024 > 1000.
- (B), (D) miscount iterations (e.g. adding a final check).

**Trap:** the iteration count is not simply ⌈log₂ 1001⌉ = 10, because each step removes slightly more than half when it moves `hi = m − 1`.''',
            'verify': '''ANSWER = {'A': 'C', 'C': 'A'}.get(ANSWER, ANSWER)

assert OUTPUT.split() == ['31', '9'] and ANSWER == 'A'
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Sorting — adjacent swaps versus arbitrary swaps',
            'text': 'For the array [4, 3, 1, 6, 5, 2, 8, 7], let x be the minimum number of swaps of **adjacent** elements needed to sort it in ascending order, and y the minimum number of swaps of **arbitrary** pairs of elements. The pair (x, y) is',
            'options': ['(9, 5)', '(9, 4)', '(5, 5)', '(8, 5)'],
            'answer': 'A',
            'solution': '''- An adjacent swap removes **exactly one inversion**, so x = number of inversions (this is the number of swaps bubble sort or insertion sort performs).
- An arbitrary swap can fix one element per swap within a permutation cycle, so y = n − (number of cycles).

**Inversions:** 4 > 3, 1, 2 (3); 3 > 1, 2 (2); 6 > 5, 2 (2); 5 > 2 (1); 8 > 7 (1) → x = **9**.

**Cycles** (value v belongs at index v − 1): index 0 holds 4 → index 3 holds 6 → index 5 holds 2 → index 1 holds 3 → index 2 holds 1 → back to index 0: a 5-cycle. Index 4 holds 5 (fixed point). Indices 6, 7 hold 8, 7: a 2-cycle. Cycles = 3 → y = 8 − 3 = **5**.

- (B) counts cycles of length > 1 as 3 and subtracts wrongly (8 − 4).
- (C) assumes adjacent swaps are as powerful as arbitrary ones.
- (D) misses one inversion.

**Tip:** selection sort achieves y (at most n − 1 swaps); bubble/insertion sort achieve x.''',
            'verify': '''
A = [4, 3, 1, 6, 5, 2, 8, 7]
x = sum(1 for i in range(8) for j in range(i + 1, 8) if A[i] > A[j])
seen, cyc = set(), 0
for i in range(8):
    if i in seen: continue
    cyc += 1; j = i
    while j not in seen: seen.add(j); j = A[j] - 1
assert (x, 8 - cyc) == (9, 5) and ANSWER == 'A'
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Python — scoping errors',
            'text': 'Each of the four snippets below is run **separately**, in a fresh interpreter. Which of them raise an exception?',
            'code': '''# Snippet (A)
x = 5
def f():
    print(x)
    x = 6
f()

# Snippet (B)
def g():
    total = 0
    def add(v):
        total += v
    add(3)
    return total
g()

# Snippet (C)
fs = [lambda: i for i in range(3)]
fs[0]()

# Snippet (D)
def h(a, b=2, *args, c, **kw):
    return a + b + c + len(kw)
h(1, c=3, d=4)''',
            'run_code': False,
            'options': ['Snippet (D)', 'Snippet (C)', 'Snippet (B)', 'Snippet (A)'],
            'answer': ['C', 'D'],
            'solution': '''A name that is **assigned anywhere** in a function body is local to that function for the whole body (decided at compile time).

- (A) c is keyword-only (after `*args`); the call supplies it, and d=4 goes into kw. Returns 1 + 2 + 3 + 1 = 7. No error.
- (B) The lambdas look up i at call time and see 2; `fs[0]()` returns 2. No error.
- (C) `total += v` assigns total inside `add`, making it local to add; reading it first fails → **UnboundLocalError** (needs `nonlocal total`).
- (D) `x = 6` makes x local to f, so `print(x)` reads an unassigned local → **UnboundLocalError.**

**Trap:** (D) fails even though a global x exists — the local assignment *later* in the body still shadows it from the first line.''',
            'verify': '''_m = {'B': 'C', 'C': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

snips = {'A': "x = 5\\ndef f():\\n    print(x)\\n    x = 6\\nf()",
         'B': "def g():\\n    total = 0\\n    def add(v):\\n        total += v\\n    add(3)\\n    return total\\ng()",
         'C': "fs = [lambda: i for i in range(3)]\\nfs[0]()",
         'D': "def h(a, b=2, *args, c, **kw):\\n    return a + b + c + len(kw)\\nassert h(1, c=3, d=4) == 7"}
import io, contextlib
bad = []
for L, s in snips.items():
    try:
        with contextlib.redirect_stdout(io.StringIO()): exec(s, {})
    except Exception:
        bad.append(L)
assert bad == sorted(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Binary trees — counting shapes of maximum height',
            'text': 'The number of structurally distinct binary trees with **5** nodes whose height (number of edges on the longest root-to-leaf path) is **4** is',
            'options': ['8', '32', '14', '16'],
            'answer': 'D',
            'solution': '''Height 4 with 5 nodes means the longest path already contains all 5 nodes, so the tree is a **path** (every node except the last has exactly one child).

Each of the 4 parent→child links independently goes **left or right** → 2^{4} = **16** distinct trees.

- (A) 8 forgets one link.
- (B) 32 = 2^{5} counts a choice for the leaf too.
- (C) 14 is the Catalan number C₄ (all binary trees with 4 nodes) — irrelevant here.

**Tip:** in general, the number of n-node binary trees of height n − 1 is 2^{n−1}; these are exactly the BSTs produced by insertion orders in which every new key is a new minimum or maximum of the remaining ones.''',
            'verify': '''ANSWER = {'A': 'D', 'D': 'A'}.get(ANSWER, ANSWER)

from functools import lru_cache
@lru_cache(None)
def shapes(n):
    if n == 0: return [None]
    out = []
    for l in range(n):
        for L in shapes(l):
            for R in shapes(n - 1 - l): out.append((L, R))
    return out
def ht(t): return -1 if t is None else 1 + max(ht(t[0]), ht(t[1]))
assert sum(1 for t in shapes(5) if ht(t) == 4) == 16 and ANSWER == 'A'
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'BST — insertion orders of minimum height',
            'text': 'The keys 1, 2, 3, 4, 5, 6 are inserted in some order into an initially empty BST. Of the 720 possible insertion orders, the number that produce a BST of the **minimum possible height** (height = number of edges on the longest root-to-leaf path) is ______.',
            'answer': '80',
            'solution': '''With 6 keys the minimum height is ⌈log₂ 7⌉ − 1 = **2** (a height-2 tree holds at most 7 keys).

**Which roots work?** The two subtrees must each have height ≤ 1, i.e. ≤ 3 keys. With 5 non-root keys, the split must be 2 + 3 or 3 + 2 → root is **3** or **4**.

**Root 3:** left {1, 2} (any order: 2 orders, both give height 1); right {4, 5, 6} must have height 1, so its root must be 5, i.e. 5 is inserted before 4 and 6 → 2 orders. The two subsequences can be interleaved in C(5, 2) = 10 ways. Count = 10 × 2 × 2 = 40.

**Root 4:** symmetric (left {1, 2, 3} needs 2 first; right {5, 6} free) → 40.

Total = 40 + 40 = **80**.

**Trap:** remembering '80' as the classic answer for 7 keys and a *perfect* tree is a coincidence here — derive it: forgetting the interleaving factor C(5, 2) gives only 8.''',
            'solution_diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        3,
                        [
                            1,
                            None,
                            [2],
                        ],
                        [
                            5,
                            [4],
                            [6],
                        ],
                    ],
                    'caption': 'One minimum-height BST (e.g. order 3, 5, 1, 6, 2, 4)',
                },
            ],
            'verify': '''
from itertools import permutations
def ins(t, k):
    if t is None: return [k, None, None]
    if k < t[0]: t[1] = ins(t[1], k)
    else: t[2] = ins(t[2], k)
    return t
def ht(t): return -1 if t is None else 1 + max(ht(t[1]), ht(t[2]))
hs = []
for p in permutations(range(1, 7)):
    t = None
    for k in p: t = ins(t, k)
    hs.append(ht(t))
assert hs.count(min(hs)) == int(ANSWER) and min(hs) == 2
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Dijkstra with a negative edge',
            'text': 'The standard Dijkstra algorithm (a vertex, once extracted, is final and never updated again) is run from **S** on the directed graph below, which has one negative edge B → A. Which of the following statements is/are TRUE?',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['S', 'A', 'B', 'C', 'D'],
                    'edges': [
                        ['S', 'A', 2],
                        ['S', 'B', 4],
                        ['A', 'C', 3],
                        ['B', 'A', -4],
                        ['C', 'D', 2],
                        ['B', 'D', 6],
                    ],
                    'pos': {
                        'S': [0, 1],
                        'A': [2, 2.2],
                        'B': [2, -0.2],
                        'C': [4, 2.2],
                        'D': [4, -0.2],
                    },
                },
            ],
            'options': [
                'Dijkstra reports the correct shortest distance to B',
                'Adding 4 to every edge weight and running Dijkstra yields shortest paths that are also shortest in the original graph',
                'Dijkstra reports the correct shortest distance to D',
                'Dijkstra reports d(A) = 2, whereas the true shortest distance to A is 0',
            ],
            'answer': ['A', 'D'],
            'solution': '''**Dijkstra trace:** extract S (0): A = 2, B = 4. Extract A (2): C = 5. Extract B (4): edge B → A would give 0, but A is already final → ignored; D = 10. Extract C (5): D = 7. Extract D (7).
Reported: A 2, B 4, C 5, D 7.

**True distances** (no negative cycle): A = 4 − 4 = **0** (S→B→A), C = 3, D = 5 (S→B→A→C→D: 4 − 4 + 3 + 2), B = 4.

- (A) d(B) = 4 is correct (no path to B uses the negative edge). **True.**
- (B) After +4: S→B→D costs 8 + 10 = 18, while S→B→A→C→D costs 8 + 0 + 7 + 6 = 21, so Dijkstra picks S→B→D (original cost 10), not the true shortest (cost 5). Adding a constant penalises paths with **more edges**. **False.**
- (C) Reported 7 vs true 5 — the error propagates through C. **False.**
- (D) **True** — A was finalised before B's negative edge was seen.

**Trap:** uniform reweighting is not Johnson's reweighting (which uses vertex potentials w'(u,v) = w(u,v) + h(u) − h(v)).''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Reported vs true distances',
                    'col_labels': ['S', 'A', 'B', 'C', 'D'],
                    'row_labels': ['Dijkstra', 'true'],
                    'rows': [
                        [0, 2, 4, 5, 7],
                        [0, 0, 4, 3, 5],
                    ],
                    'highlight': [
                        [0, 1],
                        [0, 3],
                        [0, 4],
                    ],
                },
            ],
            'verify': '''_m = {'B': 'D', 'D': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

E = [('S','A',2),('S','B',4),('A','C',3),('B','A',-4),('C','D',2),('B','D',6)]
V = 'SABCD'
def dijkstra(E):
    G = {v: [] for v in V}
    for u, v, w in E: G[u].append((v, w))
    d = {v: float('inf') for v in V}; d['S'] = 0; done = set(); par = {}
    while len(done) < len(V):
        u = min((v for v in V if v not in done), key=lambda v: (d[v], v)); done.add(u)
        for v, w in G[u]:
            if v not in done and d[u] + w < d[v]: d[v] = d[u] + w; par[v] = u
    return d, par
d, _ = dijkstra(E)
bf = {v: float('inf') for v in V}; bf['S'] = 0
for _ in range(4):
    for u, v, w in E: bf[v] = min(bf[v], bf[u] + w)
W = {(u, v): w for u, v, w in E}
_, par = dijkstra([(u, v, w + 4) for u, v, w in E])
x, cost = 'D', 0
while x != 'S': cost += W[(par[x], x)]; x = par[x]
truth = {'A': d['B'] == bf['B'], 'B': d['A'] == 2 and bf['A'] == 0,
         'C': d['D'] == bf['D'], 'D': cost == bf['D']}
assert sorted(k for k in truth if truth[k]) == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Divide and conquer — inversion counting',
            'text': 'Inversions of A = [7, 2, 9, 4, 11, 1, 8, 3, 10, 5] are counted by the merge-sort method: the array is split into A[0..4] and A[5..9], each half is sorted recursively (counting its own inversions), and the remaining *split* inversions — pairs (i, j) with i in the left half, j in the right half and A[i] > A[j] — are counted during the **final** merge. The number of inversions counted during that final merge is ______.',
            'answer': '15',
            'solution': '''During a merge, whenever an element y of the right half is output before some remaining left elements, it forms an inversion with **every** remaining left element.

Sorted halves: L = [2, 4, 7, 9, 11], R = [1, 3, 5, 8, 10]. Merge:
- 1 (from R) output while all 5 of L remain → +5
- 2 (L), then 3 (R): L has 4, 7, 9, 11 left → +4
- 4 (L), then 5 (R): 7, 9, 11 left → +3
- 7 (L), then 8 (R): 9, 11 left → +2
- 9 (L), then 10 (R): 11 left → +1
- 11 (L).

Split inversions = 5 + 4 + 3 + 2 + 1 = **15**.

(For completeness: the left half [7, 2, 9, 4, 11] has 3 inversions and the right half [1, 8, 3, 10, 5] has 3, so the total is 21.)

**Trap:** counting the inversions of the whole array (21), or adding +1 per right element instead of +(number of remaining left elements).''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Final merge: right elements and split inversions',
                    'col_labels': ['1', '3', '5', '8', '10'],
                    'row_labels': ['left items still pending'],
                    'rows': [
                        [5, 4, 3, 2, 1],
                    ],
                },
            ],
            'verify': '''
A = [7, 2, 9, 4, 11, 1, 8, 3, 10, 5]
L, R = sorted(A[:5]), sorted(A[5:])
i = j = c = 0
while i < 5 and j < 5:
    if L[i] <= R[j]: i += 1
    else: c += 5 - i; j += 1
assert c == int(ANSWER) == sum(1 for x in A[:5] for y in A[5:] if x > y)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Python — mutable defaults, closures and try/finally',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''def make(n, acc=[]):
    acc.append(n)
    return lambda k: [a * k for a in acc]

f = make(1)
g = make(2)
h = make(3, [])
print(f(10), g(1), h(2))

def t():
    try:
        return f(1)
    finally:
        make(4)

print(t(), g(1))''',
            'options': [
                '`[10, 20] [1, 2] [6]` / `[1, 2] [1, 2, 4]`',
                '`[10] [2] [6]` / `[1] [2]`',
                '`[10, 20] [1, 2] [6]` / `[1, 2, 4] [1, 2, 4]`',
                '`[10, 20] [1, 2] [2, 4, 6]` / `[1, 2] [1, 2, 4]`',
            ],
            'answer': 'A',
            'solution': '''(`/` separates the two output lines.) Three mechanisms interact:

1. `acc=[]` is created **once**; `make(1)` and `make(2)` append to the same list → acc = [1, 2]. `make(3, [])` uses a fresh list [3].
2. Each lambda closes over *its* `acc` object and reads it **when called**. So f and g see the same list [1, 2]: f(10) = [10, 20], g(1) = [1, 2]; h(2) = [6].
3. In `t()`, the `return` expression `f(1)` is evaluated **before** the `finally` block runs: it builds the new list [1, 2]. Then `finally` calls `make(4)`, appending 4 to the shared acc. The already-computed return value is unaffected, but the later `g(1)` sees [1, 2, 4].

Output:
`[10, 20] [1, 2] [6]`
`[1, 2] [1, 2, 4]`

- (B) ignores the shared default list.
- (C) assumes `finally` runs before the return value is computed.
- (D) assumes `make(3, [])` also used the shared list.

**Trap:** `finally` runs after the return expression is evaluated but before the function actually returns; it can mutate shared state (and could even override the return value with its own `return`).''',
            'verify': '''
lines = OUTPUT.strip().splitlines()
assert lines == ['[10, 20] [1, 2] [6]', '[1, 2] [1, 2, 4]'] and ANSWER == 'A'
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Linear probing — dependence on insertion order',
            'text': 'The keys 14, 24, 35, 4, 15 are inserted into an initially empty hash table with slots 0–9 using h(k) = k mod 10 and linear probing (step +1). Of the 5! = 120 possible insertion orders, the number in which key **15** ends up in slot **5** is ______.',
            'answer': '42',
            'solution': '''Keys 14, 24, 4 hash to slot 4; 35 and 15 hash to slot 5. All five end up in the cluster of slots 4–8, and 15 lands in slot 5 **iff slot 5 is still empty when 15 is inserted**.

Who can fill slot 5 before 15?
- 35 (its home slot), or
- a 4-key (14, 24 or 4) that finds slot 4 occupied, i.e. the **second** 4-key to be inserted.

So 15 gets slot 5 iff, among the keys inserted before 15, there is no 35 and at most one 4-key. Let p = number of keys before 15:
- p = 0: 15 first → any order of the other 4: 4! = 24.
- p = 1: the key before 15 is one of the three 4-keys (3 ways); the remaining 3 keys follow in any order (3! = 6) → 18.
- p ≥ 2: impossible (either 35 or a second 4-key precedes 15).

Total = 24 + 18 = **42**.

**Trap:** assuming the first 4-key always takes slot 4 'and blocks nothing' — the second 4-key spills into slot 5 and steals 15's home.''',
            'solution_diagrams': [
                {
                    'type': 'hashtable',
                    'size': 10,
                    'slots': {
                        4: 14,
                        5: 15,
                        6: 24,
                        7: 35,
                        8: 4,
                    },
                    'caption': 'Result for the order 14, 15, 24, 35, 4',
                },
            ],
            'verify': '''
from itertools import permutations
cnt = 0
for p in permutations([14, 24, 35, 4, 15]):
    T = [None] * 10
    for k in p:
        i = k % 10
        while T[i] is not None: i = (i + 1) % 10
        T[i] = k
    cnt += T[5] == 15
assert cnt == int(ANSWER)
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Heaps — structural bounds',
            'text': 'Consider binary heaps on **15 distinct** keys stored in A[0..14] (children of i at 2i+1, 2i+2). Which of the following statements is/are TRUE?',
            'diagrams': [
                {
                    'type': 'heap',
                    'values': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                    'show_index': False,
                    'caption': 'A min-heap on 15 keys (keys 1..15 in level order) — shape reference',
                },
            ],
            'options': [
                'Inserting the keys 1, 2, …, 15 in this order, one at a time, into an initially empty **max**-heap performs 34 swaps in total',
                'Bottom-up build-heap performs at most 11 swaps on any input of 15 keys',
                'In a **min**-heap, the second smallest key is always at index 1 or 2',
                'In a **min**-heap, the largest key can be at index 6',
            ],
            'answer': ['A', 'B', 'C'],
            'solution': '''- (A) Each new key is the largest so far and sifts up to the root, making as many swaps as its depth: depths 0 (1 key), 1 (2 keys), 2 (4 keys), 3 (8 keys) → 0 + 2 + 8 + 24 = **34**. **True.**
- (B) A sift-down from a node of height h makes at most h swaps. Heights: root 3, two nodes 2, four nodes 1, eight leaves 0 → at most 3 + 2·2 + 4·1 = **11** swaps (reached e.g. for ascending input to a max-heap). **True.**
- (C) The second smallest has only one smaller key (the root), so its parent must be the root → index 1 or 2. **True.**
- (D) Index 6 has children 13 and 14, which must be larger than it in a min-heap — so the largest key must be a **leaf** (indices 7–14). **False.**

**Trap:** (B) vs (A) shows why bottom-up build-heap is O(n) while repeated insertion can be Θ(n log n): bottom-up sums *heights* (mostly small), insertion sums *depths* (mostly large).''',
            'verify': '''_m = {'C': 'D', 'D': 'C'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'B', 'B': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

import random
def build_swaps(A):
    A = A[:]; n = len(A); sw = 0
    for i in range(n // 2 - 1, -1, -1):
        j = i
        while True:
            l, r, m = 2 * j + 1, 2 * j + 2, j
            if l < n and A[l] > A[m]: m = l
            if r < n and A[r] > A[m]: m = r
            if m == j: break
            A[j], A[m] = A[m], A[j]; sw += 1; j = m
    return sw
random.seed(3)
mx = max(build_swaps(random.sample(range(15), 15)) for _ in range(3000))
asc = build_swaps(list(range(15)))
H = []; ins_sw = 0
for k in range(1, 16):
    H.append(k); i = len(H) - 1
    while i and H[(i - 1) // 2] < H[i]:
        H[i], H[(i - 1) // 2] = H[(i - 1) // 2], H[i]; i = (i - 1) // 2; ins_sw += 1
pos_max, pos_2nd = set(), set()
for _ in range(3000):
    M = []
    for k in random.sample(range(15), 15):
        M.append(k); i = len(M) - 1
        while i and M[(i - 1) // 2] > M[i]:
            M[i], M[(i - 1) // 2] = M[(i - 1) // 2], M[i]; i = (i - 1) // 2
    pos_max.add(M.index(14)); pos_2nd.add(M.index(1))
truth = {'A': mx <= 11 and asc == 11, 'B': ins_sw == 34,
         'C': 6 in pos_max, 'D': pos_2nd <= {1, 2}}
assert min(pos_max) >= 7
assert sorted(k for k in truth if truth[k]) == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'DFS — counting possible visit orders',
            'text': 'Depth-first search (recursive) is started at **A** on the undirected graph shown below. The order in which a vertex scans its neighbours is **arbitrary** (any order may be used at any vertex). The number of distinct orders in which the five vertices can be first visited is ______.',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['A', 'B', 'C', 'D', 'E'],
                    'edges': [
                        ['A', 'B'],
                        ['A', 'C'],
                        ['A', 'D'],
                        ['B', 'C'],
                        ['C', 'D'],
                        ['C', 'E'],
                        ['D', 'E'],
                    ],
                    'pos': {
                        'A': [0, 1],
                        'B': [1.5, 2.2],
                        'C': [1.5, 1],
                        'D': [1.5, -0.2],
                        'E': [3, 0.4],
                    },
                },
            ],
            'answer': '9',
            'solution': '''DFS always continues from the **most recently discovered** vertex that still has an unvisited neighbour. Branch on A's first choice.

**A → B:** B's only unvisited neighbour is C. From C: D then E (D–E), or E then D. → A B C D E, A B C E D (**2**).

**A → C:** C's unvisited neighbours are B, D, E.
- C → B: B is a dead end; back at C choose D (→ E) or E (→ D): A C B D E, A C B E D.
- C → D → E (E's neighbours C, D visited) → back to C → B: A C D E B.
- C → E → D → back to C → B: A C E D B.
(**4**)

**A → D:** D's unvisited neighbours C, E.
- D → C: then C → B (dead end) → C → E: A D C B E; or C → E first, then B: A D C E B.
- D → E → C → B: A D E C B.
(**3**)

Total = 2 + 4 + 3 = **9**.

**Trap:** orders like A, B, D, … are impossible — after B, DFS must continue from B (to C) before backtracking to A. Not every 'A first' permutation of a connected graph is a DFS order.''',
            'verify': '''
from itertools import permutations, product
E = [('A','B'),('A','C'),('A','D'),('B','C'),('C','D'),('C','E'),('D','E')]
G = {}
for u, v in E: G.setdefault(u, []).append(v); G.setdefault(v, []).append(u)
V = sorted(G)
orders = set()
for choice in product(*[list(permutations(G[v])) for v in V]):
    adj = dict(zip(V, choice)); seen = []
    def dfs(u):
        seen.append(u)
        for w in adj[u]:
            if w not in seen: dfs(w)
    dfs('A'); orders.add(tuple(seen))
assert len(orders) == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Output-restricted deque permutations',
            'text': 'The values 1, 2, 3, 4 arrive in this order. Each arriving value must be inserted into a deque at **either end**; at any time the element at the **front** may be removed and output (removal only at the front). Which of the following output sequences is **impossible**?',
            'diagrams': [
                {
                    'type': 'queue',
                    'values': [2, 1, 3],
                    'caption': 'e.g. after inserting 1, 2 at front, 3 at rear',
                },
            ],
            'options': ['4, 2, 1, 3', '3, 1, 2, 4', '1, 4, 2, 3', '4, 1, 3, 2'],
            'answer': 'D',
            'solution': '''Key invariant: every arriving value is **larger** than everything already in the deque and is placed at an end. Hence the deque contents are always **valley-shaped** — reading front to rear, the values decrease to a minimum and then increase (removing from the front keeps this shape). A sequence starting with 4 needs 1, 2, 3 to be inside the deque, front to rear, in exactly their output order before 4 is added.

- (A) 4, 2, 1, 3: insert 1; 2 at front → [2, 1]; 3 at rear → [2, 1, 3]; 4 at front → output 4, 2, 1, 3. **Possible.**
- (B) 3, 1, 2, 4: [1], 2 at rear → [1, 2], 3 at front → [3, 1, 2]; output 3, 1, 2; then 4. **Possible.**
- (C) 1, 4, 2, 3: insert 1, output 1; [2], 3 at rear → [2, 3], 4 at front → 4, 2, 3. **Possible.**
- (D) 4, 1, 3, 2: the deque would have to read 1, 3, 2 (front to rear) — up then down, a **peak**, not a valley. It can never be built. **Impossible.**

(The only impossible output sequences of length 4 are 4, 1, 3, 2 and 4, 2, 3, 1.)

**Tip:** the valley invariant immediately rules out any sequence 4, a, b, c with a < b > c, which is why 4, 2, 3, 1 is the other impossible sequence.''',
            'verify': '''ANSWER = {'C': 'D', 'D': 'C'}.get(ANSWER, ANSWER)

from functools import lru_cache
from itertools import permutations
def possible(target):
    target = tuple(target)
    @lru_cache(None)
    def go(nxt, dq, k):
        if k == len(target): return True
        if dq and dq[0] == target[k] and go(nxt, dq[1:], k + 1): return True
        if nxt <= 4 and (go(nxt + 1, (nxt,) + dq, k) or go(nxt + 1, dq + (nxt,), k)): return True
        return False
    return go(1, (), 0)
opts = [(4,2,1,3), (3,1,2,4), (4,1,3,2), (1,4,2,3)]
assert [L for L, s in zip('ABCD', opts) if not possible(s)] == [ANSWER]
assert sorted(p for p in permutations(range(1, 5)) if not possible(p)) == [(4,1,3,2), (4,2,3,1)]
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Recurrences — exact operation count',
            'text': 'Consider the following Python program. The value printed is ______.',
            'code': '''c = 0
def f(n):
    global c
    if n <= 1:
        c += 1
        return
    for i in range(n // 2):
        c += 1
    f(n // 2)
    f(n // 2)
    f(n // 2)

f(16)
print(c)''',
            'answer': '146',
            'solution': '''Let T(n) be the final increase of c caused by f(n). From the code:
T(1) = 1, T(n) = n/2 + 3T(n/2).

- T(2) = 1 + 3·1 = 4
- T(4) = 2 + 3·4 = 14
- T(8) = 4 + 3·14 = 46
- T(16) = 8 + 3·46 = **146**

Closed form check: with n = 2^{k}, T(n) = 3^{k} + (n/2)·Σ_{i=0}^{k−1} (3/2)^{i} = 3^{k} + 3^{k} − 2^{k} = 2·3^{k} − 2^{k}; for k = 4: 2·81 − 16 = 146 ✓. Asymptotically T(n) = Θ(n^{log₂ 3}) ≈ Θ(n^{1.585}) (master theorem, case 1).

**Trap:** the loop runs n//2 times (not n), and leaves contribute 1 each (3^{4} = 81 leaves).''',
            'verify': '''
assert int(OUTPUT.strip()) == int(ANSWER) == 2 * 3 ** 4 - 2 ** 4
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Reversing a linked list that contains a cycle',
            'text': 'A singly linked list has nodes with values 1, 2, 3, 4, 5, 6 linked in this order, and node 6 points back to node 3 (see figure). The standard iterative reversal below is applied with `head` = node 1. Which of the following statements is/are TRUE?',
            'code': '''prev, cur, steps = None, head, 0
while cur:
    cur.nxt, prev, cur = prev, cur, cur.nxt
    steps += 1
head = prev''',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['1', '2', '3', '4', '5', '6'],
                    'edges': [
                        ['1', '2'],
                        ['2', '3'],
                        ['3', '4'],
                        ['4', '5'],
                        ['5', '6'],
                        ['6', '3'],
                    ],
                    'pos': {
                        '1': [0, 0],
                        '2': [1.3, 0],
                        '3': [2.6, 0],
                        '4': [3.6, 1.2],
                        '5': [4.8, 0.6],
                        '6': [3.8, -1],
                    },
                },
            ],
            'options': [
                'After the loop, `head` refers to the node with value 1',
                'The loop body executes exactly 9 times',
                'The loop terminates',
                'After the loop, following `nxt` from `head` visits 1, 2, 3, 4, 5, 6, 3, …',
            ],
            'answer': ['A', 'B', 'C'],
            'solution': '''Trace (each line: node processed → its new nxt; then prev, cur):

- 1: 1.nxt = None; cur → 2
- 2: 2.nxt = 1; cur → 3
- 3: 3.nxt = 2; cur → 4
- 4: 4.nxt = 3; cur → 5
- 5: 5.nxt = 4; cur → 6
- 6: 6.nxt = 5; cur → **3** (6's old nxt)
- 3 again: its current nxt is 2 (set in step 3), so cur → 2; 3.nxt = 6
- 2 again: cur → 1; 2.nxt = 3
- 1 again: cur → None (1.nxt was set to None); 1.nxt = 2. Loop ends.

9 iterations; prev = node 1. Final links: 1 → 2 → 3 → 6 → 5 → 4 → 3 (cycle).

- (A) **True** — reversing a ρ-shaped list returns the original head.
- (B) **True** — 9 = 2μ + λ + 1 with tail length μ = 2 and cycle length λ = 4 (the tail is walked twice, the cycle once).
- (C) **True** — the walk re-enters the tail and follows the already-reversed tail links back to the head, whose nxt is None.
- (D) **False** — the tail 1 → 2 → 3 is restored, but the **cycle is reversed**: 3 → 6 → 5 → 4 → 3.

**Tip:** comparing the returned head with the original head is a (slow) way to detect a cycle with O(1) extra space.''',
            'solution_diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['1', '2', '3', '4', '5', '6'],
                    'edges': [
                        ['1', '2'],
                        ['2', '3'],
                        ['3', '6'],
                        ['6', '5'],
                        ['5', '4'],
                        ['4', '3'],
                    ],
                    'pos': {
                        '1': [0, 0],
                        '2': [1.3, 0],
                        '3': [2.6, 0],
                        '4': [3.6, 1.2],
                        '5': [4.8, 0.6],
                        '6': [3.8, -1],
                    },
                    'caption': 'Links after the loop: the cycle direction is reversed',
                },
            ],
            'verify': '''_m = {'B': 'A', 'A': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'C', 'C': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

class Node:
    def __init__(s, v): s.v, s.nxt = v, None
ns = [Node(i) for i in range(1, 7)]
for a, b in zip(ns, ns[1:]): a.nxt = b
ns[5].nxt = ns[2]
head = ns[0]
prev, cur, steps = None, head, 0
while cur and steps < 100:
    cur.nxt, prev, cur = prev, cur, cur.nxt
    steps += 1
walk, h = [], prev
for _ in range(7): walk.append(h.v); h = h.nxt
truth = {'A': cur is None, 'B': prev is ns[0], 'C': steps == 9,
         'D': walk == [1, 2, 3, 4, 5, 6, 3]}
assert walk == [1, 2, 3, 6, 5, 4, 3]
assert sorted(k for k in truth if truth[k]) == sorted(ANSWER)
''',
            'run_code': False,
        },
    ],
}
