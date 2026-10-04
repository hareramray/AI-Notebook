# Reference example showing every supported feature.  A real set has EXACTLY 20 questions:
# Q1-Q10 are 1-mark, Q11-Q20 are 2-mark.  Only 4 questions are shown here.
#
# Markup inside text / options / solution:
#   `inline code`, **bold**, x^{2} superscript, a_{i} subscript,
#   single newline = line break, blank line = new paragraph, lines starting "- " = bullets.
#   Use real unicode for math: Θ Ω O ≤ ≥ ≠ → ⌈ ⌉ ⌊ ⌋ log₂ n² √ ∑ ∞ × ÷
# Field order per question (optional fields marked ?):
#   type, marks, topic, text, code?, diagrams?, text2?, options (MCQ/MSQ only), answer,
#   solution, solution_code?, solution_diagrams?, solution_after?, verify?, run_code?
# verify: hidden Python run AFTER `code` (unless run_code=False) in the same namespace.
#   OUTPUT = everything `code` printed;  ANSWER = the "answer" field.  Use assert.

SET = {
    "number": 0,
    "title": "Example Set — Format Reference",
    "difficulty": "Moderate",
    "focus": "Python semantics, stacks, BST, Dijkstra",
    "questions": [
        {
            "type": "MCQ", "marks": 1, "topic": "Python — mutable default arguments",
            "text": "Consider the following Python program. What is printed?",
            "code": '''def add(x, bucket=[]):
    bucket.append(x)
    return bucket

a = add(1)
b = add(2)
c = add(3, [])
print(len(a), len(b), len(c))''',
            "options": ["`1 1 1`", "`1 2 1`", "`2 2 1`", "`2 2 2`"],
            "answer": "C",
            "solution": (
                "The default value `[]` is evaluated **once**, when `def` executes, and the same list "
                "object is reused by every call that omits `bucket`.\n\n"
                "- `add(1)` appends 1 to the shared list → shared list is `[1]`; `a` refers to it.\n"
                "- `add(2)` appends 2 to the *same* list → `[1, 2]`; `b` is the same object as `a`.\n"
                "- `add(3, [])` uses a fresh list → `[3]`.\n\n"
                "Since `a` and `b` alias one list of length 2, the output is `2 2 1`.\n\n"
                "**Trap:** option (B) assumes `a` was a snapshot. Lists are references, not copies."
            ),
            "verify": "assert OUTPUT.strip() == '2 2 1'",
        },
        {
            "type": "MSQ", "marks": 1, "topic": "Binary search trees",
            "text": "Consider the binary search tree shown below. Which of the following statements is/are TRUE?",
            "diagrams": [{"type": "bintree",
                          "tree": [50, [30, [20, None, None], [40, None, None]],
                                   [70, [60, None, None], [80, None, [90, None, None]]]],
                          "caption": "Figure: BST T"}],
            "options": [
                "The pre-order traversal of T is 50, 30, 20, 40, 70, 60, 80, 90",
                "The height of T (edges on the longest root-to-leaf path) is 3",
                "Deleting 50 using the in-order successor makes 60 the new root",
                "The post-order traversal of T ends with 70, 50",
            ],
            "answer": ["A", "B", "C", "D"],
            "solution": (
                "- (A) Pre-order = root, left, right: 50, 30, 20, 40, 70, 60, 80, 90. **True.**\n"
                "- (B) Longest path 50→70→80→90 has 3 edges. **True.**\n"
                "- (C) In-order successor of 50 is the minimum of the right subtree = 60. **True.**\n"
                "- (D) Post-order = 20, 40, 30, 60, 90, 80, 70, 50 — ends with 70, 50. **True.**"
            ),
            "solution_diagrams": [{"type": "bintree",
                                   "tree": [60, [30, [20], [40]], [70, None, [80, None, [90]]]],
                                   "highlight": [60], "caption": "T after deleting 50 (successor 60 promoted)"}],
            "verify": '''
def pre(t): return [] if t is None else [t[0]] + pre(t[1]) + pre(t[2])
def post(t): return [] if t is None else post(t[1]) + post(t[2]) + [t[0]]
T = [50,[30,[20,None,None],[40,None,None]],[70,[60,None,None],[80,None,[90,None,None]]]]
assert pre(T) == [50,30,20,40,70,60,80,90]
assert post(T)[-2:] == [70,50]
assert sorted(ANSWER) == ['A','B','C','D']
''',
        },
        {
            "type": "NAT", "marks": 2, "topic": "Shortest paths — Dijkstra",
            "text": ("Dijkstra's algorithm is run on the weighted directed graph below with source **S**. "
                     "What is the shortest-path distance from S to T?"),
            "diagrams": [{"type": "graph", "directed": True,
                          "nodes": ["S", "A", "B", "C", "T"],
                          "edges": [["S", "A", 4], ["S", "B", 1], ["B", "A", 2], ["A", "C", 1],
                                    ["B", "C", 5], ["C", "T", 3], ["A", "T", 7]],
                          "pos": {"S": [0, 1], "A": [2, 2], "B": [2, 0], "C": [4, 1], "T": [6, 1]}}],
            "answer": "7",
            "solution": (
                "Run Dijkstra from S (distances shown after each extraction):\n\n"
                "- Extract S (0): relax A=4, B=1.\n"
                "- Extract B (1): A = min(4, 1+2) = 3; C = 1+5 = 6.\n"
                "- Extract A (3): C = min(6, 3+1) = 4; T = 3+7 = 10.\n"
                "- Extract C (4): T = min(10, 4+3) = 7.\n"
                "- Extract T (7).\n\n"
                "Shortest path S → B → A → C → T with cost 1 + 2 + 1 + 3 = **7**."
            ),
            "solution_diagrams": [{"type": "matrix", "title": "Distance table after each extraction",
                                   "col_labels": ["S", "A", "B", "C", "T"],
                                   "row_labels": ["init", "S", "B", "A", "C"],
                                   "rows": [[0, "∞", "∞", "∞", "∞"], [0, 4, 1, "∞", "∞"], [0, 3, 1, 6, "∞"],
                                            [0, 3, 1, 4, 10], [0, 3, 1, 4, 7]]}],
            "verify": '''
import heapq
G = {'S':[('A',4),('B',1)],'B':[('A',2),('C',5)],'A':[('C',1),('T',7)],'C':[('T',3)],'T':[]}
d = {v: float('inf') for v in G}; d['S'] = 0; pq = [(0,'S')]
while pq:
    du,u = heapq.heappop(pq)
    if du > d[u]: continue
    for v,w in G[u]:
        if du+w < d[v]: d[v] = du+w; heapq.heappush(pq,(d[v],v))
assert d['T'] == float(ANSWER)
''',
        },
        {
            "type": "NAT", "marks": 2, "topic": "Hashing — linear probing",
            "text": ("Keys 43, 36, 92, 87, 11, 4, 71, 13, 14 are inserted in that order into an initially empty "
                     "hash table of size 10 using h(k) = k mod 10 and linear probing. "
                     "What is the index of the slot where key 14 is stored?"),
            "answer": "9",
            "solution": (
                "Trace (h = k mod 10, step +1 on collision):\n\n"
                "- 43→3, 36→6, 92→2, 87→7, 11→1, 4→4 (all direct hits).\n"
                "- 71: home 1 full → 2 full → 3 full → 4 full → **5**.\n"
                "- 13: home 3 full → 4 → 5 → 6 → 7 full → **8**.\n"
                "- 14: home 4 full → 5 → 6 → 7 → 8 full → **9**.\n\n"
                "Key 14 lands in slot **9** after 5 failed probes — a textbook case of *primary clustering*."
            ),
            "solution_diagrams": [{"type": "hashtable", "size": 10,
                                   "slots": {1: 11, 2: 92, 3: 43, 4: 4, 5: 71, 6: 36, 7: 87, 8: 13, 9: 14},
                                   "caption": "Final table"}],
            "verify": '''
T = [None]*10
for k in [43,36,92,87,11,4,71,13,14]:
    i = k % 10
    while T[i] is not None: i = (i+1) % 10
    T[i] = k
assert T.index(14) == int(ANSWER)
''',
        },
    ],
}
