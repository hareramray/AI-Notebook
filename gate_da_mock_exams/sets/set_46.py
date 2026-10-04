# Set 46 — Challenge Mock — Paper 1 (Hard)
# Q1-Q10: 1 mark, Q11-Q20: 2 marks.

SET = {
    "number": 46,
    "title": "Challenge Mock — Paper 1",
    "difficulty": "Hard",
    "focus": "hardest, multi-concept, trap-heavy 2-mark questions",
    "questions": [
        # ---------------------------------------------------------------- Q1
        {
            "type": "MCQ", "marks": 1, "topic": "Python — short-circuit values, chained comparisons, identity",
            "text": "Consider the following Python program. What is printed?",
            "code": '''a = 0 or [] or 'GATE'[1:3]
b = 1 < 3 > 2 == 2
c = [] is not [] and not 0
print(a, b, c, (5 > 3) + (2 > 1) * 2)''',
            "options": ["`AT True True 3`", "`AT False True 3`", "`True True False 2`", "`AT True False 3`"],
            "answer": "A",
            "solution": (
                "Four independent traps:\n\n"
                "- `or` returns the **first truthy operand** (or the last one): 0 and [] are falsy, so "
                "`a = 'GATE'[1:3]` = `'AT'` (indices 1 and 2) — a string, not `True`.\n"
                "- Chained comparison `1 < 3 > 2 == 2` means `1 < 3 and 3 > 2 and 2 == 2` → **True** (it is "
                "*not* `(1 < 3) > 2`, which would be False).\n"
                "- Each `[]` literal creates a new list, so `[] is not []` is True; `not 0` is True; `and` "
                "returns the last evaluated operand → **True**.\n"
                "- Booleans are integers: True + True * 2 = 1 + 2 = **3**.\n\n"
                "Output: `AT True True 3`.\n\n"
                "- (B) evaluates the chain left to right as `(1 < 3) > 2`.\n"
                "- (C) treats `or` as returning a bool and adds without precedence.\n"
                "- (D) thinks two empty lists are the same object.\n\n"
                "**Trap:** `and`/`or` return operands, not booleans; `is` compares identity, not equality."
            ),
            "verify": '''
assert OUTPUT.split() == ['AT', 'True', 'True', '3'] and ANSWER == 'A'
''',
        },
        # ---------------------------------------------------------------- Q2
        {
            "type": "NAT", "marks": 1, "topic": "Stack permutations — counting with a constraint",
            "text": ("The integers 1, 2, 3, 4, 5 are pushed in this order onto an initially empty stack, with pops "
                     "interleaved arbitrarily; each popped value is output and the stack is empty at the end. The "
                     "number of possible output sequences whose **first** element is 3 is ______."),
            "answer": "9",
            "solution": (
                "To output 3 first, we must push 1, 2, 3 and pop 3 immediately. Now the stack holds [1, 2] "
                "(2 on top) and 4, 5 are still to be pushed.\n\n"
                "Count the ways to finish. Think of it as interleaving: 2 must come out before 1 (stack order), "
                "and 4, 5 can be pushed/popped in between.\n\n"
                "Enumerate by when 4 is pushed relative to popping 2 and 1:\n"
                "- Pop 2, pop 1, then 4/5: {4 5, 5 4} → 2 sequences (3 2 1 4 5, 3 2 1 5 4).\n"
                "- Pop 2, then 4/5 activity, then 1 at some point: 3 2 4 1 5, 3 2 4 5 1, 3 2 5 4 1 → 3.\n"
                "- Push 4 before popping 2: 3 4 2 1 5, 3 4 2 5 1, 3 4 5 2 1, 3 5 4 2 1 → 4.\n\n"
                "Total = 2 + 3 + 4 = **9**.\n\n"
                "Check by the pattern rule: a sequence is achievable iff it has no a…b…c with c < a < b. After "
                "the leading 3, the remaining 4 values must avoid the pattern and keep 2 before 1.\n\n"
                "**Trap:** answering C₄ = 14 (as if the stack were empty after outputting 3) ignores that 1 and 2 "
                "are already stacked in a fixed order."
            ),
            "solution_diagrams": [{"type": "stack", "values": [1, 2], "label": "after popping 3",
                                   "caption": "2 must be popped before 1"}],
            "verify": '''
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
        # ---------------------------------------------------------------- Q3
        {
            "type": "MCQ", "marks": 1, "topic": "Complexity — doubling outer loop",
            "text": "The time complexity of the following fragment, as a function of n, is",
            "code": '''i, s = 1, 0
while i < n:
    for j in range(i):
        s += 1
    i *= 2''',
            "options": ["Θ(log n)", "Θ(n)", "Θ(n log n)", "Θ(n²)"],
            "answer": "B",
            "solution": (
                "The outer loop runs about log₂ n times, but the inner loop's length **doubles** each time "
                "(i = 1, 2, 4, …, < n). Total inner iterations:\n"
                "1 + 2 + 4 + … + 2^{k} where 2^{k} < n ≤ 2^{k+1} → sum = 2^{k+1} − 1 < 2n.\n"
                "Hence the work is **Θ(n)** (a geometric series is dominated by its last term).\n\n"
                "- (A) counts only outer iterations.\n"
                "- (C) multiplies log n iterations by the *maximum* inner length n — an upper bound that is "
                "not tight.\n"
                "- (D) has no basis.\n\n"
                "**Trap:** 'a loop inside a log-loop' is not automatically n log n; sum the actual inner "
                "lengths."
            ),
            "verify": '''
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
            "run_code": False,
        },
        # ---------------------------------------------------------------- Q4
        {
            "type": "MSQ", "marks": 1, "topic": "Queue using two stacks",
            "text": ("A queue is implemented with two stacks IN and OUT: `enqueue(x)` pushes x on IN; `dequeue()` "
                     "first, **only if OUT is empty**, pops every element of IN and pushes it on OUT, and then pops "
                     "OUT. Starting empty, the operations are:\n"
                     "enq 1, enq 2, enq 3, deq, enq 4, enq 5, deq, deq, deq, enq 6, deq.\n"
                     "Which of the following statements is/are TRUE?"),
            "options": ["The second dequeue moves elements from IN to OUT",
                        "In total, 5 elements are moved from IN to OUT",
                        "At the end, OUT is empty and IN contains only 6",
                        "No single dequeue performs more than 5 push/pop operations"],
            "answer": ["B", "C"],
            "solution": (
                "Elements are transferred only when OUT is empty, which is what makes the amortised cost O(1).\n\n"
                "- enq 1, 2, 3 → IN [1, 2, 3].\n"
                "- deq #1: OUT empty → move 3 elements (OUT [3, 2, 1], top 1); pop 1. Cost 3 pops + 3 pushes + "
                "1 pop = **7** operations.\n"
                "- enq 4, 5 → IN [4, 5].\n"
                "- deq #2: OUT = [3, 2] not empty → pop 2 (no transfer).\n"
                "- deq #3: pop 3. OUT empty.\n"
                "- deq #4: OUT empty → move 4, 5 (OUT [5, 4]); pop 4.\n"
                "- enq 6 → IN [6].\n"
                "- deq #5: OUT = [5] → pop 5. OUT empty; IN = [6].\n\n"
                "- (A) False — OUT still held 2 and 3.\n"
                "- (B) 3 + 2 = **5** transfers. True.\n"
                "- (C) True.\n"
                "- (D) False — the first dequeue performs 7 push/pop operations.\n\n"
                "**Trap:** transferring on *every* dequeue (not only when OUT is empty) would break FIFO order."
            ),
            "solution_diagrams": [{"type": "stack", "values": [3, 2, 1], "label": "OUT after deq #1 transfer",
                                   "caption": "Reversal puts the oldest element (1) on top"}],
            "verify": '''
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
        # ---------------------------------------------------------------- Q5
        {
            "type": "NAT", "marks": 1, "topic": "Hashing — expected number of empty slots",
            "text": ("12 keys are inserted into a hash table with 8 slots using separate chaining. Assume simple "
                     "uniform hashing (each key independently hashes to each slot with probability 1/8). The "
                     "expected number of slots that remain **empty** is ______ (rounded off to two decimal places)."),
            "answer": ["1.60", "1.62"],
            "solution": (
                "Use linearity of expectation with an indicator for each slot.\n\n"
                "P(a particular slot is empty) = P(none of the 12 keys hashes there) = (1 − 1/8)^{12} = "
                "(7/8)^{12}.\n\n"
                "(7/8)^{2} = 0.765625; (7/8)^{4} ≈ 0.586182; (7/8)^{8} ≈ 0.343609; (7/8)^{12} ≈ 0.343609 × "
                "0.586182 ≈ 0.201417.\n\n"
                "E[empty slots] = 8 × 0.201417 ≈ **1.61**.\n\n"
                "**Trap:** the events 'slot i empty' are *not* independent, but linearity of expectation does "
                "not need independence. Also, n > m does not mean every slot is used — about 20% of slots are "
                "still empty on average."
            ),
            "verify": '''
from itertools import product
e = 8 * (7 / 8) ** 12
assert float(ANSWER[0]) <= round(e, 2) <= float(ANSWER[1])
''',
        },
        # ---------------------------------------------------------------- Q6
        {
            "type": "MCQ", "marks": 1, "topic": "Graph theory — graphical degree sequences",
            "text": "Which of the following is **not** the degree sequence of any simple undirected graph?",
            "options": ["(5, 5, 4, 3, 2, 2, 1)", "(6, 5, 4, 3, 2, 2, 2)", "(5, 5, 5, 3, 2, 1, 1)",
                        "(4, 4, 3, 3, 2, 2, 2)"],
            "answer": "C",
            "solution": (
                "All four have an even sum and maximum degree ≤ 6 = n − 1, so the quick checks pass. Use "
                "**Havel–Hakimi**: remove the largest degree d and subtract 1 from the next d degrees; repeat.\n\n"
                "(C) (5, 5, 5, 3, 2, 1, 1): remove 5 → (4, 4, 2, 1, 0, 1) → sort (4, 4, 2, 1, 1, 0); remove 4 → "
                "(3, 1, 0, 0, 0) → remove 3 → needs three positive entries after it, but we get (0, −1, −1) → "
                "**not graphical**.\n"
                "(Erdős–Gallai at k = 3: 5 + 5 + 5 = 15 > 3·2 + min(3,3) + min(2,3) + 1 + 1 = 13.) Intuitively, "
                "three vertices of degree 5 each need 3 neighbours outside the trio, but the other four "
                "vertices have total degree only 7 and two of them have degree 1.\n\n"
                "- (A) remove 5 → (4, 3, 2, 1, 1, 1) → remove 4 → (2, 1, 0, 0, 1) → (2, 1, 1, 0, 0) → "
                "(0, 0, 0, 0) ✓ graphical.\n"
                "- (B) remove 6 → (4, 3, 2, 1, 1, 1) → same as above ✓.\n"
                "- (D) remove 4 → (3, 2, 2, 1, 2, 2) → (3, 2, 2, 2, 2, 1) → (1, 1, 1, 2, 1) → … ✓.\n\n"
                "**Trap:** 'even sum and max degree ≤ n − 1' is necessary but **not sufficient**."
            ),
            "verify": '''
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
        # ---------------------------------------------------------------- Q7
        {
            "type": "MCQ", "marks": 1, "topic": "Binary search on the answer",
            "text": "Consider the following Python program. What is printed?",
            "code": '''N = 1000
lo, hi, it = 0, N, 0
while lo < hi:
    it += 1
    m = (lo + hi + 1) // 2
    if m * m <= N:
        lo = m
    else:
        hi = m - 1
print(lo, it)''',
            "options": ["`31 9`", "`31 10`", "`32 9`", "`31 11`"],
            "answer": "A",
            "solution": (
                "This finds the **largest m with m² ≤ N** (integer square root). Using the *upper* middle "
                "`(lo+hi+1)//2` together with `lo = m` guarantees progress (with the lower middle the loop could "
                "stick at hi = lo + 1).\n\n"
                "Trace (lo, hi) → m:\n"
                "- (0, 1000) m=500 > → hi=499\n"
                "- (0, 499) m=250 > → hi=249\n"
                "- (0, 249) m=125 > → hi=124\n"
                "- (0, 124) m=62 > → hi=61\n"
                "- (0, 61) m=31: 961 ≤ 1000 → lo=31\n"
                "- (31, 61) m=46 > → hi=45\n"
                "- (31, 45) m=38 > → hi=37\n"
                "- (31, 37) m=34 > → hi=33\n"
                "- (31, 33) m=32: 1024 > → hi=31 → loop ends.\n\n"
                "9 iterations, lo = 31. Output `31 9`.\n\n"
                "- (B), (D) miscount iterations (e.g. adding a final check).\n"
                "- (C) 32 would be the ceiling square root; 32² = 1024 > 1000.\n\n"
                "**Trap:** the iteration count is not simply ⌈log₂ 1001⌉ = 10, because each step removes "
                "slightly more than half when it moves `hi = m − 1`."
            ),
            "verify": '''
assert OUTPUT.split() == ['31', '9'] and ANSWER == 'A'
''',
        },
        # ---------------------------------------------------------------- Q8
        {
            "type": "MCQ", "marks": 1, "topic": "Sorting — adjacent swaps versus arbitrary swaps",
            "text": ("For the array [4, 3, 1, 6, 5, 2, 8, 7], let x be the minimum number of swaps of **adjacent** "
                     "elements needed to sort it in ascending order, and y the minimum number of swaps of "
                     "**arbitrary** pairs of elements. The pair (x, y) is"),
            "options": ["(9, 5)", "(9, 4)", "(5, 5)", "(8, 5)"],
            "answer": "A",
            "solution": (
                "- An adjacent swap removes **exactly one inversion**, so x = number of inversions (this is the "
                "number of swaps bubble sort or insertion sort performs).\n"
                "- An arbitrary swap can fix one element per swap within a permutation cycle, so "
                "y = n − (number of cycles).\n\n"
                "**Inversions:** 4 > 3, 1, 2 (3); 3 > 1, 2 (2); 6 > 5, 2 (2); 5 > 2 (1); 8 > 7 (1) → x = **9**.\n\n"
                "**Cycles** (value v belongs at index v − 1): index 0 holds 4 → index 3 holds 6 → index 5 holds 2 → "
                "index 1 holds 3 → index 2 holds 1 → back to index 0: a 5-cycle. Index 4 holds 5 (fixed point). "
                "Indices 6, 7 hold 8, 7: a 2-cycle. Cycles = 3 → y = 8 − 3 = **5**.\n\n"
                "- (B) counts cycles of length > 1 as 3 and subtracts wrongly (8 − 4).\n"
                "- (C) assumes adjacent swaps are as powerful as arbitrary ones.\n"
                "- (D) misses one inversion.\n\n"
                "**Tip:** selection sort achieves y (at most n − 1 swaps); bubble/insertion sort achieve x."
            ),
            "verify": '''
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
        # ---------------------------------------------------------------- Q9
        {
            "type": "MSQ", "marks": 1, "topic": "Python — scoping errors",
            "text": "Which of the following Python snippets raise an exception when run?",
            "options": ["`x = 5` / `def f():` / `    print(x)` / `    x = 6` / `f()`",
                        "`def g():` / `    total = 0` / `    def add(v):` / `        total += v` / `    add(3)` / "
                        "`    return total` / `g()`",
                        "`fs = [lambda: i for i in range(3)]` / `fs[0]()`",
                        "`def h(a, b=2, *args, c, **kw):` / `    return a + b + c + len(kw)` / `h(1, c=3, d=4)`"],
            "answer": ["A", "B"],
            "solution": (
                "(Each `/` separates lines.) A name that is **assigned anywhere** in a function body is local "
                "to that function for the whole body (decided at compile time).\n\n"
                "- (A) `x = 6` makes x local to f, so `print(x)` reads an unassigned local → "
                "**UnboundLocalError.**\n"
                "- (B) `total += v` assigns total inside `add`, making it local to add; reading it first fails → "
                "**UnboundLocalError** (needs `nonlocal total`).\n"
                "- (C) The lambdas look up i at call time and see 2; `fs[0]()` returns 2. No error.\n"
                "- (D) c is keyword-only (after `*args`); the call supplies it, and d=4 goes into kw. Returns "
                "1 + 2 + 3 + 1 = 7. No error.\n\n"
                "**Trap:** (A) fails even though a global x exists — the local assignment *later* in the body "
                "still shadows it from the first line."
            ),
            "verify": '''
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
        # ---------------------------------------------------------------- Q10
        {
            "type": "MCQ", "marks": 1, "topic": "Binary trees — counting shapes of maximum height",
            "text": ("The number of structurally distinct binary trees with **5** nodes whose height (number of "
                     "edges on the longest root-to-leaf path) is **4** is"),
            "options": ["16", "32", "14", "8"],
            "answer": "A",
            "solution": (
                "Height 4 with 5 nodes means the longest path already contains all 5 nodes, so the tree is a "
                "**path** (every node except the last has exactly one child).\n\n"
                "Each of the 4 parent→child links independently goes **left or right** → 2^{4} = **16** "
                "distinct trees.\n\n"
                "- (B) 32 = 2^{5} counts a choice for the leaf too.\n"
                "- (C) 14 is the Catalan number C₄ (all binary trees with 4 nodes) — irrelevant here.\n"
                "- (D) 8 forgets one link.\n\n"
                "**Tip:** in general, the number of n-node binary trees of height n − 1 is 2^{n−1}; these are "
                "exactly the BSTs produced by insertion orders in which every new key is a new minimum or "
                "maximum of the remaining ones."
            ),
            "verify": '''
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
    ],
}
