# -*- coding: utf-8 -*-
"""GATE DA question bank: AI - Search (uninformed, informed, adversarial,
problem formulation, local search).

Each entry is a dict with keys: topic, type, marks, q, options, answer, solution.
Text uses ReportLab Paragraph mark-up only (<b>, <i>, <sub>, <sup>, <br/>).
"""

UN = "Uninformed Search"
IN = "Informed Search"
AD = "Adversarial Search"
LO = "Local Search"
PF = "Problem Formulation"


def _q(topic, typ, marks, q, options, answer, solution):
    return {"topic": topic, "type": typ, "marks": marks, "q": q,
            "options": options, "answer": answer, "solution": solution}


def MCQ(topic, marks, q, options, ans, sol):
    return _q(topic, "MCQ", marks, q, options, [ans], sol)


def MSQ(topic, marks, q, options, ans, sol):
    return _q(topic, "MSQ", marks, q, options, list(ans), sol)


def NAT(topic, marks, q, lo, hi, sol):
    return _q(topic, "NAT", marks, q, [], {"lo": lo, "hi": hi}, sol)


# Graph G1 (used by several questions), described fully in text.
G1 = ("Consider the directed graph with start S and goal G and edges (with costs): "
      "S→A (1), S→B (4), A→B (2), A→C (5), B→C (1), B→G (6), C→G (3). ")
H1 = "The heuristic is h(S)=7, h(A)=6, h(B)=2, h(C)=1, h(G)=0. "

# Graph G2 (consistent heuristic).
G2 = ("Consider the directed graph with start S and goal G and edges (with costs): "
      "S→A (2), S→B (4), A→C (2), A→D (4), B→C (1), C→D (1), C→G (5), D→G (2). "
      "The heuristic is h(S)=5, h(A)=4, h(B)=4, h(C)=3, h(D)=2, h(G)=0. ")

HEAP = ("Consider a complete binary tree of depth 3 whose 15 nodes are labelled 1 to 15 in "
        "level order: the root is 1 and the children of node i are 2i (left) and 2i+1 (right). ")

BANK = [
    # ------------------------------------------------------------------
    # UNINFORMED SEARCH
    # ------------------------------------------------------------------
    MCQ(UN, 1,
        "Breadth-first search (graph search) is guaranteed to return an <i>optimal</i> (least-cost) "
        "solution whenever a solution exists, provided that",
        ["all step costs are identical (e.g. every action costs 1)",
         "an admissible heuristic is supplied",
         "the branching factor is infinite",
         "the state space contains no cycles"],
        0,
        "BFS always returns the <b>shallowest</b> goal. The shallowest goal is the cheapest one only "
        "when path cost is a non-decreasing function of depth, the standard case being identical step "
        "costs. BFS uses no heuristic, so (B) has nothing to do with it. With an infinite branching factor "
        "BFS cannot even finish a single level, so (C) is wrong. Removing cycles does not help when "
        "step costs differ: a deep cheap path can still beat a shallow expensive one, so (D) is wrong."),

    NAT(UN, 1,
        "A uniform tree has branching factor b = 10, and the only goal is at depth d = 5. Breadth-first "
        "search applies the goal test when a node is <i>generated</i>. In the worst case the goal is the "
        "last node generated at depth 5. How many nodes are generated in total, not counting the root?",
        111110, 111110,
        "With the goal test at generation, BFS stops as soon as the goal is generated, so it generates at "
        "most every node down to depth d. Nodes generated = b + b<sup>2</sup> + b<sup>3</sup> + "
        "b<sup>4</sup> + b<sup>5</sup> = 10 + 100 + 1000 + 10000 + 100000 = <b>111110</b>. "
        "This is the AIMA figure behind BFS's O(b<sup>d</sup>) time bound."),

    NAT(UN, 2,
        "Iterative deepening search (IDS) runs on a uniform tree with b = 10 and the shallowest goal at "
        "d = 5. Assume the worst case: the final iteration (limit 5) generates every node at depth 5. "
        "Each time a non-root node is generated, it counts once, so a node regenerated in a later "
        "iteration counts again. The root is not counted. What is the total number of node generations?",
        123450, 123450,
        "Nodes at depth i are generated once in each iteration with limit ≥ i, so they are generated "
        "(d − i + 1) times. N(IDS) = d·b + (d−1)·b<sup>2</sup> + … + 1·b<sup>d</sup> = 5·10 + 4·100 + "
        "3·1000 + 2·10000 + 1·100000 = 50 + 400 + 3000 + 20000 + 100000 = <b>123450</b>. "
        "BFS generates 111110 nodes on the same problem, so the overhead of repeating the shallow levels "
        "is only about 11%."),

    MCQ(UN, 1,
        "For depth-first <i>tree</i> search with branching factor b and maximum depth m, the space "
        "complexity is",
        ["O(b<sup>m</sup>)", "O(bm)", "O(b<sup>d</sup>)", "O(m<sup>b</sup>)"],
        1,
        "DFS tree search stores only the current path from the root plus the unexpanded siblings of each "
        "node on that path. That is at most about b nodes per level over m levels, so the space is "
        "<b>O(bm)</b>. O(b<sup>m</sup>) is its worst-case <i>time</i>, not its space. "
        "O(b<sup>d</sup>) is the space of BFS. O(m<sup>b</sup>) does not arise for any standard algorithm."),

    MCQ(UN, 1,
        "Which statement about depth-first search on a <b>finite</b> state space is correct?",
        ["The graph-search version is complete, but the tree-search version can loop forever on cycles",
         "Both versions are complete and optimal",
         "The tree-search version is complete, but the graph-search version is not",
         "Neither version is complete"],
        0,
        "Graph-search DFS never re-expands a state, so in a finite space it eventually expands every "
        "reachable state and is complete. Tree-search DFS keeps no explored set, so it can follow a cycle "
        "such as A→B→A→… forever and is incomplete. Neither version is optimal: DFS can return a deep, "
        "expensive goal before a shallow one. So (B), (C) and (D) are all wrong."),

    NAT(UN, 2,
        "Depth-first tree search generates all b = 3 children of a node when it expands that node. The "
        "tree has depth m = 10, and no goal is found along the leftmost path. Consider the moment just "
        "after DFS expands the leftmost node at depth 9, so that its 3 children at depth 10 have been "
        "added to the frontier. How many nodes are in the frontier at that moment?",
        21, 21,
        "Along the leftmost path, the nodes at depths 0 to 9 have all been expanded. At each depth from "
        "1 to 9, the b − 1 = 2 unexpanded siblings of the path node are still in the frontier: "
        "9 × 2 = 18 nodes. The 3 children at depth 10 have just been added. "
        "Frontier size = 18 + 3 = <b>21</b> = (b−1)m + 1, which illustrates DFS's O(bm) space."),

    NAT(UN, 2,
        HEAP + "Iterative deepening search uses depth limits 0, 1, 2, 3, … in turn, expands left children "
        "before right children, and goal-tests a node when it is visited (popped). The goal is node 11. "
        "Over all iterations, counting repeated visits, how many node visits happen up to and including "
        "the visit at which node 11 is found?",
        19, 19,
        "Node 11 lies at depth 3 (path 1→2→5→11). Limit 0 visits {1}: 1 visit. Limit 1 visits "
        "{1,2,3}: 3 visits. Limit 2 visits the whole depth-2 tree {1,2,4,5,3,6,7}: 7 visits. Limit 3 "
        "visits 1,2,4,8,9,5,10,11 in preorder and stops at 11: 8 visits. "
        "Total = 1 + 3 + 7 + 8 = <b>19</b>."),

    NAT(UN, 2,
        HEAP + "Depth-first search pushes the right child before the left child, so the left child is "
        "explored first, and it goal-tests a node when the node is removed from the frontier. The goal is "
        "node 12. How many nodes are removed from the frontier, including node 12?",
        11, 11,
        "DFS visits nodes in preorder: 1, 2, 4, 8, 9, 5, 10, 11, 3, 6, 12, … Node 12 is the "
        "<b>11th</b> node removed. For comparison, BFS would remove nodes in label order and find node "
        "12 at the 12th removal."),

    NAT(UN, 1,
        "Bidirectional BFS runs on a problem with uniform branching factor b = 10 in both directions, and "
        "the solution has depth d = 6. Each search goes to depth d/2 = 3, and the two frontiers meet. "
        "Assume each direction generates every node down to depth 3, excluding its own root. How many "
        "nodes are generated in total by the two searches?",
        2220, 2220,
        "Each direction generates b + b<sup>2</sup> + b<sup>3</sup> = 10 + 100 + 1000 = 1110 nodes. "
        "Two directions give 2 × 1110 = <b>2220</b>. A single BFS to depth 6 would generate about "
        "1.11 × 10<sup>6</sup> nodes. That is the O(b<sup>d/2</sup>) versus O(b<sup>d</sup>) advantage."),

    MSQ(UN, 1,
        "Which of the following are requirements for applying bidirectional search?",
        ["Predecessors of a state can be computed, so the problem can be searched backward",
         "The goal state is explicitly known (or there are only a few goal states), so the backward search has somewhere to start",
         "An admissible heuristic must be available",
         "The state space must be a tree"],
        [0, 1],
        "The backward search expands states toward their predecessors, so (A) predecessors must be "
        "computable and (B) the goal must be explicitly known. An implicit goal test such as 'checkmate' "
        "gives backward search no starting state. A heuristic is not needed (C): bidirectional BFS and "
        "bidirectional UCS are uninformed. The state space may be any graph (D)."),

    MSQ(UN, 2,
        "Iterative deepening search (IDS) runs on a problem with finite branching factor b and shallowest "
        "goal depth d. Which of the following statements are TRUE?",
        ["IDS is complete",
         "IDS is optimal when all step costs are equal",
         "The space complexity of IDS is O(bd)",
         "The time complexity of IDS is asymptotically worse than BFS by a factor of d, namely O(d·b<sup>d</sup>)"],
        [0, 1, 2],
        "IDS combines DFS's memory use with BFS's level-by-level completeness. (A) is true: with finite b "
        "it eventually reaches limit d and finds the goal. (B) is true: like BFS, it finds the shallowest "
        "goal first, which is optimal for unit costs. (C) is true: each iteration is a DFS of depth at "
        "most d, so the space is O(bd). (D) is false: the total d·b + (d−1)b<sup>2</sup> + … + "
        "b<sup>d</sup> is still O(b<sup>d</sup>), because the deepest level dominates and the repeated "
        "shallow levels add only a constant factor of about b/(b−1)."),

    MCQ(UN, 2,
        "Depth-limited search (DLS) with limit l is applied to a problem with unit step costs whose "
        "shallowest goal lies at depth d. Which statement is correct?",
        ["If l &lt; d, DLS is incomplete. If l &gt; d, it finds a solution but not necessarily the shallowest (optimal) one",
         "If l &lt; d, DLS still finds the goal because it backtracks",
         "If l &gt; d, DLS is always optimal because it searches deeper than needed",
         "DLS is complete and optimal for every l ≥ 0"],
        0,
        "DLS treats nodes at depth l as having no successors. If l &lt; d, the goal can never be reached, "
        "so DLS is incomplete; backtracking does not help, so (B) is wrong. If l &gt; d, a goal is "
        "reachable, but DLS explores depth-first and may meet a deeper goal (depth between d and l) "
        "before the shallowest one, so it is not optimal and (C) is wrong. (D) is wrong for both reasons."),

    NAT(UN, 2,
        "Iterative deepening search runs on a complete binary tree of depth 3 (15 nodes) that contains "
        "<b>no</b> goal. It uses limits 0, 1, 2, 3 and then stops. A node visit is one goal test on one "
        "node, and repeated visits across iterations count separately. What is the total number of node "
        "visits?",
        26, 26,
        "The iteration with limit L visits the whole tree of depth L, which has 2<sup>L+1</sup> − 1 "
        "nodes. Limit 0: 1. Limit 1: 3. Limit 2: 7. Limit 3: 15. "
        "Total = 1 + 3 + 7 + 15 = <b>26</b>. For b = 2 the repetition overhead is largest, here 26 "
        "versus 15 nodes, which is still less than double."),

    MCQ(UN, 2,
        G1 + "Uniform-cost search (graph search, goal test when a node is selected for expansion) is run "
        "from S. Which path does it return?",
        ["S→B→G (cost 10)", "S→A→C→G (cost 9)", "S→B→C→G (cost 8)", "S→A→B→C→G (cost 7)"],
        3,
        "UCS expands nodes in order of g. Pop S(0): push A(1), B(4). Pop A(1): push B(3), C(6). "
        "Pop B(3): push C(4), G(9). Pop C(4): push G(7). The stale entries B(4) and C(6) are skipped. "
        "Pop G(7) and return <b>S→A→B→C→G with cost 7</b>. "
        "The other paths are real paths in the graph, but each costs more than 7. UCS returns the "
        "cheapest path because it tests the goal on expansion."),

    NAT(UN, 2,
        G1 + "Uniform-cost search (graph search with an explored set, goal test when a node is selected "
        "for expansion) is run from S. How many nodes are <i>expanded</i> before the goal G is selected? "
        "Count S, and do not count G.",
        4, 4,
        "The expansion order by g-value is S(0), A(1), B(3) (reached via A), C(4) (reached via B). After "
        "that, the cheapest entry in the frontier is G(7), which is selected and terminates the search. "
        "The stale entries B(4) and C(6) are never expanded. Nodes expanded = {S, A, B, C} = "
        "<b>4</b>."),

    MSQ(UN, 1,
        "Every action has the same positive cost. Which of the following algorithms are guaranteed to "
        "return an optimal solution on a problem with a finite branching factor that has a solution?",
        ["Breadth-first search", "Iterative deepening search", "Uniform-cost search",
         "Depth-first search (graph search)"],
        [0, 1, 2],
        "With equal step costs, the cheapest solution is the shallowest one. BFS (A) and IDS (B) find the "
        "shallowest goal first. UCS (C) is optimal for any positive step costs. DFS (D) can follow a deep "
        "branch and return a deep goal before discovering a shallower one, so it is not optimal."),

    MCQ(UN, 1,
        "The frontier of depth-first search is implemented as a",
        ["FIFO queue", "LIFO stack", "priority queue ordered by g(n)", "priority queue ordered by h(n)"],
        1,
        "DFS always expands the most recently generated (deepest) node, which is <b>LIFO</b> behaviour. "
        "A FIFO queue gives BFS (A). A priority queue on g(n) gives UCS (C). A priority queue on h(n) "
        "gives greedy best-first search (D)."),

    MCQ(UN, 2,
        "Suppose breadth-first search were changed to apply the goal test when a node is <i>selected for "
        "expansion</i> instead of when it is generated. The branching factor is b and the shallowest goal "
        "is at depth d. In the worst case, the number of nodes generated becomes",
        ["O(b<sup>d</sup>)", "O(b<sup>d+1</sup>)", "O(b<sup>d/2</sup>)", "O(bd)"],
        1,
        "With a late goal test, BFS expands every node at depth d that precedes the goal and generates "
        "their children at depth d+1. That adds up to b<sup>d+1</sup> − b nodes, so the bound is "
        "<b>O(b<sup>d+1</sup>)</b>. Early testing (at generation) gives O(b<sup>d</sup>) (A). "
        "O(b<sup>d/2</sup>) is the bidirectional bound (C). O(bd) is a space bound for IDS (D)."),

    MSQ(UN, 2,
        "Which of the following statements about tree search versus graph search are TRUE?",
        ["Graph search keeps an explored (reached) set so that no state is expanded more than once",
         "On a finite state space with reversible actions, tree search can face an infinite search tree because of loopy paths",
         "Depth-first graph search is complete on infinite state spaces",
         "The memory used by depth-first graph search can grow in proportion to the number of reachable states"],
        [0, 1, 3],
        "(A) is true: the explored set is what defines graph search. (B) is true: with reversible actions, "
        "a path such as A→B→A→B… can be extended forever, so even a finite state space produces an "
        "infinite tree. (C) is false: in an infinite state space, DFS can follow an infinite branch "
        "forever. (D) is true: the explored set can hold every reachable state, which removes DFS's "
        "linear-space advantage."),

    NAT(UN, 1,
        "AIMA bounds the time and space of uniform-cost search by O(b<sup>1+⌊C*/ε⌋</sup>), where C* is "
        "the optimal solution cost and ε is the minimum step cost. For C* = 10 and ε = 2, what is the "
        "exponent of b in this bound?",
        6, 6,
        "The exponent is 1 + ⌊C*/ε⌋ = 1 + ⌊10/2⌋ = 1 + 5 = <b>6</b>. Each step costs at least ε, so an "
        "optimal path has at most C*/ε = 5 steps. UCS can then generate one further level when it expands "
        "nodes of cost about C*."),

    MCQ(UN, 2,
        "BFS runs on a problem with b = 10 and solution depth d = 8. It stores every generated node, and "
        "each node needs 1 KB. Approximately how much memory is required? (1 GB = 10<sup>6</sup> KB.)",
        ["About 100 MB", "About 1 GB", "About 100 GB", "About 10 TB"],
        2,
        "The nodes generated are b + … + b<sup>8</sup> ≈ 1.11 × 10<sup>8</sup>. At 1 KB each, that is "
        "about 1.11 × 10<sup>8</sup> KB ≈ <b>111 GB, i.e. about 100 GB</b>. This is AIMA's point that "
        "memory, not time, is the binding constraint for BFS. 100 MB (A) and 1 GB (B) are 2 to 3 orders of "
        "magnitude too small, and 10 TB (D) is 100 times too large."),

    MSQ(UN, 2,
        "Uniform-cost search runs with every step cost at least some ε &gt; 0. Which of the following "
        "are TRUE?",
        ["UCS is optimal",
         "If every step cost equals the same constant, UCS behaves essentially like BFS (expanding level by level), but because it goal-tests on expansion it may generate a whole extra level of nodes",
         "UCS is complete when the branching factor is finite",
         "UCS remains complete even when the graph contains a cycle of zero-cost actions"],
        [0, 1, 2],
        "(A) is true: UCS expands nodes in order of g, so the first goal it selects is the cheapest. "
        "(B) is true: equal costs make g proportional to depth, but the goal test at expansion means the "
        "children at depth d+1 may already have been generated. (C) is true: with costs ≥ ε and finite "
        "b, only finitely many nodes have g ≤ C*. (D) is false: a zero-cost cycle lets g stay constant "
        "while the path grows forever, so UCS may never terminate. This is why the ε &gt; 0 condition "
        "is needed."),

    # ------------------------------------------------------------------
    # INFORMED SEARCH
    # ------------------------------------------------------------------
    MCQ(IN, 1,
        "A heuristic h is <b>admissible</b> if, for every node n (where h*(n) is the true cost of an "
        "optimal path from n to a goal),",
        ["h(n) ≥ h*(n)", "h(n) ≤ h*(n)", "h(n) ≤ c(n, a, n′) + h(n′) for every successor n′",
         "h(n) = 0"],
        1,
        "An admissible heuristic never overestimates the cost to reach a goal: <b>h(n) ≤ h*(n)</b>. "
        "(A) describes a pessimistic, inadmissible heuristic. (C) is the definition of consistency, which "
        "is a stronger condition. (D) is one particular admissible heuristic, not the definition."),

    MCQ(IN, 1,
        "A heuristic h is <b>consistent</b> (monotone) if, for every node n, every action a and its "
        "successor n′,",
        ["h(n) ≤ h*(n)", "h(n) ≤ c(n, a, n′) + h(n′)", "h(n′) ≤ h(n)", "h(n) + h(n′) ≤ c(n, a, n′)"],
        1,
        "Consistency is the triangle inequality <b>h(n) ≤ c(n,a,n′) + h(n′)</b>. (A) is admissibility. "
        "(C) is not required: a successor can have a larger h than its parent. (D) is meaningless as a "
        "condition and would force h to be tiny."),

    MSQ(IN, 2,
        "Assume h(goal) = 0 and all step costs are positive. Which of the following are TRUE?",
        ["Every consistent heuristic is admissible",
         "Every admissible heuristic is consistent",
         "If h is consistent, the values of f(n) = g(n) + h(n) along any path are non-decreasing",
         "A* tree search with an admissible heuristic is optimal"],
        [0, 2, 3],
        "(A) is true: induct backward along an optimal path from the goal, using h(n) ≤ c + h(n′) ≤ "
        "c + h*(n′) = h*(n). (B) is false: admissible but inconsistent heuristics exist, for example "
        "h(A)=6 and h(B)=2 with c(A,B)=2. (C) is true: f(n′) = g(n) + c + h(n′) ≥ g(n) + h(n) = f(n). "
        "(D) is true: for tree search, admissibility is enough for optimality. Consistency is needed for "
        "graph search without reopening."),

    NAT(IN, 1,
        "In the 8-puzzle, the goal configuration is (rows top to bottom) 1 2 3 / 4 5 6 / 7 8 _, where _ "
        "is the blank. The current state is 8 1 3 / 4 _ 2 / 7 6 5. What is the value of h<sub>1</sub>, "
        "the number of misplaced tiles (do not count the blank)?",
        5, 5,
        "Compare position by position. Tiles 3, 4 and 7 are already in place. Tiles 8, 1, 2, 6 and 5 are "
        "not. h<sub>1</sub> = <b>5</b>."),

    NAT(IN, 2,
        "In the 8-puzzle, the goal configuration is 1 2 3 / 4 5 6 / 7 8 _ and the current state is "
        "8 1 3 / 4 _ 2 / 7 6 5 (rows top to bottom, _ = blank). What is h<sub>2</sub>, the sum of the "
        "Manhattan distances of the tiles from their goal positions (excluding the blank)?",
        10, 10,
        "Use (row, column) coordinates from (0,0). Tile 8 is at (0,0) and belongs at (2,1): distance 3. "
        "Tile 1 is at (0,1) and belongs at (0,0): 1. Tile 3: 0. Tile 4: 0. Tile 2 is at (1,2) and "
        "belongs at (0,1): 2. Tile 7: 0. Tile 6 is at (2,1) and belongs at (1,2): 2. Tile 5 is at (2,2) "
        "and belongs at (1,1): 2. Sum = 3+1+2+2+2 = <b>10</b>."),

    MCQ(IN, 2,
        G1 + H1 + "A* <b>graph search</b> is run from S. It keeps an explored set, never re-opens a state "
        "that has already been expanded, and goal-tests on expansion. What is the cost of the solution "
        "it returns?",
        ["7", "8", "9", "10"],
        1,
        "Expand S: push A (g=1, f=7) and B (g=4, f=6). Expand B (f=6): push C (g=5, f=6) and G (g=10, "
        "f=10). Expand C (f=6): push G (g=8, f=8). Expand A (f=7): its successors B (g=3) and C (g=6) are "
        "already explored and are discarded. Expand G (f=8) and return cost <b>8</b> (S→B→C→G). The "
        "optimal cost is 7 (S→A→B→C→G). Optimality fails because h is admissible but not consistent "
        "(h(A)=6 &gt; c(A,B)+h(B)=4), and the cheaper path to B is discovered only after B is closed."),

    MSQ(IN, 2,
        G1 + H1 + "Which of the following statements are TRUE?",
        ["h is admissible",
         "h is consistent",
         "A* <i>tree</i> search (no explored set) with this h returns a path of cost 7",
         "Greedy best-first search (graph search) with this h returns the path S→B→G"],
        [0, 2, 3],
        "The true costs-to-go are h*(C)=3, h*(B)=min(6, 1+3)=4, h*(A)=min(5+3, 2+4)=6, and "
        "h*(S)=min(1+6, 4+4)=7. In every case h ≤ h*, so (A) is true. (B) is false: on edge A→B, "
        "h(A)=6 &gt; 2 + h(B) = 4. (C) is true: A* tree search with an admissible h is optimal and "
        "returns S→A→B→C→G of cost 7. (D) is true: greedy expands S, then B (h=2), which generates C "
        "(h=1) and G (h=0). It then selects G and returns S→B→G of cost 10."),

    MCQ(IN, 1,
        "Greedy best-first search orders its frontier by",
        ["g(n)", "h(n)", "g(n) + h(n)", "depth(n)"],
        1,
        "Greedy best-first search always expands the node that looks closest to the goal, so it uses "
        "f(n) = <b>h(n)</b>. g(n) gives UCS (A). g + h gives A* (C). Depth gives BFS when the shallowest "
        "node is expanded first, or DFS when the deepest is (D)."),

    MCQ(IN, 1,
        "h<sub>1</sub> and h<sub>2</sub> are both admissible, and h<sub>2</sub>(n) ≥ h<sub>1</sub>(n) "
        "for every n. Which statement is correct?",
        ["h<sub>1</sub> dominates h<sub>2</sub>, so A* with h<sub>1</sub> is preferable",
         "h<sub>2</sub> dominates h<sub>1</sub>, and A* with h<sub>2</sub> never expands more nodes than A* with h<sub>1</sub> (apart from ties at f = C*)",
         "A* with h<sub>2</sub> may return a more expensive solution than A* with h<sub>1</sub>",
         "Dominance requires h<sub>2</sub>(n) = h<sub>1</sub>(n) + c for a constant c"],
        1,
        "<b>h<sub>2</sub> dominates h<sub>1</sub></b>. With consistent heuristics, A* expands every "
        "node with f(n) &lt; C*, which means h(n) &lt; C* − g(n). A larger h satisfies this inequality "
        "at fewer nodes, so A* with h<sub>2</sub> expands a subset. (A) reverses the relation. (C) is "
        "wrong because both heuristics are admissible, so both runs are optimal. (D) is not the "
        "definition of dominance."),

    NAT(IN, 1,
        "A* generates N = 84 nodes (not counting the root) to find a solution at depth d = 3. Using AIMA's "
        "definition N + 1 = 1 + b* + (b*)<sup>2</sup> + … + (b*)<sup>d</sup>, what is the effective "
        "branching factor b*?",
        4, 4,
        "Solve 1 + b* + b*<sup>2</sup> + b*<sup>3</sup> = 85, which means b* + b*<sup>2</sup> + "
        "b*<sup>3</sup> = 84. Try b* = 4: 4 + 16 + 64 = 84. So <b>b* = 4</b>."),

    NAT(IN, 2,
        "A search algorithm generates N = 52 nodes (not counting the root) to find a solution at depth "
        "d = 5. Using N + 1 = 1 + b* + (b*)<sup>2</sup> + … + (b*)<sup>5</sup>, find the effective "
        "branching factor b*, correct to two decimal places.",
        1.90, 1.93,
        "Solve b* + b*<sup>2</sup> + b*<sup>3</sup> + b*<sup>4</sup> + b*<sup>5</sup> = 52. For "
        "b*=1.9: 1.9+3.61+6.859+13.03+24.76 ≈ 50.2, which is too small. For b*=1.95: about 54.0, which "
        "is too large. Bisection gives <b>b* ≈ 1.92</b>, the AIMA textbook example. A b* close to 1 "
        "indicates a very good heuristic."),

    MCQ(IN, 1,
        "Heuristics are often derived from <i>relaxed problems</i>, in which some constraints on the "
        "actions are removed. The cost of an optimal solution to a relaxed problem is",
        ["an admissible (and in fact consistent) heuristic for the original problem",
         "always an overestimate of the original problem's optimal cost",
         "always equal to the original problem's optimal cost",
         "inadmissible, but useful for greedy search only"],
        0,
        "The relaxed problem's state-space graph is a supergraph of the original, because it has extra "
        "edges. So every original solution is also a relaxed solution, and the relaxed optimum is "
        "<b>≤ the true cost: admissible</b>. It is also an exact cost in a real problem, so it satisfies "
        "the triangle inequality and is consistent. Hence (B) and (D) are wrong. (C) holds only when the "
        "relaxation happens to be tight."),

    MSQ(IN, 2,
        "The 8-puzzle rule is: a tile can move from square X to square Y if X is adjacent to Y "
        "<i>and</i> Y is blank. Which of the following statements about relaxations are TRUE?",
        ["Dropping both conditions (a tile can move anywhere in one step) gives the misplaced-tiles heuristic h<sub>1</sub>",
         "Dropping only the 'Y is blank' condition gives the Manhattan-distance heuristic h<sub>2</sub>",
         "Dropping only the adjacency condition gives the Manhattan-distance heuristic h<sub>2</sub>",
         "The heuristics obtained from these relaxations are admissible for the original 8-puzzle"],
        [0, 1, 3],
        "(A) is true: if a tile can jump anywhere, each misplaced tile needs exactly 1 move. (B) is true: "
        "if tiles move to adjacent squares regardless of the blank, each tile needs exactly its Manhattan "
        "distance. (C) is false: dropping adjacency but keeping 'Y is blank' gives Gaschnig's heuristic, "
        "not Manhattan distance. (D) is true: optimal costs of relaxed problems are admissible."),

    MCQ(IN, 2,
        "h<sub>1</sub>, …, h<sub>m</sub> are admissible heuristics for a problem. Which composite "
        "heuristic is guaranteed to be admissible <i>and</i> to dominate each h<sub>i</sub>?",
        ["h(n) = h<sub>1</sub>(n) + … + h<sub>m</sub>(n)",
         "h(n) = max(h<sub>1</sub>(n), …, h<sub>m</sub>(n))",
         "h(n) = min(h<sub>1</sub>(n), …, h<sub>m</sub>(n))",
         "h(n) = m · h<sub>1</sub>(n)"],
        1,
        "Each h<sub>i</sub>(n) ≤ h*(n), so their maximum is also ≤ h*(n), and it is ≥ each component by "
        "construction. So the <b>max</b> is admissible and dominates every h<sub>i</sub>. The sum (A) "
        "and the multiple (D) can exceed h*. The min (C) is admissible but is dominated by every "
        "h<sub>i</sub>, not dominating."),

    NAT(IN, 1,
        "Weighted A* uses f(n) = g(n) + W·h(n) with W = 1.5 and an admissible heuristic h. The optimal "
        "solution cost is C* = 40. What is the largest solution cost that weighted A* is guaranteed not "
        "to exceed?",
        60, 60,
        "With an admissible h, weighted A* is W-admissible: the cost it returns is ≤ W·C* = 1.5 × 40 = "
        "<b>60</b>. Inflating h makes the search greedier and faster, and the price is this bounded loss "
        "of optimality."),

    MCQ(IN, 1,
        "Iterative deepening A* (IDA*) uses a cutoff on f = g + h. After an iteration fails, the cutoff "
        "for the next iteration is set to",
        ["the previous cutoff plus 1",
         "the smallest f-value of any node that exceeded the cutoff in the previous iteration",
         "the largest f-value seen in the previous iteration",
         "twice the previous cutoff"],
        1,
        "IDA* raises the threshold to the <b>smallest f-cost that exceeded the old threshold</b>. This "
        "keeps it optimal with an admissible h, because no solution with a smaller f is skipped. "
        "Increment-by-1 (A) assumes integer costs and can waste iterations. The largest f (C) and doubling "
        "(D) can jump past the optimal cost and return a suboptimal solution."),

    MSQ(IN, 2,
        "Which of the following statements about IDA* are TRUE?",
        ["Its memory requirement is linear in the depth of the solution",
         "With an admissible heuristic, it returns an optimal solution",
         "It keeps every previously visited state in memory to avoid repeated states",
         "When step costs are real-valued and almost all distinct, each iteration may add only one new node, which leads to many iterations"],
        [0, 1, 3],
        "(A) is true: each iteration is a depth-first search bounded by the f-cutoff. (B) is true: "
        "thresholds rise to the smallest f that exceeded the old one, so the first goal found is optimal. "
        "(C) is false: IDA* does not keep an explored set, which is exactly why it uses little memory "
        "and why it can re-expand states. (D) is true: this is the well-known weakness, which motivates "
        "RBFS and SMA*."),

    MCQ(IN, 1,
        "A* search with h(n) = 0 for every node n is equivalent to",
        ["breadth-first search", "depth-first search", "uniform-cost search", "greedy best-first search"],
        2,
        "With h = 0, f(n) = g(n), so A* expands nodes in order of path cost, which is <b>uniform-cost "
        "search</b>. It equals BFS (A) only when all step costs are equal. DFS (D) uses a LIFO order. "
        "Greedy search with h ≡ 0 has every node tied, so its behaviour depends entirely on tie-breaking."),

    MCQ(IN, 2,
        "A* graph search runs with a consistent heuristic, and C* is the optimal solution cost. Which "
        "statement is correct?",
        ["Every node reachable from the start with f(n) &lt; C* is expanded",
         "No node with f(n) &lt; C* is ever expanded",
         "Nodes with f(n) &gt; C* may be expanded before the goal is selected",
         "A* expands exactly the nodes on the optimal path and no others"],
        0,
        "With a consistent h, A* expands nodes in non-decreasing order of f. It therefore expands "
        "<b>all nodes with f &lt; C*</b>, some nodes with f = C*, and none with f &gt; C*. (B) is the "
        "opposite. (C) contradicts that ordering, because the goal with f = C* would be selected first. "
        "(D) is true only for a perfect heuristic with favourable tie-breaking."),

    NAT(IN, 2,
        G2 + "A* graph search is run from S. It goal-tests a node when the node is selected from the "
        "frontier, and it keeps the cheapest entry for each state. How many nodes are selected from the "
        "frontier for expansion, <i>including</i> the selection of G that ends the search?",
        5, 5,
        "f(S)=5. Expand S: A(g=2, f=6), B(g=4, f=8). Expand A (f=6): C(g=4, f=7), D(g=6, f=8). Expand "
        "C (f=7): D improves to g=5, f=7, and G is added with g=9, f=9. Expand D (f=7): G improves to "
        "g=7, f=7. Select G (f=7) and stop with cost 7 via S→A→C→D→G. Selections: S, A, C, D, G = "
        "<b>5</b>. B (f=8) is never expanded."),

    MCQ(IN, 1,
        "In route finding on a road map, why is the straight-line (Euclidean) distance to the "
        "destination an admissible heuristic?",
        ["Because it is easy to compute",
         "Because the shortest route between two points can never be shorter than the straight line between them",
         "Because roads are always straight",
         "Because it equals the true road distance"],
        1,
        "Admissibility needs h(n) ≤ h*(n). Any road route is a path in the plane, and no path is "
        "<b>shorter than the straight line</b> between its endpoints, so the heuristic never "
        "overestimates. Being cheap to compute (A) is useful but irrelevant to admissibility. Roads are "
        "generally not straight (C), and the heuristic generally underestimates rather than equals the "
        "road distance (D)."),

    MSQ(IN, 1,
        "h<sub>1</sub> and h<sub>2</sub> are admissible heuristics. Which of the following are "
        "<b>guaranteed</b> to be admissible?",
        ["max(h<sub>1</sub>, h<sub>2</sub>)", "(h<sub>1</sub> + h<sub>2</sub>) / 2",
         "h<sub>1</sub> + h<sub>2</sub>", "0.5 · h<sub>1</sub>"],
        [0, 1, 3],
        "Since h<sub>1</sub>, h<sub>2</sub> ≤ h*, the max is ≤ h* (A), the average is ≤ h* (B), and any "
        "non-negative multiple ≤ 1 such as 0.5·h<sub>1</sub> is ≤ h* (D). The sum (C) can reach "
        "2h*, for example when both heuristics equal h*, so it is not guaranteed admissible."),

    MCQ(IN, 2,
        "Weighted A* uses f(n) = g(n) + W·h(n). As the weight W → ∞, the order in which it expands "
        "nodes approaches that of",
        ["uniform-cost search", "A* search", "greedy best-first search", "breadth-first search"],
        2,
        "For very large W, the term W·h dominates g, so nodes are effectively ordered by h alone, which "
        "is <b>greedy best-first search</b>. W = 1 gives A* (B). W = 0 gives UCS (A). BFS (D) would need "
        "ordering by depth."),

    MSQ(IN, 2,
        "Which of the following statements about greedy best-first search are TRUE?",
        ["The graph-search version is complete in finite state spaces",
         "It is optimal whenever the heuristic is admissible",
         "Its worst-case time and space complexity is O(b<sup>m</sup>), where m is the maximum depth",
         "If h(n) = h*(n) exactly, greedy best-first search always returns an optimal solution"],
        [0, 2],
        "(A) is true: in a finite space with an explored set, it eventually expands every state. (B) is "
        "false: greedy search ignores g, so admissibility does not help. (C) is true, as stated in AIMA. "
        "(D) is false. Counterexample: S→A costs 100 and A→G costs 1, while S→B costs 1 and B→G costs 2. "
        "Then h*(A)=1 &lt; h*(B)=2, so greedy expands A and returns cost 101 instead of 3. A perfect "
        "heuristic makes <i>A*</i> optimal, not greedy search."),

    MCQ(IN, 2,
        G2 + "What is the cost of the optimal path from S to G, and is h consistent?",
        ["Cost 7; h is consistent", "Cost 7; h is not consistent",
         "Cost 8; h is consistent", "Cost 9; h is not consistent"],
        0,
        "Path costs: S→A→C→D→G = 2+2+1+2 = 7; S→A→C→G = 9; S→A→D→G = 8; S→B→C→D→G = 8; "
        "S→B→C→G = 10. The optimum is <b>7</b>. Consistency, edge by edge: S→A: 5 ≤ 2+4. S→B: 5 ≤ 4+4. "
        "A→C: 4 ≤ 2+3. A→D: 4 ≤ 4+2. B→C: 4 ≤ 1+3. C→D: 3 ≤ 1+2. C→G: 3 ≤ 5+0. D→G: 2 ≤ 2+0. "
        "All hold, so <b>h is consistent</b>."),

    MSQ(IN, 2,
        "In the 8-puzzle, h<sub>1</sub> is the number of misplaced tiles and h<sub>2</sub> is the "
        "total Manhattan distance. Which of the following are TRUE?",
        ["h<sub>2</sub>(n) ≥ h<sub>1</sub>(n) for every state n",
         "Both h<sub>1</sub> and h<sub>2</sub> are consistent",
         "h<sub>1</sub> + h<sub>2</sub> is admissible",
         "The number of reachable states from any start state is 9!/2 = 181440"],
        [0, 1, 3],
        "(A) is true: every misplaced tile is at Manhattan distance at least 1, so h<sub>2</sub> ≥ "
        "h<sub>1</sub>. (B) is true: one move changes h<sub>1</sub> by at most 1 and h<sub>2</sub> by "
        "exactly 1, while the step cost is 1. (C) is false: in a state one move from the goal, "
        "h<sub>1</sub> = h<sub>2</sub> = 1, so the sum is 2 &gt; h* = 1. (D) is true: the parity "
        "invariant splits the 9! states into two halves that cannot reach each other."),

    MCQ(IN, 2,
        "A* tree search uses an admissible h, the optimal goal is G<sub>1</sub> with cost C*, and "
        "G<sub>2</sub> is a suboptimal goal with g(G<sub>2</sub>) &gt; C*. Why can G<sub>2</sub> never "
        "be selected for expansion before G<sub>1</sub>?",
        ["Because h(G<sub>2</sub>) &gt; h(G<sub>1</sub>)",
         "Because some node n on the optimal path is always in the frontier with f(n) ≤ C* &lt; g(G<sub>2</sub>) = f(G<sub>2</sub>)",
         "Because A* expands nodes in order of depth",
         "Because G<sub>2</sub> is never generated"],
        1,
        "This is the standard optimality proof. Until G<sub>1</sub> is selected, some node n on the "
        "optimal path is still in the frontier, and admissibility gives f(n) = g(n) + h(n) ≤ C*. Also "
        "f(G<sub>2</sub>) = g(G<sub>2</sub>) &gt; C* because h(goal) = 0. So n, and eventually "
        "G<sub>1</sub>, are selected before G<sub>2</sub>. (A) is wrong because h = 0 at every goal. "
        "(C) is wrong because A* orders by f, not depth. (D) is wrong because G<sub>2</sub> may well be "
        "generated, just not selected."),

    # ------------------------------------------------------------------
    # ADVERSARIAL SEARCH
    # ------------------------------------------------------------------
    NAT(AD, 1,
        "A two-ply game tree has a MAX root with four MIN children. Their leaf values, left to right, are: "
        "MIN<sub>1</sub>: (10, 9, 14); MIN<sub>2</sub>: (11, 8, 20); MIN<sub>3</sub>: (2, 15, 30); "
        "MIN<sub>4</sub>: (12, 13, 7). What is the minimax value of the root?",
        9, 9,
        "Each MIN node takes the minimum of its leaves: MIN<sub>1</sub> = 9, MIN<sub>2</sub> = 8, "
        "MIN<sub>3</sub> = 2, MIN<sub>4</sub> = 7. The root takes the maximum: max(9, 8, 2, 7) = <b>9</b>, "
        "so MAX plays the first move."),

    NAT(AD, 2,
        "A two-ply game tree has a MAX root with four MIN children, whose leaves are listed left to right: "
        "MIN<sub>1</sub>: (10, 9, 14); MIN<sub>2</sub>: (11, 8, 20); MIN<sub>3</sub>: (2, 15, 30); "
        "MIN<sub>4</sub>: (12, 13, 7). Alpha-beta pruning visits children left to right. How many leaves "
        "are <b>pruned</b> (never evaluated)?",
        3, 3,
        "MIN<sub>1</sub>: evaluate 10, 9, 14, giving 9, so α = 9 at the root. MIN<sub>2</sub>: 11, then "
        "8 ≤ α, so prune 20. MIN<sub>3</sub>: 2 ≤ α, so prune 15 and 30. MIN<sub>4</sub>: 12, 13, 7 are "
        "all evaluated, because the running minimum stays above 9 until the last leaf. Evaluated leaves: "
        "9 of 12. Pruned: 20, 15, 30 = <b>3</b>."),

    NAT(AD, 2,
        "A three-ply binary game tree has levels MAX (root), MIN, MAX, and then leaves. The eight leaf "
        "values, left to right, are 5, 6, 7, 4, 5, 3, 6, 7. Each MAX node at the third level owns two "
        "consecutive leaves. Alpha-beta pruning processes children left to right. How many leaves are "
        "<b>evaluated</b>?",
        5, 5,
        "The leftmost MAX node sees (5, 6) and returns 6, so its MIN parent has β = 6. The next MAX node "
        "sees 7 ≥ β and prunes leaf 4. The left MIN node therefore has value 6, and the root gets α = 6. "
        "In the right MIN subtree, the first MAX node sees 5 and then 3 and returns 5. The MIN node's "
        "value is now ≤ 5 ≤ α, so the whole MAX subtree with leaves (6, 7) is pruned. Evaluated leaves: "
        "5, 6, 7, 5, 3 = <b>5</b>. The root value is 6."),

    NAT(AD, 2,
        "A game tree has a MAX root with three MIN children. Each MIN child has two MAX children, and each "
        "of those has two leaves, for 12 leaves in total. The leaves, left to right, are "
        "4, 8, 9, 3, 2, 1, 7, 6, 5, 10, 2, 11. Alpha-beta pruning processes children left to right. How "
        "many leaves are <b>evaluated</b>?",
        9, 9,
        "MIN<sub>1</sub>: MAX(4, 8) = 8, so β = 8. The next MAX node sees 9 ≥ 8 and prunes leaf 3. "
        "MIN<sub>1</sub> = 8, so root α = 8. MIN<sub>2</sub>: MAX(2, 1) = 2 ≤ α, so the MAX node with "
        "leaves (7, 6) is pruned. MIN<sub>3</sub>: MAX(5, 10) = 10, so β = 10. MAX(2, 11): leaf 2 does not "
        "cut and 11 ≥ 10 cuts, but no siblings remain, so both are evaluated. MIN<sub>3</sub> = 10, and "
        "the root value is 10. Pruned: 3, 7, 6. Evaluated: 12 − 3 = <b>9</b>."),

    NAT(AD, 1,
        "A uniform game tree has branching factor b = 3 and depth d = 4 plies. Alpha-beta search "
        "examines the moves in perfect order. Using the best-case formula b<sup>⌈d/2⌉</sup> + "
        "b<sup>⌊d/2⌋</sup> − 1, how many leaves are evaluated?",
        17, 17,
        "3<sup>2</sup> + 3<sup>2</sup> − 1 = 9 + 9 − 1 = <b>17</b>. Plain minimax evaluates "
        "3<sup>4</sup> = 81 leaves, so perfect ordering saves 64 leaf evaluations."),

    NAT(AD, 1,
        "Chess has an average branching factor of about b = 36. With perfect move ordering, alpha-beta "
        "reduces the effective branching factor from b to √b. What is the effective branching factor?",
        6, 6,
        "Perfect ordering gives O(b<sup>m/2</sup>) = O((√b)<sup>m</sup>). The effective branching factor "
        "is √36 = <b>6</b>. Equivalently, alpha-beta can search roughly twice as deep as minimax in the "
        "same time."),

    MCQ(AD, 1,
        "With perfect move ordering, the time complexity of alpha-beta search to depth m with branching "
        "factor b is",
        ["O(b<sup>m</sup>)", "O(b<sup>m/2</sup>)", "O(b<sup>3m/4</sup>)", "O(bm)"],
        1,
        "Perfect ordering examines about b<sup>⌈m/2⌉</sup> + b<sup>⌊m/2⌋</sup> − 1 leaves, which is "
        "<b>O(b<sup>m/2</sup>)</b>. O(b<sup>m</sup>) is minimax, or the worst ordering (A). "
        "O(b<sup>3m/4</sup>) is the random-ordering estimate (C). O(bm) is minimax's space, not its "
        "time (D)."),

    MCQ(AD, 1,
        "When successors are examined in <b>random</b> order, alpha-beta search is expected to examine "
        "roughly",
        ["O(b<sup>m/2</sup>) nodes", "O(b<sup>3m/4</sup>) nodes", "O(b<sup>m</sup>) nodes",
         "O(m·b) nodes"],
        1,
        "AIMA reports that random move ordering gives about <b>O(b<sup>3m/4</sup>)</b> for moderate b. "
        "O(b<sup>m/2</sup>) (A) needs perfect ordering. O(b<sup>m</sup>) (C) is the worst case. O(mb) (D) "
        "is a space bound."),

    MSQ(AD, 2,
        "Which of the following statements about alpha-beta pruning are TRUE?",
        ["It returns the same root value as minimax",
         "A pruned subtree cannot change the root's minimax decision",
         "Move ordering affects how much is pruned, but not the root value",
         "It can be applied unchanged to expectimax trees containing chance nodes, with the same pruning conditions"],
        [0, 1, 2],
        "(A), (B) and (C) are the defining properties of alpha-beta: it prunes only subtrees that "
        "provably cannot affect the decision, so the result matches minimax for any ordering, and only "
        "the amount of pruning changes. (D) is false: the value of a chance node is an average, so one "
        "child does not bound it. Pruning there needs extra bounds on the leaf values and modified "
        "conditions."),

    MCQ(AD, 1,
        "In alpha-beta search, α denotes",
        ["the value of the best choice (highest value) found so far for MAX along the current path",
         "the value of the best choice (lowest value) found so far for MIN along the current path",
         "the depth limit",
         "the number of pruned nodes"],
        0,
        "<b>α is MAX's best guaranteed value so far</b>, a lower bound, along the path to the root. "
        "β is MIN's best value so far, an upper bound (B). A branch is cut when the bounds cross, i.e. "
        "when α ≥ β. (C) and (D) are not what α means."),

    NAT(AD, 2,
        "A MAX root has two chance-node children. Chance node C<sub>1</sub> leads with probability 0.4 to "
        "a MIN node with leaves (6, 10) and with probability 0.6 to a MIN node with leaves (3, 9). Chance "
        "node C<sub>2</sub> leads with probability 0.5 to a leaf of value 8 and with probability 0.5 to a "
        "leaf of value 1. What is the expectiminimax value of the root?",
        4.5, 4.5,
        "The MIN nodes under C<sub>1</sub> have values min(6,10) = 6 and min(3,9) = 3. "
        "C<sub>1</sub> = 0.4·6 + 0.6·3 = 2.4 + 1.8 = 4.2. C<sub>2</sub> = 0.5·8 + 0.5·1 = 4.5. "
        "Root = max(4.2, 4.5) = <b>4.5</b>, so MAX chooses C<sub>2</sub>."),

    MCQ(AD, 2,
        "MAX has two moves, each leading to a chance node with two equally likely outcomes. Move A has "
        "leaf values (0, 10) and move B has leaf values (4, 5). Every leaf value is then replaced by its "
        "square root. Which move does expectimax choose before and after the transformation?",
        ["A before, A after", "A before, B after", "B before, A after", "B before, B after"],
        1,
        "Before: E[A] = (0+10)/2 = 5 and E[B] = 4.5, so A is chosen. After: E[A] = (0 + 3.162)/2 ≈ 1.58 "
        "and E[B] = (2 + 2.236)/2 ≈ 2.12, so B is chosen. Expectimax decisions are preserved only by "
        "<i>positive linear</i> transformations of the evaluation function. A merely order-preserving "
        "map such as √x can change them. Minimax decisions are invariant under any order-preserving "
        "map."),

    MSQ(AD, 1,
        "Which of the following statements about two-player zero-sum games are TRUE?",
        ["The players' utilities sum to the same constant in every terminal state",
         "Chess, with outcomes +1/0/−1 or 1/½/0, can be modelled as a zero-sum (constant-sum) game",
         "Minimax assumes that the opponent plays optimally",
         "In a zero-sum game, both players can strictly gain from the same outcome change"],
        [0, 1, 2],
        "(A) is the definition of zero-sum (constant-sum). (B) is true: AIMA notes that chess's payoffs "
        "always total a constant. (C) is true: minimax computes the best play against a perfect, "
        "adversarial opponent. (D) is false: since the sum is constant, one player's gain is exactly the "
        "other's loss."),

    MSQ(AD, 2,
        "Minimax search (depth-first) runs on a finite game tree with branching factor b and maximum depth "
        "m. Which of the following are TRUE?",
        ["Its time complexity is O(b<sup>m</sup>)",
         "Its space complexity is O(bm) when all successors are generated at once",
         "Against an optimal opponent, the minimax strategy achieves the minimax value of the root",
         "It needs a heuristic evaluation function even when every path can be searched to a terminal state"],
        [0, 1, 2],
        "(A) and (B) are true: minimax is a complete depth-first exploration of the tree. (C) is true: "
        "minimax is optimal against an optimal adversary and guarantees the root's minimax value. (D) is "
        "false: when the search reaches terminal states, the exact utilities are used. An evaluation "
        "function is needed only when the search is cut off early."),

    NAT(AD, 1,
        "A chess evaluation function is the weighted linear function Eval = 9·Δq + 5·Δr + 3·Δb + 1·Δp, "
        "where each Δ is White's count minus Black's count of queens, rooks, bishops and pawns. In a "
        "position, the queens are equal, White has one extra rook, Black has one extra bishop, and White "
        "has two extra pawns. What is Eval?",
        4, 4,
        "Δq = 0, Δr = +1, Δb = −1, Δp = +2. Eval = 9·0 + 5·1 + 3·(−1) + 1·2 = 0 + 5 − 3 + 2 = <b>4</b>. "
        "A weighted linear evaluation function treats features as independent contributions."),

    MSQ(AD, 2,
        "Which of the following statements about depth-limited (cutoff) game search with heuristic "
        "evaluation functions are TRUE?",
        ["The horizon effect occurs when an unavoidable damaging event is pushed beyond the search depth by delaying moves",
         "Quiescence search extends the search at non-quiescent positions, such as pending captures, before applying the evaluation function",
         "A good evaluation function should be strongly correlated with the actual chance of winning",
         "Increasing the cutoff depth by a fixed amount always removes the horizon effect"],
        [0, 1, 2],
        "(A) defines the horizon effect. (B) defines quiescence search, which applies the evaluation "
        "function only at quiet positions. (C) is the AIMA requirement for evaluation functions. (D) is "
        "false: at any fixed depth, a delaying tactic can push the bad event just beyond the new "
        "horizon."),

    MCQ(AD, 2,
        "A three-ply binary game tree has levels MAX (root), MIN, MAX, and then leaves. The leaves, left to "
        "right, are 3, 4, 2, 9, 7, 1, 8, 6. Each bottom MAX node owns two consecutive leaves. Alpha-beta "
        "processes children left to right. Which statement is correct?",
        ["Root value 7; only the last leaf (6) is pruned",
         "Root value 4; leaves 2 and 9 are pruned",
         "Root value 7; leaves 1 and 6 are pruned",
         "Root value 8; no leaf is pruned"],
        0,
        "Left MIN: MAX(3,4) = 4, so β = 4. MAX(2,9): leaf 2 does not cut, and 9 ≥ 4 cuts, but it is the "
        "last child, so both leaves are evaluated. Left MIN = 4 and root α = 4. Right MIN: MAX(7,1) = 7 "
        "(7 &gt; α, so no cut), so β = 7. MAX(8, 6): 8 ≥ β = 7, so leaf 6 is pruned. Right MIN = 7, and "
        "the root is max(4, 7) = <b>7</b>. Only leaf 6 is pruned, so (A) is correct. Leaf 1 must be "
        "evaluated because 7 &gt; α at that point."),

    MCQ(AD, 1,
        "Chess has an average branching factor of about 35, and a game lasts about 100 plies. The full "
        "game tree therefore has about how many nodes?",
        ["10<sup>40</sup>", "10<sup>100</sup>", "10<sup>154</sup>", "10<sup>400</sup>"],
        2,
        "35<sup>100</sup> = 10<sup>100·log<sub>10</sub>35</sup> ≈ 10<sup>100×1.544</sup> ≈ "
        "<b>10<sup>154</sup></b>, the AIMA estimate. 10<sup>40</sup> (A) is AIMA's estimate of the number "
        "of distinct chess positions, not of the tree. (B) and (D) do not match the calculation."),

    MCQ(AD, 2,
        "To get the maximum pruning from alpha-beta search, how should children be ordered?",
        ["At MAX nodes in decreasing order of value, at MIN nodes in increasing order of value",
         "At MAX nodes in increasing order of value, at MIN nodes in decreasing order of value",
         "In increasing order at both node types",
         "Ordering does not affect pruning"],
        0,
        "Pruning is greatest when the best move is examined first: the highest value for MAX and the "
        "lowest for MIN. That gives the tightest α (or β) as early as possible, so later siblings are cut "
        "sooner. (B) is the worst ordering, under which alpha-beta degenerates to O(b<sup>m</sup>). (C) is "
        "best for only one of the two players. (D) is false: ordering decides whether the cost is "
        "O(b<sup>m/2</sup>) or O(b<sup>m</sup>)."),

    MSQ(AD, 2,
        "Which of the following statements about expectimax / expectiminimax are TRUE?",
        ["The value of a chance node is the probability-weighted average of its children's values",
         "With n distinct chance outcomes per chance layer, the time complexity becomes O(b<sup>m</sup> n<sup>m</sup>)",
         "Pruning at chance nodes is impossible even when leaf values are known to lie in a bounded range",
         "Expectimax is appropriate when the opponent's or environment's moves are random rather than optimally adversarial"],
        [0, 1, 3],
        "(A) is the definition of a chance node's value. (B) is the AIMA bound for expectiminimax. (C) is "
        "false: if utilities are bounded, a chance node's average can be bounded before all of its "
        "children are seen, so some pruning is possible. (D) is true: expectimax models stochastic "
        "behaviour, while minimax models a worst-case adversary."),

    MCQ(AD, 1,
        "In alpha-beta search, while a MIN node is being evaluated with current bounds (α, β), the "
        "remaining children of the MIN node can be pruned as soon as its running value v satisfies",
        ["v ≥ β", "v ≤ α", "v ≥ α", "v ≤ β"],
        1,
        "A MIN node's value can only decrease as more children are seen. Once <b>v ≤ α</b>, MAX already "
        "has an alternative worth α higher up the tree and will never let play reach this node. "
        "v ≥ β (A) is the cutoff test at MAX nodes. (C) and (D) do not justify pruning."),

    NAT(AD, 1,
        "Tic-tac-toe has 9 squares. If early wins are ignored and every game continues until all 9 squares "
        "are filled, how many distinct move sequences (orderings of the 9 moves) are there?",
        362880, 362880,
        "The first move has 9 choices, the second 8, and so on, giving 9! = <b>362880</b> sequences. "
        "This is AIMA's upper bound on the size of the tic-tac-toe game tree. Games that end early make "
        "the actual tree smaller."),

    # ------------------------------------------------------------------
    # PROBLEM FORMULATION
    # ------------------------------------------------------------------
    NAT(PF, 1,
        "The 8-puzzle has 9!/2 states reachable from any given start state. Compute this number.",
        181440, 181440,
        "9! = 362880. The parity of a permutation splits the states into two disjoint halves, and no "
        "sequence of moves crosses from one half to the other. So 362880/2 = <b>181440</b> states are "
        "reachable."),

    NAT(PF, 2,
        "The 4-queens problem uses the improved incremental formulation. A state places k queens "
        "(0 ≤ k ≤ 4), one in each of the leftmost k columns, with no two queens attacking each other. "
        "Including the empty board (k = 0), how many states are in this state space?",
        17, 17,
        "k = 0: 1 state. k = 1: 4 states. k = 2: the pairs of rows (r<sub>1</sub>, r<sub>2</sub>) with "
        "|r<sub>1</sub>−r<sub>2</sub>| ≥ 2 are (1,3), (1,4), (2,4), (3,1), (4,1), (4,2), so 6 states. "
        "k = 3: extending these without attack gives (1,4,2), (2,4,1), (3,1,4), (4,1,3), so 4 states. "
        "k = 4: the two solutions (2,4,1,3) and (3,1,4,2). Total = 1+4+6+4+2 = <b>17</b>. For "
        "8-queens, the same formulation gives AIMA's 2057 states."),

    NAT(PF, 1,
        "In the vacuum world with n = 3 squares in a row, a state specifies the agent's location and "
        "whether each square is dirty or clean. How many states are there?",
        24, 24,
        "The agent can be in any of 3 squares, and each of the 3 squares is dirty or clean, giving "
        "2<sup>3</sup> combinations. States = n·2<sup>n</sup> = 3 × 8 = <b>24</b>. The 2-square world "
        "has 2·2<sup>2</sup> = 8 states."),

    NAT(PF, 2,
        "In the missionaries-and-cannibals problem (3 of each, a boat with capacity 2), a state is "
        "(m, c, b), where m and c are the numbers of missionaries and cannibals on the left bank "
        "(0 to 3 each) and b ∈ {left, right} is the boat's side. A state is <i>safe</i> if, on each bank, "
        "the missionaries are either zero or at least as many as the cannibals. How many safe states "
        "are there, counting both boat positions and ignoring reachability?",
        20, 20,
        "Count the safe (m, c) pairs. m = 0: the right bank has 3 missionaries, so every c = 0..3 is "
        "safe, giving 4 pairs. m = 3: the left bank needs c ≤ 3 and the right bank has no missionaries, "
        "giving 4 pairs. m = 1: the left bank needs c ≤ 1 and the right bank (2 missionaries, 3−c "
        "cannibals) needs 3−c ≤ 2, so c = 1: 1 pair. m = 2: c ≤ 2 and 3−c ≤ 1, so c = 2: 1 pair. That "
        "gives 10 pairs, and 2 boat positions give <b>20</b> states. (Only 16 of them are reachable "
        "from (3,3,left).)"),

    NAT(PF, 1,
        "The Tower of Hanoi has 3 pegs and 4 disks of distinct sizes, and a larger disk may never sit on "
        "a smaller one. How many distinct legal states are there?",
        81, 81,
        "Each disk can be on any of the 3 pegs. For a given assignment of disks to pegs, the size rule "
        "allows exactly one legal stacking order on each peg. So the number of states is "
        "3<sup>4</sup> = <b>81</b>."),

    MCQ(PF, 1,
        "In AIMA, a search problem is formally defined by",
        ["initial state, actions, transition model, goal test, and path (action) cost function",
         "initial state and goal state only",
         "a heuristic function and an evaluation function",
         "a frontier and an explored set"],
        0,
        "A problem consists of the <b>initial state, the actions available in each state, the transition "
        "model RESULT(s,a), the goal test, and the action-cost / path-cost function</b>. Together these "
        "define the state space implicitly. (B) leaves out actions and costs. (C) belongs to particular "
        "algorithms, not to the problem. (D) is the data structure of a search algorithm."),

    MSQ(PF, 2,
        "Which of the following statements match standard (AIMA) definitions of the terms used to "
        "analyse search algorithms?",
        ["Completeness: the algorithm is guaranteed to find a solution when one exists",
         "Cost-optimality: the algorithm finds a solution with the lowest path cost among all solutions",
         "b, the branching factor, is the maximum number of successors of any node",
         "d is the depth of the deepest node in the state space"],
        [0, 1, 2],
        "(A), (B) and (C) are the textbook definitions. (D) is false: d is the depth of the "
        "<b>shallowest</b> goal node. The maximum length of any path in the state space is m."),

    MCQ(PF, 2,
        "For 8-queens, the complete-state formulation places exactly one queen in each column, in any "
        "row, with attacks allowed. How many states does this formulation have?",
        ["8<sup>8</sup> = 16,777,216", "64<sup>8</sup>", "C(64, 8) = 4,426,165,368", "8! = 40,320"],
        0,
        "Each of the 8 columns independently holds its queen in one of 8 rows, giving "
        "<b>8<sup>8</sup> = 16,777,216</b> states. C(64,8) (C) counts any 8 squares without the "
        "one-per-column constraint. 64<sup>8</sup> (B) counts ordered placements of distinguishable "
        "queens. 8! (D) also requires distinct rows."),

    MCQ(PF, 1,
        "In a search problem, the state space is defined implicitly by",
        ["the initial state, the actions, and the transition model",
         "the goal test only",
         "the heuristic function",
         "the path cost function only"],
        0,
        "Starting from the <b>initial state</b> and applying the <b>actions</b> through the "
        "<b>transition model</b> generates every reachable state and the edges between them, which is "
        "the state-space graph. The goal test (B) only identifies goal states. The heuristic (C) guides "
        "search but does not define states. The path cost (D) only labels edges."),

    MSQ(PF, 2,
        "In a grid route-finding problem, the agent moves N, S, E or W at cost 1 per move. The start "
        "state is (0,0), the only goal is (3,2), and there are no obstacles in an unbounded grid. Which of "
        "the following are TRUE?",
        ["The optimal solution cost is 5",
         "BFS with graph search is optimal for this problem",
         "Manhattan distance is a consistent heuristic for this problem",
         "The branching factor b is 8"],
        [0, 1, 2],
        "(A) is true: the shortest path needs |3| + |2| = 5 unit moves. (B) is true: costs are uniform, "
        "so the shallowest goal is cheapest. (C) is true: one move changes the Manhattan distance by "
        "exactly 1 = the step cost, so h(n) ≤ 1 + h(n′). (D) is false: there are 4 actions, so b = 4. "
        "b = 8 would need diagonal moves."),

    # ------------------------------------------------------------------
    # LOCAL SEARCH
    # ------------------------------------------------------------------
    NAT(LO, 1,
        "In the 8-queens complete-state formulation (one queen per column), the successors of a state are "
        "all states obtained by moving a single queen to a different square in the same column. How many "
        "successors does each state have?",
        56, 56,
        "Each of the 8 queens can move to any of the 7 other squares in its column, giving 8 × 7 = "
        "<b>56</b> successors. Steepest-ascent hill climbing evaluates all 56 and picks the best."),

    NAT(LO, 2,
        "In simulated annealing, a randomly chosen move worsens the objective (which is being maximised) "
        "by ΔE = −2 at temperature T = 4. With what probability is this move accepted? Give the answer "
        "to two decimal places.",
        0.60, 0.61,
        "A worsening move is accepted with probability e<sup>ΔE/T</sup> = e<sup>−2/4</sup> = "
        "e<sup>−0.5</sup> ≈ <b>0.6065</b>, which rounds to 0.61. Lower temperatures or larger losses "
        "make acceptance less likely. Improving moves (ΔE &gt; 0) are always accepted."),

    MSQ(LO, 1,
        "Steepest-ascent hill climbing (maximisation, moves only to a strictly better neighbour) can halt "
        "without reaching a global maximum because of which of the following?",
        ["A local maximum",
         "A plateau or shoulder (a flat region where all neighbours have equal value)",
         "A ridge (a sequence of local maxima that single moves cannot climb)",
         "A state where the neighbour with the highest value is better than the current state"],
        [0, 1, 2],
        "(A), (B) and (C) are the three classic traps listed in AIMA. At a local maximum no neighbour is "
        "better. On a plateau no neighbour is strictly better. On a ridge every single-move neighbour is "
        "worse even though the ridge rises. (D) is false: if the best neighbour is better, hill climbing "
        "moves there and does not halt."),

    MSQ(LO, 2,
        "Which of the following statements about simulated annealing (maximisation) are TRUE?",
        ["If the temperature is lowered slowly enough, it finds a global optimum with probability approaching 1",
         "It always accepts a move that improves the objective",
         "At very high temperature, it behaves almost like a random walk",
         "At T = 0, it accepts worsening moves with probability 1"],
        [0, 1, 2],
        "(A) is the classical convergence result for sufficiently slow cooling. (B) is true: moves with "
        "ΔE &gt; 0 are always taken. (C) is true: e<sup>ΔE/T</sup> → 1 as T → ∞, so almost every move "
        "is accepted. (D) is false: as T → 0, e<sup>ΔE/T</sup> → 0 for ΔE &lt; 0, so worsening moves are "
        "rejected and the algorithm becomes hill climbing."),

    MCQ(LO, 2,
        "Steepest-ascent hill climbing solves a random 8-queens instance with probability p ≈ 0.14. "
        "Random-restart hill climbing repeats independent trials until one succeeds. What is the expected "
        "number of trials?",
        ["About 1.14", "About 3", "About 7", "About 14"],
        2,
        "The number of trials until the first success is geometrically distributed with mean 1/p = "
        "1/0.14 ≈ <b>7</b>. That means about 6 failures and 1 success, matching AIMA's analysis. (A) "
        "confuses 1/p with 1 + p. (D) confuses 1/p with 100·p."),

    MSQ(LO, 1,
        "Which of the following statements about local search are TRUE?",
        ["Local beam search with k states passes useful information among the k parallel searches",
         "Local beam search with k = 1 is equivalent to hill climbing",
         "Hill climbing stores the whole search tree in memory",
         "Typical local-search algorithms use only a constant amount of memory"],
        [0, 1, 3],
        "(A) is true: beam search selects the k best successors from the pooled successors of all k "
        "states. (B) is true: with one state, keeping the best successor is hill climbing. (C) is false: "
        "hill climbing keeps only the current state, not a tree or paths. (D) is true: local search keeps "
        "just the current state or states."),

    # ------------------------------------------------------------------
    # MORE MIXED QUESTIONS
    # ------------------------------------------------------------------
    MCQ(UN, 2,
        HEAP + "Breadth-first search goal-tests a node when it is generated, generating the left child "
        "before the right, and the goal is node 13. Depth-first search goal-tests on removal from the "
        "frontier, exploring the left child first. Which is correct about the number of nodes each "
        "algorithm goal-tests up to and including node 13 (counting the root)?",
        ["BFS: 13, DFS: 12", "BFS: 13, DFS: 11", "BFS: 12, DFS: 12", "BFS: 7, DFS: 12"],
        0,
        "BFS generates nodes in label order (root, then 2, 3, 4, …), so node 13 is the <b>13th</b> node "
        "tested. DFS preorder is 1, 2, 4, 8, 9, 5, 10, 11, 3, 6, 12, 13, …, so node 13 is the "
        "<b>12th</b>. The other options miscount one or both orders."),

    NAT(IN, 2,
        "In the 8-puzzle, the goal is 1 2 3 / 8 _ 4 / 7 6 5 (rows top to bottom, _ = blank), and the "
        "current state is 2 8 3 / 1 6 4 / 7 _ 5. Let h<sub>1</sub> be the number of misplaced tiles and "
        "h<sub>2</sub> the total Manhattan distance. What is h<sub>1</sub> + h<sub>2</sub>?",
        9, 9,
        "Misplaced tiles: 2 (at (0,0), belongs at (0,1)), 8 (at (0,1), belongs at (1,0)), 1 (at (1,0), "
        "belongs at (0,0)), and 6 (at (1,1), belongs at (2,1)). Tiles 3, 4, 7 and 5 are in place, so "
        "h<sub>1</sub> = 4. Manhattan distances: 2 → 1, 8 → 1+1 = 2, 1 → 1, 6 → 1, so h<sub>2</sub> = 5. "
        "h<sub>1</sub> + h<sub>2</sub> = <b>9</b>. (The sum is not necessarily admissible. This question "
        "is purely arithmetic.)"),
]
