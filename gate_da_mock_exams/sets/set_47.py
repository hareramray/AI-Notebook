# Set 47 — Challenge Mock — Paper 2
SET = {
    'number': 47,
    'title': 'Challenge Mock — Paper 2',
    'difficulty': 'Hard',
    'focus': 'hardest, multi-concept, trap-heavy 2-mark questions',
    'questions': [
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Python — `+=` vs `+` on lists, identity',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''a = [1, 2]
b = a
a += [3]
c = a
a = a + [4]
print(b, c is b, a is c, len(a))''',
            'options': [
                '`[1, 2] False False 4`',
                '`[1, 2, 3] True True 4`',
                '`[1, 2, 3] True False 4`',
                '`[1, 2, 3, 4] True True 4`',
            ],
            'answer': 'C',
            'solution': '''For lists, `a += x` calls `list.__iadd__`, which **extends the same object in place**; `a = a + x` builds a **new** list and rebinds `a` to it.

- `b = a`: b and a name the same list [1, 2].
- `a += [3]`: that shared list becomes [1, 2, 3] — b sees it.
- `c = a`: c is the same object as b.
- `a = a + [4]`: a now names a new list [1, 2, 3, 4]; b and c still name the old one.

So b = [1, 2, 3], `c is b` → True, `a is c` → False, len(a) = 4.

- (A) treats `+=` as creating a new list (true for tuples/strings, not lists).
- (B) treats `a = a + [4]` as in-place.
- (D) treats both operations as in-place.

**Trap:** `x += y` and `x = x + y` are equivalent only for immutable types.''',
            'verify': "ANSWER = {'B': 'C', 'C': 'B'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == '[1, 2, 3] True False 4' and ANSWER == 'B'",
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Python — try/except/finally and return',
            'text': 'The value printed by the following Python program is ______.',
            'code': '''def f(n):
    try:
        if n % 2:
            return n * 10
        raise ValueError
    except ValueError:
        return n + 1
    finally:
        if n > 5:
            return -n

print(sum(f(k) for k in range(8)))''',
            'answer': '86',
            'solution': '''The `finally` block runs on every exit path. If it executes its own `return`, that value **replaces** whatever the `try` or `except` block was returning.

- n = 0: even → ValueError → except returns 1; finally (0 > 5 false) → **1**
- n = 1: odd → return 10 → **10**
- n = 2: → **3**
- n = 3: → **30**
- n = 4: → **5**
- n = 5: → **50**
- n = 6: except would return 7, but finally returns **−6**
- n = 7: try would return 70, but finally returns **−7**

Sum = 1 + 10 + 3 + 30 + 5 + 50 − 6 − 7 = **86**.

**Trap:** assuming `return` ends the function immediately. With n > 5 the pending return value (7 or 70) is discarded; ignoring `finally` would give 176.''',
            'verify': 'assert OUTPUT.strip() == ANSWER',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Input-restricted deque permutations',
            'text': 'An **input-restricted deque** allows insertion only at the rear but deletion at both ends. The values 1, 2, 3, 4 are inserted in this order; deletions may be interleaved with insertions, and each deleted value is output at once. Which of the following output sequences is/are possible?',
            'options': ['3, 1, 4, 2', '4, 2, 1, 3', '4, 1, 3, 2', '4, 2, 3, 1'],
            'answer': ['A', 'C'],
            'solution': '''When the first output is 4, all of 1, 2, 3, 4 have already been inserted, in order, so the deque is [1, 2, 3, 4] and afterwards only the two **ends** can be removed.

- (A) Insert 1, 2, 3 → [1,2,3]; delete rear 3; delete front 1 → [2]; insert 4 → [2,4]; delete rear 4; delete 2. **Possible.** (This sequence is *impossible* for a stack — the deque's extra front deletion makes it reachable.)
- (B) After 4 the deque is [1, 2, 3]; 2 is in the middle — neither end. **Impossible.**
- (C) [1,2,3,4]: delete rear 4 → [1,2,3]; delete front 1 → [2,3]; delete rear 3; then 2. **Possible.**
- (D) Again 2 would have to leave from the middle of [1, 2, 3]. **Impossible.**

In fact, of the 24 permutations of 1..4, exactly these two (4,2,1,3 and 4,2,3,1) cannot be produced by an input-restricted deque.

**Trap:** applying the stack rule (forbidden 3-1-2 pattern) — it rejects (A) wrongly.''',
            'verify': '''_m = {'A': 'C', 'C': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

import itertools
def possible(seq):
    n = len(seq); st = [(1, (), 0)]; seen = set()
    while st:
        nx, dq, oi = st.pop()
        if oi == n: return True
        if (nx, dq, oi) in seen: continue
        seen.add((nx, dq, oi))
        if nx <= n: st.append((nx + 1, dq + (nx,), oi + 0))
        if dq and dq[0] == seq[oi]: st.append((nx, dq[1:], oi + 1))
        if dq and dq[-1] == seq[oi]: st.append((nx, dq[:-1], oi + 1))
    return False
opts = [(4,1,3,2),(4,2,1,3),(3,1,4,2),(4,2,3,1)]
assert [L for L, s in zip('ABCD', opts) if possible(s)] == sorted(ANSWER)
assert [p for p in itertools.permutations(range(1, 5)) if not possible(p)] == [(4,2,1,3),(4,2,3,1)]
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Linear probing — expected probes',
            'text': 'A hash table with 10 slots (0–9) uses linear probing. Slots 1, 2, 3, 6 and 8 are occupied and the rest are empty, as shown. A new key is inserted whose home slot is uniformly distributed over 0–9. Counting every slot examined (including the one where the key is placed), the expected number of probes for this insertion is ______ (rounded off to two decimal places).',
            'diagrams': [
                {
                    'type': 'hashtable',
                    'size': 10,
                    'slots': {
                        1: 31,
                        2: 52,
                        3: 13,
                        6: 96,
                        8: 78,
                    },
                    'caption': 'Current table',
                },
            ],
            'answer': ['1.79', '1.81'],
            'solution': '''With linear probing, a key whose home slot lies inside a run of occupied slots must walk to the end of the run. Probes needed for each home slot h:

- h = 0: empty → 1
- h = 1: 1, 2, 3 full, 4 empty → 4
- h = 2: → 3
- h = 3: → 2
- h = 4: → 1
- h = 5: → 1
- h = 6: 6 full, 7 empty → 2
- h = 7: → 1
- h = 8: 8 full, 9 empty → 2
- h = 9: → 1

Total = 1 + 4 + 3 + 2 + 1 + 1 + 2 + 1 + 2 + 1 = 18; expected = 18/10 = **1.80**.

Notice also that slot 4 receives the key with probability 4/10 (home slots 1–4) while slot 5 gets only 1/10 — long runs grow faster (primary clustering).

**Trap:** using the load-factor formula ½(1 + 1/(1 − α)²) = ½(1 + 4) = 2.5 — that is an asymptotic average over *random* tables, not this specific table.''',
            'verify': '''
occ = {1, 2, 3, 6, 8}; tot = 0
for h in range(10):
    i, c = h, 1
    while i in occ: i = (i + 1) % 10; c += 1
    tot += c
assert float(ANSWER[0]) <= tot / 10 <= float(ANSWER[1])
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'BST — insertion orders',
            'text': 'How many permutations of the keys 1, 2, 3, 4, 5, when inserted in that order into an initially empty BST, produce exactly the tree shown?',
            'diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        3,
                        [
                            2,
                            [1],
                            None,
                        ],
                        [
                            4,
                            None,
                            [5],
                        ],
                    ],
                    'caption': 'Target BST',
                },
            ],
            'options': ['6', '4', '8', '12'],
            'answer': 'A',
            'solution': '''A permutation produces this tree iff every node is inserted **before all its descendants**. Here that means: 3 first; 2 before 1; 4 before 5. Keys in different subtrees of 3 can be interleaved freely.

- The root 3 must come first.
- The left subtree sequence is forced: (2, 1). The right subtree sequence is forced: (4, 5).
- Interleavings of two fixed sequences of length 2 and 2: C(4, 2) = **6**.

They are: 3 2 1 4 5, 3 2 4 1 5, 3 2 4 5 1, 3 4 2 1 5, 3 4 2 5 1, 3 4 5 2 1.

General rule: ways(T) = C(|L| + |R|, |L|) · ways(L) · ways(R).

- (B) 4 forgets some interleavings. (C) 8 and (D) 12 allow 1 before 2 or 5 before 4, which would change the shape.

**Trap:** thinking the order must be level-order; any topological order of the tree (parents before children) works.''',
            'verify': '''ANSWER = {'B': 'A', 'A': 'B'}.get(ANSWER, ANSWER)

import itertools
def ins(t, k):
    if t is None: return [k, None, None]
    if k < t[0]: t[1] = ins(t[1], k)
    else: t[2] = ins(t[2], k)
    return t
target = [3, [2, [1, None, None], None], [4, None, [5, None, None]]]
cnt = 0
for p in itertools.permutations(range(1, 6)):
    t = None
    for k in p: t = ins(t, k)
    cnt += t == target
assert cnt == 6 and ['4','6','8','12'][ord(ANSWER) - 65] == '6'
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Binary search — worst-case iterations',
            'text': 'The standard iterative binary search (lo = 0, hi = n − 1; while lo ≤ hi: mid = ⌊(lo + hi)/2⌋; compare; move lo or hi past mid) is run on a sorted array of n distinct keys. The **smallest** n for which some search (successful or unsuccessful) can execute the loop body 8 times is ______.',
            'answer': '128',
            'solution': '''The loop examines the nodes of an implicit, height-balanced decision tree on n keys. Its worst case equals the number of levels, ⌊log₂ n⌋ + 1, and an unsuccessful search never takes more iterations than that (it ends just below a node on the deepest level).

We need ⌊log₂ n⌋ + 1 ≥ 8, i.e. ⌊log₂ n⌋ ≥ 7, i.e. n ≥ 2⁷ = **128**.

Check: with n = 127 the tree is perfect with 7 levels (2⁷ − 1 nodes), so every search ends within 7 iterations. Adding one key (n = 128) creates an 8th level containing one node.

**Trap:** answering 255 or 256 (confusing “at most 8” with “at least 8”), or 127 (the largest n for which 7 iterations always suffice).''',
            'verify': '''
def worst(n):
    w = 0
    for x in range(-1, 2 * n + 1):            # keys are 0, 2, 4, ...; odd x are misses
        lo, hi, c = 0, n - 1, 0
        while lo <= hi:
            mid = (lo + hi) // 2; c += 1
            if 2 * mid == x: break
            if 2 * mid < x: lo = mid + 1
            else: hi = mid - 1
        w = max(w, c)
    return w
assert worst(127) == 7 and worst(128) == 8 and int(ANSWER) == 128
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Graph theory — edges forcing connectivity',
            'text': 'What is the minimum number m such that **every** simple undirected graph on 10 vertices with m edges is connected?',
            'options': ['9', '37', '36', '45'],
            'answer': 'B',
            'solution': '''Find the largest number of edges a **disconnected** simple graph on 10 vertices can have; m is one more than that.

A disconnected graph splits into parts of sizes k and 10 − k with no edges between them, so it has at most C(k, 2) + C(10 − k, 2) edges, maximised at the extreme split k = 1: an isolated vertex plus K₉ → C(9, 2) = 36 edges.

So 36 edges do not guarantee connectivity (K₉ + isolated vertex), but any graph with **37** edges must be connected.

- (A) 9 = n − 1 is the minimum number of edges in *some* connected graph (a tree), not a guarantee.
- (C) 36 is the largest disconnected case.
- (D) 45 = C(10, 2) is the complete graph.

**Trap:** confusing “can be connected” (n − 1 edges) with “must be connected” (C(n − 1, 2) + 1 edges).''',
            'verify': '''ANSWER = {'C': 'B', 'B': 'C'}.get(ANSWER, ANSWER)

mx = max(k*(k-1)//2 + (10-k)*(9-k)//2 for k in range(1, 10))
assert mx == 36 and ['9','36','37','45'][ord(ANSWER) - 65] == str(mx + 1)
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Stability depends on the comparison',
            'text': 'Which of the following sorting procedures is/are **stable**?',
            'options': [
                'Merge sort whose merge takes from the left run only when `L[i] <= R[j]`',
                'Quicksort with Lomuto partitioning (pivot = last element, `a[j] <= pivot` goes left)',
                'Bubble sort that swaps adjacent elements when `A[j] >= A[j+1]`',
                'Insertion sort that shifts A[j] right while `A[j] > key`',
            ],
            'answer': ['A', 'D'],
            'solution': '''A sort is stable if records with equal keys keep their input order. Whether an implementation is stable often hinges on a single `<` versus `<=`.

- (A) **Stable.** On ties the merge takes from the **left** run, which holds the earlier records. (With strict `<` it would take from the right on ties and be unstable.)
- (B) **Not stable.** The final pivot swap is a long-range exchange. Input [(1,a), (1,b), (0,c)]: pivot key 0, nothing goes left, and the pivot swap exchanges positions 0 and 2 → [(0,c), (1,b), (1,a)]. The recursive call on [(1,b), (1,a)] leaves it unchanged, so the 1-records come out as b, a — reversed.
- (C) **Not stable.** With `>=`, two adjacent equal keys are swapped, reversing their order; e.g. (1,'x'), (1,'y') becomes (1,'y'), (1,'x').
- (D) **Stable.** The key stops at the first element ≤ it, so it never jumps over an equal key.

**Trap:** classifying algorithms as stable/unstable without looking at the exact comparison.''',
            'verify': '''_m = {'B': 'A', 'A': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'B': 'C', 'C': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

import itertools
def ins(a):
    a = a[:]
    for i in range(1, len(a)):
        k = a[i]; j = i - 1
        while j >= 0 and a[j][0] > k[0]: a[j+1] = a[j]; j -= 1
        a[j+1] = k
    return a
def bub(a):
    a = a[:]
    for i in range(len(a)):
        for j in range(len(a) - 1 - i):
            if a[j][0] >= a[j+1][0]: a[j], a[j+1] = a[j+1], a[j]
    return a
def ms(a):
    if len(a) <= 1: return a
    m = len(a) // 2; L, R = ms(a[:m]), ms(a[m:]); o = []; i = j = 0
    while i < len(L) and j < len(R):
        if L[i][0] <= R[j][0]: o.append(L[i]); i += 1
        else: o.append(R[j]); j += 1
    return o + L[i:] + R[j:]
def qs(a):
    a = a[:]
    def part(lo, hi):
        p = a[hi][0]; i = lo - 1
        for j in range(lo, hi):
            if a[j][0] <= p: i += 1; a[i], a[j] = a[j], a[i]
        a[i+1], a[hi] = a[hi], a[i+1]; return i + 1
    def rec(lo, hi):
        if lo < hi: q = part(lo, hi); rec(lo, q - 1); rec(q + 1, hi)
    rec(0, len(a) - 1); return a
def stable(f):
    for n in range(1, 6):
        for keys in itertools.product(range(3), repeat=n):
            recs = [(k, i) for i, k in enumerate(keys)]
            if f(recs) != sorted(recs): return False
    return True
assert [L for L, f in zip('ABCD', (ins, bub, ms, qs)) if stable(f)] == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Counting heaps',
            'text': 'The number of distinct binary max-heaps that can be built with the six distinct keys 1, 2, 3, 4, 5, 6 is ______.',
            'answer': '20',
            'solution': '''The shape of a 6-node heap is fixed (complete binary tree): the root's left subtree has 3 nodes (a root with two children) and the right subtree has 2 nodes (a root with one left child).

- The root must be 6.
- Choose which 3 of the remaining 5 keys go to the left subtree: C(5, 3) = 10. The other 2 go right.
- Left subtree (3 nodes): its largest key is its root; the other two can be placed in 2 ways → 2.
- Right subtree (2 nodes): the larger is the parent, the smaller the child → 1 way.

Total = 10 × 2 × 1 = **20**.

Recurrence: H(n) = C(n − 1, L) · H(L) · H(R), where L, R are the subtree sizes of the complete tree. (For comparison H(7) = C(6, 3)·2·2 = 80.)

**Trap:** assuming both subtrees have the same size (as for 7 nodes) or that the 2-node subtree allows 2 arrangements — the single child position is forced.''',
            'solution_diagrams': [
                {
                    'type': 'heap',
                    'values': [6, 5, 4, 2, 3, 1],
                    'caption': 'One of the 20 heaps (left subtree {5,2,3}, right {4,1})',
                },
            ],
            'verify': '''
import itertools
c = sum(1 for p in itertools.permutations(range(1, 7))
        if all(p[(i-1)//2] > p[i] for i in range(1, 6)))
assert c == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Python — multi-pass stable sorting',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''data = ['b2', 'a3', 'c1', 'a1', 'b3', 'c2']
data.sort(key=lambda s: s[1])
data.sort(key=lambda s: s[0], reverse=True)
print(data)''',
            'options': [
                "`['c2', 'c1', 'b3', 'b2', 'a3', 'a1']`",
                "`['c1', 'c2', 'b2', 'b3', 'a1', 'a3']`",
                "`['c1', 'c2', 'b3', 'b2', 'a1', 'a3']`",
                "`['a1', 'a3', 'b2', 'b3', 'c1', 'c2']`",
            ],
            'answer': 'B',
            'solution': '''Python's sort is **stable**, and `reverse=True` keeps stability: elements with equal keys stay in their original relative order (the sort does *not* simply reverse the stable ascending result).

- Pass 1 (by digit): 1s: c1, a1; 2s: b2, c2; 3s: a3, b3 → `['c1', 'a1', 'b2', 'c2', 'a3', 'b3']`
- Pass 2 (by letter, descending): c-group in current order c1, c2; b-group b2, b3; a-group a1, a3 → `['c1', 'c2', 'b2', 'b3', 'a1', 'a3']`

Net effect: letters descending, digits ascending within a letter — the classic “sort by secondary key first, then by primary key” idiom.

- (A) assumes `reverse=True` reverses ties too (it would if you sorted ascending and then called `reverse()`).
- (C) mixes the two behaviours.
- (D) ignores `reverse=True`.

**Trap:** `sorted(x, reverse=True)` ≠ `sorted(x)[::-1]` when there are ties.''',
            'verify': '''ANSWER = {'A': 'B', 'B': 'A'}.get(ANSWER, ANSWER)

assert OUTPUT.strip() == "['c1', 'c2', 'b2', 'b3', 'a1', 'a3']" and ANSWER == 'A'
d2 = sorted(sorted(['b2','a3','c1','a1','b3','c2'], key=lambda s: s[1]), key=lambda s: s[0])[::-1]
assert d2 == ['c2', 'c1', 'b3', 'b2', 'a3', 'a1']
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Counting topological orders',
            'text': 'The number of distinct topological orderings of the directed acyclic graph shown is ______.',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
                    'edges': [
                        ['A', 'B'],
                        ['A', 'C'],
                        ['B', 'D'],
                        ['C', 'D'],
                        ['C', 'E'],
                        ['D', 'F'],
                        ['E', 'F'],
                        ['B', 'G'],
                    ],
                    'pos': {
                        'A': [0, 1],
                        'B': [1.6, 2],
                        'C': [1.6, 0],
                        'D': [3.2, 1],
                        'E': [3.2, -0.6],
                        'F': [4.8, 0.4],
                        'G': [3.2, 2.6],
                    },
                },
            ],
            'answer': '21',
            'solution': '''Strategy: fix the forced parts, count the core, then insert the “loose” vertex G.

**Forced:** A is the only source → first. F must follow D and E, and D, E follow B and C (D after B, C; E after C), so among {B, C, D, E, F}, F is last.

**Core {B, C, D, E}** with B → D, C → D, C → E:

- B first: then C must precede D and E → B C D E, B C E D (2)
- C first: remaining B, D, E with B before D → C B D E, C B E D, C E B D (3)

So 5 orders of B, C, D, E (each followed by F).

**Insert G** (only constraint: after B) into the 6 gaps of each 5-element sequence X₁…X₅ — the gaps after B number 6 − pos(B):

- B C D E F: pos 1 → 5
- B C E D F: → 5
- C B D E F: pos 2 → 4
- C B E D F: → 4
- C E B D F: pos 3 → 3

Total = 5 + 5 + 4 + 4 + 3 = **21**.

**Trap:** multiplying independent-looking counts (e.g. 5 × 6 = 30) — G's options depend on where B sits in each order.''',
            'verify': '''
import itertools
E = [('A','B'),('A','C'),('B','D'),('C','D'),('C','E'),('D','F'),('E','F'),('B','G')]
cnt = sum(1 for p in itertools.permutations('ABCDEFG')
          if all(p.index(u) < p.index(v) for u, v in E))
assert cnt == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Generators + closures + default arguments',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''def gen():
    fs = []
    for i in range(3):
        fs.append(lambda x, i=i: x + i)
        fs.append(lambda x: x * i)
        yield len(fs)
    yield [f(2) for f in fs]

g = gen()
next(g)
print(next(g), list(g))''',
            'options': [
                '`4 [[2, 4, 3, 4, 4, 4]]`',
                '`4 [6, [2, 0, 3, 2, 4, 4]]`',
                '`2 [4, 6, [2, 4, 3, 4, 4, 4]]`',
                '`4 [6, [2, 4, 3, 4, 4, 4]]`',
            ],
            'answer': 'D',
            'solution': '''Two independent traps: (1) a generator resumes where it paused, and `list(g)` collects **all remaining** yields; (2) `i=i` freezes the current value in a default argument, while the plain lambda looks `i` up when called (late binding).

**Generator progress:**

- first `next(g)`: i = 0, two lambdas appended, yields 2 (discarded)
- second `next(g)`: i = 1, yields **4** (printed first)
- `list(g)`: i = 2, yields 6; loop ends; yields the list of results; then stops → [6, [ … ]]

**The list** is computed after the loop, when i = 2:

- i=0 pair: 2 + 0 = 2, and 2 × i = 2 × 2 = 4
- i=1 pair: 2 + 1 = 3, and 4
- i=2 pair: 2 + 2 = 4, and 4

→ [2, 4, 3, 4, 4, 4]. Output: `4 [6, [2, 4, 3, 4, 4, 4]]`.

- (A) forgets the third `yield len(fs)`.
- (B) evaluates the plain lambdas with the i of their creation (no late binding).
- (C) prints the discarded first yield as well.

**Tip:** the generator's frame (and its `i`) stays alive until exhausted, which is why the plain lambdas see i = 2.''',
            'verify': "ANSWER = {'A': 'D', 'D': 'A'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == '4 [6, [2, 4, 3, 4, 4, 4]]' and ANSWER == 'A'",
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Dijkstra with a negative edge',
            'text': "Dijkstra's algorithm is run from S on the directed graph shown, which has one negative edge (A → B, weight −4) and no negative cycle. Implementation: repeatedly extract the non-finalized vertex with the smallest d (ties alphabetically), finalize it, and relax **all** its outgoing edges — d of an already-finalized vertex may still decrease, but a finalized vertex is never extracted again. Which of the following statements is/are TRUE?",
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['S', 'A', 'B', 'C', 'D'],
                    'edges': [
                        ['S', 'A', 5],
                        ['S', 'B', 2],
                        ['A', 'B', -4],
                        ['B', 'C', 3],
                        ['C', 'D', 2],
                        ['A', 'D', 6],
                    ],
                    'pos': {
                        'S': [0, 1],
                        'A': [2, 2.2],
                        'B': [2, -0.2],
                        'C': [4, -0.2],
                        'D': [4, 2.2],
                    },
                },
            ],
            'options': [
                'Bellman–Ford on this graph would report a negative-weight cycle',
                'The final value d[B] equals the true shortest distance from S to B',
                'The final value d[C] is 5, whereas the true distance to C is 4',
                'Exactly one vertex ends with an incorrect d value',
            ],
            'answer': ['B', 'C'],
            'solution': '''**Dijkstra trace:**

- Extract S (0): d[A] = 5, d[B] = 2.
- Extract B (2): d[C] = 5.
- Extract A (5; tie with C, A first): d[B] = min(2, 5 − 4) = **1** (B is already finalized — its value changes but it is never re-processed); d[D] = 11.
- Extract C (5): d[D] = min(11, 7) = 7.
- Extract D (7).

Final: S 0, A 5, B 1, C 5, D 7.

**True distances** (Bellman–Ford): S 0, A 5, B = 5 − 4 = 1, C = 1 + 3 = 4, D = 4 + 2 = 6.

- (A) **False** — the graph has no directed cycle at all, so there is no negative cycle; Bellman–Ford simply returns the true distances.
- (B) **True** — d[B] = 1 is correct, but only because the late relaxation from A updated it.
- (C) **True** — C was relaxed from B while d[B] was still 2, and the improvement of B never propagated: d[C] = 5 vs 4.
- (D) **False** — both C (5 vs 4) and D (7 vs 6) are wrong.

**Trap:** believing Dijkstra fails only at the endpoint of the negative edge — the damage is in everything *downstream* of it.''',
            'verify': '''_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'C', 'C': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'B', 'B': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

G = {'S':[('A',5),('B',2)],'A':[('B',-4),('D',6)],'B':[('C',3)],'C':[('D',2)],'D':[]}
INF = float('inf'); d = {v: INF for v in G}; d['S'] = 0; done = set()
while len(done) < len(G):
    u = min(sorted(v for v in G if v not in done), key=lambda v: d[v]); done.add(u)
    for v, w in G[u]:
        if d[u] + w < d[v]: d[v] = d[u] + w
bf = {v: INF for v in G}; bf['S'] = 0
for _ in range(len(G) - 1):
    for u in G:
        for v, w in G[u]:
            if bf[u] + w < bf[v]: bf[v] = bf[u] + w
neg = any(bf[u] + w < bf[v] for u in G for v, w in G[u])
vals = [d['B'] == bf['B'], d['C'] == 5 and bf['C'] == 4,
        sum(d[v] != bf[v] for v in G) == 1, neg]
assert [L for L, v in zip('ABCD', vals) if v] == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Counting BSTs by height',
            'text': 'Consider all binary search trees containing exactly the keys 1, 2, …, 7. The height of a tree is the number of edges on its longest root-to-leaf path. The number of these BSTs whose height is **exactly 3** is ______.',
            'answer': '68',
            'solution': '''Let N(n, h) = number of BSTs on n keys with height ≤ h (empty tree has height −1, so N(0, h) = 1 for h ≥ −1). Choosing root i splits the keys into i − 1 and n − i:

N(n, h) = ∑_{i=1}^{n} N(i − 1, h − 1) · N(n − i, h − 1).

Answer = N(7, 3) − N(7, 2).

**Height ≤ 2** (at most 7 nodes in 3 levels), for n = 0..7:
N(n, 2) = 1, 1, 2, 5, 6, 6, 4, 1.

(e.g. n = 4: of the 14 BSTs, the 8 “paths” have height 3, leaving 6; n = 7: only the perfect tree.)

**Height ≤ 3**, n = 7: sum over root position, left size L = 0..6, right size 6 − L:

- L = 0, 6: 1 × 4 = 4 each
- L = 1, 5: 1 × 6 = 6 each
- L = 2, 4: 2 × 6 = 12 each
- L = 3: 5 × 5 = 25

N(7, 3) = 4 + 6 + 12 + 25 + 12 + 6 + 4 = 69.

Since N(7, 2) = 1 (the perfect tree), the count with height exactly 3 is 69 − 1 = **68**.

**Trap:** forgetting to subtract the height-2 tree, or using node-count height (where “height 3” would mean something else).''',
            'solution_diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        4,
                        [
                            2,
                            [1],
                            [3],
                        ],
                        [
                            5,
                            None,
                            [
                                6,
                                None,
                                [7],
                            ],
                        ],
                    ],
                    'caption': 'One BST of height 3',
                },
            ],
            'verify': '''
from functools import lru_cache
@lru_cache(None)
def shapes(lo, hi):
    if lo > hi: return [None]
    out = []
    for r in range(lo, hi + 1):
        for L in shapes(lo, r - 1):
            for R in shapes(r + 1, hi): out.append((r, L, R))
    return out
def h(t): return -1 if t is None else 1 + max(h(t[1]), h(t[2]))
T = shapes(1, 7)
assert len(T) == 429 and sum(h(t) == 3 for t in T) == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Unbalanced divide-and-conquer recurrences',
            'text': '''Consider (with T(n) = 1 for n ≤ 1)

T₁(n) = T₁(⌊n/2⌋) + T₁(⌊n/3⌋) + n
T₂(n) = T₂(⌊n/4⌋) + T₂(⌊3n/4⌋) + n

Which one of the following is correct?''',
            'options': [
                'T₁(n) = Θ(n) and T₂(n) = Θ(n)',
                'T₁(n) = Θ(n log n) and T₂(n) = Θ(n log n)',
                'T₁(n) = Θ(n) and T₂(n) = Θ(n log n)',
                'T₁(n) = Θ(n log n) and T₂(n) = Θ(n²)',
            ],
            'answer': 'C',
            'solution': '''Use the recursion tree: the work at a level is n times the sum of the fractions raised to the level number.

**T₁:** the subproblem sizes n/2 + n/3 = (5/6)n. Level i costs at most (5/6)^{i}·n, a geometric series: total ≤ n · 1/(1 − 5/6) = 6n. With the root alone costing n, T₁(n) = **Θ(n)**.

**T₂:** n/4 + 3n/4 = n, so every full level costs exactly n. The shortest root-to-leaf path (always taking n/4) has log₄ n levels and the longest log_{4/3} n levels — both Θ(log n). Hence T₂(n) = **Θ(n log n)** (like a merge sort with a 1:3 split).

Numerical check: T₁(n)/n rises towards the bound 6 (5.1 at n = 10⁴, 5.7 at n = 10⁶), while T₂(n)/(n log₂ n) settles near a constant (≈ 1.2) and T₂(n)/n keeps growing.

- (A) treats T₂ like T₁ — but its fractions sum to exactly 1.
- (B) treats T₁ like a balanced split — but the fractions sum to less than 1.
- (D) confuses an unbalanced *constant-fraction* split with quicksort's worst case T(n) = T(n − 1) + n.

**Tip:** for T(n) = ∑ T(αᵢ n) + n: ∑ αᵢ < 1 → Θ(n); = 1 → Θ(n log n); > 1 → polynomially larger.''',
            'verify': '''ANSWER = {'A': 'C', 'C': 'A'}.get(ANSWER, ANSWER)

import math, sys
sys.setrecursionlimit(10000)
from functools import lru_cache
@lru_cache(None)
def T1(n): return 1 if n <= 1 else T1(n // 2) + T1(n // 3) + n
@lru_cache(None)
def T2(n): return 1 if n <= 1 else T2(n // 4) + T2(3 * n // 4) + n
a = [T1(n) / n for n in (10**4, 10**5, 10**6)]
b = [T2(n) / (n * math.log2(n)) for n in (10**4, 10**5, 10**6)]
c = [T2(n) / n for n in (10**4, 10**6)]
assert max(a) < 6 and (a[2] - a[1]) < (a[1] - a[0])          # bounded, converging to 6
assert max(b) - min(b) < 0.1 and c[1] > c[0] * 1.3
assert ANSWER == 'A'
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Linear probing with deletion (tombstones)',
            'text': '''A hash table of size 11 uses h(k) = k mod 11 with linear probing. Deletion replaces a key by a tombstone **DEL**. Insertion places the key in the first slot on its probe sequence that is empty or DEL. A search continues past DEL slots and stops at the key or at an empty slot.

Operations: insert 22, 33, 13, 44, 24, 35; delete 33; delete 13; insert 46.

Then two unsuccessful searches are made, for 57 and for 55. Counting every slot examined (including the empty slot that ends a search), the total number of slots examined by the two searches is ______.''',
            'answer': '12',
            'solution': '''Home slots: 22 → 0, 33 → 0, 13 → 2, 44 → 0, 24 → 2, 35 → 2, 46 → 2, 57 → 2, 55 → 0.

**Insertions:**

- 22 → 0; 33 → 0 full → 1; 13 → 2; 44 → 0,1,2 full → 3; 24 → 2,3 full → 4; 35 → 2,3,4 full → 5.
- Table: [22, 33, 13, 44, 24, 35, –, –, –, –, –]

**Deletions:** 33 (slot 1) and 13 (slot 2) become DEL.

**Insert 46** (home 2): slot 2 is DEL → 46 goes to slot 2. Table: [22, DEL, 46, 44, 24, 35, –, …].

**Search 57** (home 2): slots 2 (46), 3 (44), 4 (24), 5 (35), 6 (empty) → **5** examined.

**Search 55** (home 0): 0 (22), 1 (DEL — continue), 2, 3, 4, 5, 6 (empty) → **7** examined.

Total = 5 + 7 = **12**.

**Trap:** stopping a search at a DEL slot (which would wrongly report keys such as 44 as absent), or treating deletion as emptying the slot — that would break the probe chain of 44, 24 and 35. Tombstones keep searches correct but make them longer, which is why tables are periodically rebuilt.''',
            'solution_diagrams': [
                {
                    'type': 'hashtable',
                    'size': 11,
                    'slots': {
                        0: 22,
                        1: 'DEL',
                        2: 46,
                        3: 44,
                        4: 24,
                        5: 35,
                    },
                    'caption': 'Table before the two searches',
                },
            ],
            'verify': '''
DEL = 'DEL'; T = [None]*11
def ins(k):
    i = k % 11
    while T[i] is not None and T[i] != DEL: i = (i + 1) % 11
    T[i] = k
def find(k):
    i = k % 11; c = 0
    while True:
        c += 1
        if T[i] is None or T[i] == k: return i, c
        i = (i + 1) % 11
for k in [22, 33, 13, 44, 24, 35]: ins(k)
for k in [33, 13]: T[find(k)[0]] = DEL
ins(46)
assert T[:7] == [22, DEL, 46, 44, 24, 35, None]
assert find(57)[1] + find(55)[1] == int(ANSWER)
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'All possible BFS orders',
            'text': 'BFS is run from s on the undirected graph shown. The adjacency lists may be ordered arbitrarily, so several visiting orders are possible. Which of the following statements is/are TRUE?',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['s', 'a', 'b', 'c', 'd', 'e', 'f'],
                    'edges': [
                        ['s', 'a'],
                        ['s', 'b'],
                        ['s', 'c'],
                        ['a', 'd'],
                        ['b', 'd'],
                        ['b', 'e'],
                        ['c', 'e'],
                        ['d', 'f'],
                        ['e', 'f'],
                    ],
                    'pos': {
                        's': [0, 1],
                        'a': [1.6, 2.2],
                        'b': [1.6, 1],
                        'c': [1.6, -0.2],
                        'd': [3.2, 1.6],
                        'e': [3.2, 0.4],
                        'f': [4.8, 1],
                    },
                },
            ],
            'options': [
                'Exactly 8 distinct BFS visiting orders are possible',
                'Some BFS order visits e before d',
                's, c, a, b, d, e, f is a possible BFS order',
                'f is the last vertex visited in every BFS order',
            ],
            'answer': ['A', 'B', 'D'],
            'solution': '''Levels are fixed: {s}, {a, b, c}, {d, e}, {f}. Within these, BFS order is constrained: the level-2 vertices are visited in the order they were **discovered**, which is determined by the level-1 order (d is discovered by a or b, e by b or c).

Enumerate the 6 orders of {a, b, c} and see who discovers d, e first:

- a b c → a finds d first → d, e (b's list order is irrelevant: d already found)
- a c b → a finds d → d, e
- b a c, b c a → b finds both; its adjacency order decides → d, e **or** e, d (2 each)
- c a b, c b a → c finds e first → e, d

Total orders = 1 + 1 + 2 + 2 + 1 + 1 = **8**.

- (A) **True.**
- (B) **True** — e.g. s, c, a, b, e, d, f.
- (C) **False** — if c is the first level-1 vertex, it discovers e before anyone discovers d, so e must precede d.
- (D) **True** — f is the only vertex at distance 3.

**Trap:** assuming any permutation within each level is achievable (that would give 3! × 2! = 12).''',
            'verify': '''_m = {'C': 'B', 'B': 'C'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'B': 'D', 'D': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

import itertools
E = [('s','a'),('s','b'),('s','c'),('a','d'),('b','d'),('b','e'),('c','e'),('d','f'),('e','f')]
adj = {}
for u, v in E: adj.setdefault(u, []).append(v); adj.setdefault(v, []).append(u)
V = sorted(adj); orders = set()
for combo in itertools.product(*[list(itertools.permutations(adj[v])) for v in V]):
    P = dict(zip(V, combo)); seen = {'s'}; q = ['s']; o = []
    while q:
        u = q.pop(0); o.append(u)
        for w in P[u]:
            if w not in seen: seen.add(w); q.append(w)
    orders.add(''.join(o))
vals = [len(orders) == 8, all(o[-1] == 'f' for o in orders),
        any(o.index('e') < o.index('d') for o in orders), 'scabdef' in orders]
assert [L for L, v in zip('ABCD', vals) if v] == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Memoization via a mutable default',
            'text': 'The value printed by the following Python program is ______.',
            'code': '''def f(n, memo={}):
    if n in memo:
        return memo[n]
    f.calls += 1
    r = n if n < 2 else f(n - 1) + f(n - 2)
    memo[n] = r
    return r

f.calls = 0
f(10)
a = f.calls
f(15)
b = f.calls
print(a * 100 + b)''',
            'answer': '1116',
            'solution': '''The default `memo={}` is created **once** when `def` runs, so it persists across top-level calls — here that is exploited as a cache. `f.calls` counts only cache misses (calls that actually compute).

**f(10):** f(10) → f(9) → … → f(1); f(0) is reached via f(2)'s second call. Every n from 0 to 10 is computed exactly once (later requests hit the memo) → 11 misses. a = 11.

**f(15):** values 0..10 are already cached; 15, 14, 13, 12, 11 are computed → 5 more misses. b = 16.

Printed: 11 × 100 + 16 = **1116**.

Without memoisation f(10) alone would make 177 calls (2·F(11) − 1 with F(11) = 89); memoisation reduces this to linear.

**Trap:** expecting the memo to reset between calls (then f(15) would add 16 more misses, b = 27, printing 1127), or counting cache hits as calls.''',
            'verify': '''
assert OUTPUT.strip() == ANSWER
def g(n): return 1 if n < 2 else 1 + g(n - 1) + g(n - 2)
assert g(10) == 177
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Linked lists — reversal in growing groups',
            'text': 'Consider the following Python program on the list 1 → 2 → … → 10. What is printed?',
            'code': '''class N:
    def __init__(self, v, nxt=None):
        self.v, self.next = v, nxt

def rev(h, k):
    cur, prev, cnt = h, None, 0
    while cur and cnt < k:
        cur.next, prev, cur = prev, cur, cur.next
        cnt += 1
    if cur:
        h.next = rev(cur, k + 1)
    return prev

head = None
for v in range(10, 0, -1):
    head = N(v, head)
head = rev(head, 2)
out = []
while head:
    out.append(head.v)
    head = head.next
print(*out)''',
            'diagrams': [
                {
                    'type': 'linkedlist',
                    'values': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                    'head': 'head',
                    'caption': 'Input list',
                },
            ],
            'options': [
                '`2 1 5 4 3 9 8 7 6 10`',
                '`2 1 4 3 6 5 8 7 10 9`',
                '`2 1 5 4 3 9 8 7 6`',
                '`2 1 5 4 3 10 9 8 7 6`',
            ],
            'answer': 'A',
            'solution': '''`rev(h, k)` reverses the first k nodes, then recursively processes the rest with group size k + 1, and links the old first node `h` (now the group's tail) to the result.

The tuple assignment `cur.next, prev, cur = prev, cur, cur.next` evaluates the whole right side first (old prev, old cur, old cur.next) and then assigns left to right — `cur.next` is set on the *old* cur before `cur` is rebound, so it is a correct in-place reversal step.

- k = 2: group [1, 2] → 2 1; recurse from 3
- k = 3: group [3, 4, 5] → 5 4 3; recurse from 6
- k = 4: group [6, 7, 8, 9] → 9 8 7 6; recurse from 10
- k = 5: only [10] remains → loop stops after 1 node (cur becomes None) → 10

Joined: `2 1 5 4 3 9 8 7 6 10`.

- (B) uses a constant group size 2.
- (C) loses the final short group (as if `if cur` were missing the last link).
- (D) treats the last group as 6..10 (sizes 2, 3, 5).

**Trap:** writing the assignment as `cur, cur.next, prev = cur.next, prev, cur` would set `.next` on the *new* cur and corrupt the list — order of targets matters.''',
            'verify': "assert OUTPUT.strip() == '2 1 5 4 3 9 8 7 6 10' and ANSWER == 'A'",
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Heap facts and heapsort',
            'text': 'Which of the following statements about binary heaps with n distinct keys is/are TRUE?',
            'options': [
                'Heapsort is a stable sorting algorithm',
                'For n ≥ 7, the third-largest key of a max-heap can occupy exactly 6 different array positions',
                'The k-th smallest key of a min-heap can be found in O(k log k) time without modifying the heap',
                'Two binary heaps of n keys each can be merged into one binary heap in O(n) time',
            ],
            'answer': ['B', 'C', 'D'],
            'solution': '''- (A) **False.** E.g. records (1,x), (1,y): build-heap leaves them, then the first extraction swaps the root (1,x) to the end, giving the order y, x. Long-range swaps destroy stability.
- (B) **True.** The third-largest has exactly two larger keys, so it has at most two ancestors: depth 1 or 2 → array positions 2..7 (1-indexed), six positions. Each is achievable: at depth 1 with the second-largest as its sibling, at depth 2 with the second-largest as its parent.
- (C) **True.** Keep an auxiliary min-heap of *candidates*, starting with the root. Pop the smallest candidate and push its (at most two) children; the k-th pop is the k-th smallest. The auxiliary heap never exceeds k + 1 entries, so the cost is O(k log k), independent of n.
- (D) **True.** Concatenate the two arrays (O(n)) and run bottom-up build-heap on the 2n keys, which is O(n).

**Trap:** in (B), confusing *positions* (6) with *depths* (2); in (C), thinking the heap order forces the k-th smallest to be at depth ≤ log k (it can be at depth k − 1).''',
            'verify': '''_m = {'A': 'B', 'B': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'B': 'D', 'D': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'C', 'C': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

import itertools, heapq
# (C): enumerate all max-heaps on 1..7 and 1..8, positions of the 3rd largest
for n in (7, 8):
    pos = set()
    for p in itertools.permutations(range(1, n + 1)):
        if all(p[(i-1)//2] > p[i] for i in range(1, n)): pos.add(p.index(n - 2))
    assert pos == {1, 2, 3, 4, 5, 6}
# (A): candidate-heap method agrees with sorting
H = [1, 3, 2, 7, 4, 5, 6, 9, 8, 10]
def kth(H, k):
    c = [(H[0], 0)]
    for _ in range(k):
        v, i = heapq.heappop(c)
        for j in (2*i + 1, 2*i + 2):
            if j < len(H): heapq.heappush(c, (H[j], j))
    return v
assert all(kth(H, k) == sorted(H)[k-1] for k in range(1, 11))
# (D): heapsort on records is unstable
def heapsort(a):
    a = a[:]; n = len(a)
    def down(i, n):
        while True:
            l, r, m = 2*i+1, 2*i+2, i
            if l < n and a[l][0] > a[m][0]: m = l
            if r < n and a[r][0] > a[m][0]: m = r
            if m == i: return
            a[i], a[m] = a[m], a[i]; i = m
    for i in range(n//2 - 1, -1, -1): down(i, n)
    for e in range(n - 1, 0, -1): a[0], a[e] = a[e], a[0]; down(0, e)
    return a
assert heapsort([(1, 'x'), (1, 'y')]) == [(1, 'y'), (1, 'x')]
assert sorted(ANSWER) == ['A', 'B', 'C']
''',
        },
    ],
}
