"""Front matter: how to use the book + compact revision notes with diagrams."""
from reportlab.platypus import Paragraph, Spacer, PageBreak, KeepTogether
from reportlab.graphics.shapes import Drawing, String

from common import ST, tbl
from draw import graph_drawing, tree_drawing, legend_game, QUERY_FILL, EVID_FILL


def P(t):
    return Paragraph(t, ST["body"])


def B(t):
    return Paragraph(t, ST["solb"], bulletText="•")


def story(H):
    s = []
    s.append(H("How to Use this Book", "h1", toc=(0, "How to use this book & exam pattern")))
    s.append(P("This book has 100 independent mock tests for <b>Section 7 (Artificial Intelligence)</b> of the "
               "GATE Data Science &amp; AI (DA) syllabus. Each test is timed for 75 minutes and mirrors the GATE "
               "question styles:"))
    s.append(tbl([["Type", "What you do", "Marking"],
                  ["MCQ", "Choose exactly one of four options", "+1 / −1/3 (1-mark); +2 / −2/3 (2-mark)"],
                  ["MSQ", "Choose ALL correct options (one or more)", "Full marks only for exactly the correct set; no negative"],
                  ["NAT", "Type a number (range accepted where stated)", "No negative marking"]],
                 widths=[50, 220, 220], align="LEFT"))
    s.append(Spacer(1, 6))
    s.append(P("<b>Suggested routine.</b> Attempt a test in one sitting without notes, mark your answers, then use "
               "the answer key on the last pages of the test. Read the detailed solution for <i>every</i> question, "
               "including the ones you got right: the traces (frontier contents, α/β values, factor scopes, sample "
               "weights) show exactly the steps an examiner expects. Re-attempt tests where you score below 60%."))
    s.append(P("<b>Conventions used throughout.</b> Unless a question says otherwise: ties are broken "
               "alphabetically; graph search keeps an explored set; UCS and A* apply the goal test when a node is "
               "selected for expansion; game trees are explored left to right; Bayesian-network variables are Boolean "
               "and CPTs list P(X = T | parents)."))

    # ------------------------------------------------------------- Search notes
    s.append(PageBreak())
    s.append(H("Revision Notes 1 — Search", "h1", toc=(0, "Revision notes: Search")))
    s.append(P("A search problem consists of an initial state, the actions available in a state, a transition model, "
               "a goal test and a step-cost function. b = branching factor, d = depth of the shallowest goal, "
               "m = maximum depth, C* = optimal cost, ε = minimum step cost, ℓ = depth limit."))
    s.append(tbl([["Algorithm", "Frontier / priority", "Complete?", "Optimal?", "Time", "Space"],
                  ["BFS", "FIFO queue", "Yes (finite b)", "Yes if unit costs", "O(b^d)", "O(b^d)"],
                  ["Uniform-cost", "g(n)", "Yes if ε &gt; 0", "Yes", "O(b^(1+⌊C*/ε⌋))", "O(b^(1+⌊C*/ε⌋))"],
                  ["DFS", "LIFO stack", "No (infinite depth / tree search)", "No", "O(b^m)", "O(bm)"],
                  ["Depth-limited", "LIFO, depth ≤ ℓ", "No (if ℓ &lt; d)", "No", "O(b^ℓ)", "O(bℓ)"],
                  ["Iterative deepening", "DLS for ℓ = 0,1,2,…", "Yes", "Yes if unit costs", "O(b^d)", "O(bd)"],
                  ["Bidirectional", "two BFS frontiers", "Yes", "Yes if unit costs", "O(b^(d/2))", "O(b^(d/2))"],
                  ["Greedy best-first", "h(n)", "No (tree); yes finite graph", "No", "O(b^m)", "O(b^m)"],
                  ["A*", "f(n) = g(n) + h(n)", "Yes", "Yes (admissible tree / consistent graph)", "exp.", "exp."],
                  ["IDA*", "f-cost contour limit", "Yes", "Yes (admissible)", "exp.", "O(bd)"]],
                 widths=[78, 92, 95, 115, 60, 55], align="LEFT"))
    s.append(Spacer(1, 6))
    s.append(H("Heuristics", "h3"))
    for t in ["<b>Admissible:</b> h(n) ≤ h*(n) for all n (never overestimates).",
              "<b>Consistent (monotone):</b> h(n) ≤ c(n, a, n′) + h(n′) for every edge and h(goal) = 0. Consistent ⇒ "
              "admissible; with a consistent h, f is non-decreasing along any path and A* graph search never re-opens "
              "a node.",
              "<b>Dominance:</b> if h₂(n) ≥ h₁(n) for all n (both admissible), A* with h₂ expands no more nodes than with h₁. "
              "max(h₁, h₂) of admissible heuristics is admissible and dominates both.",
              "<b>Relaxed problems</b> give admissible heuristics (8-puzzle: misplaced tiles h₁, Manhattan distance h₂ ≥ h₁).",
              "<b>Effective branching factor</b> b*: N + 1 = 1 + b* + (b*)² + … + (b*)^d.",
              "A* expands all nodes with f(n) &lt; C*, some with f(n) = C*, none with f(n) &gt; C*."]:
        s.append(B(t))
    s.append(Spacer(1, 4))
    # worked example
    pos = {"S": (0, 0.5), "A": (0.35, 1), "B": (0.35, 0), "C": (0.7, 0.75), "G": (1, 0.3)}
    edges = [("S", "A", 2), ("S", "B", 5), ("A", "C", 3), ("B", "G", 6), ("C", "G", 4), ("A", "B", 2)]
    note = {"S": "h=7", "A": "h=6", "B": "h=5", "C": "h=4", "G": "h=0"}
    s.append(KeepTogether([
        H("Worked example — A* graph search", "h3"),
        graph_drawing(pos, edges, width=360, height=140, node_note=note, start="S", goal="G"),
        P("f(S)=7 → expand S: A (g=2, f=8), B (g=5, f=10). Expand A (f=8): C (g=5, f=9), B improves to g=4, f=9. "
          "Ties at f=9 are broken alphabetically: expand B: G (g=10, f=10). Expand C (f=9): G improves to g=9, f=9. "
          "Expand G (f=9) ⇒ goal. Path S→A→C→G, cost 9. h is consistent here, e.g. h(S)=7 ≤ 2+h(A)=8.")]))
    s.append(H("Adversarial search", "h3"))
    for t in ["<b>Minimax:</b> MAX picks the child of maximum value, MIN the minimum; complete for finite trees, "
              "optimal against an optimal opponent; time O(b^m), space O(bm).",
              "<b>Alpha–beta:</b> α = best value MAX can guarantee so far on the path; β = best value for MIN. At a MIN "
              "node stop when v ≤ α; at a MAX node stop when v ≥ β. The root value is never changed by pruning.",
              "Perfect move ordering examines b^⌈d/2⌉ + b^⌊d/2⌋ − 1 leaves (≈ O(b^(d/2))), random ordering ≈ O(b^(3d/4)), "
              "worst ordering O(b^d).",
              "<b>Expectimax</b> replaces MIN by chance nodes (probability-weighted average). Its decisions are "
              "invariant only to positive <i>linear</i> transformations of the utilities (minimax: any monotonic "
              "transformation). Alpha–beta style pruning needs bounded utilities at chance nodes."]:
        s.append(B(t))
    tree = {"R": ["R0", "R1", "R2"], "R0": ["a", "b"], "R1": ["c", "d"], "R2": ["e", "f"],
            "a": [], "b": [], "c": [], "d": [], "e": [], "f": []}
    kinds = {"R": "max", "R0": "min", "R1": "min", "R2": "min"}
    vals = {"a": 3, "b": 12, "c": 2, "d": 4, "e": 14, "f": 1}
    names = {"R": "R", "R0": "A", "R1": "B", "R2": "C", "a": "L1", "b": "L2", "c": "L3", "d": "L4", "e": "L5",
             "f": "L6"}
    s.append(KeepTogether([
        H("Worked example — alpha–beta", "h3"),
        tree_drawing(tree, kinds, vals, node_names=names, width=330, marks={"d": "pruned"}),
        legend_game(),
        P("A = min(3, 12) = 3 ⇒ α = 3 at the root. At B the first leaf gives 2 ≤ α = 3 ⇒ L4 is pruned (B ≤ 2). "
          "C: 14 &gt; 3, then 1 ≤ 3 ⇒ C = 1. Root = max(3, ≤2, 1) = 3. One leaf is pruned. With C's children "
          "reversed (1 first), L5 would be pruned as well — move ordering matters.")]))

    # ------------------------------------------------------------- Logic notes
    s.append(PageBreak())
    s.append(H("Revision Notes 2 — Logic", "h1", toc=(0, "Revision notes: Logic")))
    s.append(P("A model is a truth assignment (propositional) or an interpretation (first-order). "
               "α ⊨ β iff every model of α is a model of β. α is <b>valid</b> iff true in all models; "
               "<b>satisfiable</b> iff true in some model. α ⊨ β iff (α → β) is valid iff (α ∧ ¬β) is unsatisfiable "
               "(the basis of proof by refutation)."))
    s.append(tbl([["Equivalence", "Law"],
                  ["α → β ≡ ¬α ∨ β ≡ ¬β → ¬α", "implication elimination, contraposition"],
                  ["α ↔ β ≡ (α → β) ∧ (β → α) ≡ (α ∧ β) ∨ (¬α ∧ ¬β)", "biconditional elimination"],
                  ["¬(α ∧ β) ≡ ¬α ∨ ¬β;  ¬(α ∨ β) ≡ ¬α ∧ ¬β", "De Morgan"],
                  ["α ∧ (β ∨ γ) ≡ (α ∧ β) ∨ (α ∧ γ);  α ∨ (β ∧ γ) ≡ (α ∨ β) ∧ (α ∨ γ)", "distributivity"],
                  ["(α ∧ β) → γ ≡ α → (β → γ)", "exportation"],
                  ["¬∀x P(x) ≡ ∃x ¬P(x);  ¬∃x P(x) ≡ ∀x ¬P(x)", "quantifier negation"],
                  ["∀x (P ∧ Q) ≡ ∀x P ∧ ∀x Q;  ∃x (P ∨ Q) ≡ ∃x P ∨ ∃x Q", "distribution of quantifiers"],
                  ["∃x∀y R(x,y) ⊨ ∀y∃x R(x,y) (converse fails)", "quantifier order"]],
                 widths=[300, 190], align="LEFT"))
    s.append(Spacer(1, 5))
    s.append(tbl([["Inference rule", "Form", "Sound?"],
                  ["Modus ponens", "α → β, α ⊢ β", "yes"],
                  ["Modus tollens", "α → β, ¬β ⊢ ¬α", "yes"],
                  ["Resolution", "(α ∨ ℓ), (¬ℓ ∨ β) ⊢ (α ∨ β)", "yes; refutation-complete"],
                  ["Affirming the consequent", "α → β, β ⊢ α", "NO (fallacy)"],
                  ["Denying the antecedent", "α → β, ¬α ⊢ ¬β", "NO (fallacy)"]],
                 widths=[140, 220, 130], align="LEFT"))
    s.append(Spacer(1, 4))
    for t in ["<b>CNF conversion:</b> eliminate ↔, eliminate →, push ¬ inwards (De Morgan, double negation), "
              "distribute ∨ over ∧. A formula on n variables with k models has 2^n − k maxterms in canonical CNF.",
              "<b>Horn clause:</b> at most one positive literal. <b>Definite clause:</b> exactly one. Forward chaining "
              "(data-driven) and backward chaining (goal-driven) are sound and complete for definite clauses and run in "
              "linear time in the size of the KB.",
              "<b>Resolution:</b> resolve on one complementary pair at a time; deriving □ proves unsatisfiability. "
              "Resolution is not complete for <i>deriving</i> every entailed clause (e.g. weakenings), only for refutation.",
              "<b>Translation patterns:</b> “All P are Q”: ∀x (P(x) → Q(x)). “Some P is Q”: ∃x (P(x) ∧ Q(x)). "
              "The mistakes ∀x (P(x) ∧ Q(x)) and ∃x (P(x) → Q(x)) are classic distractors.",
              "<b>Unification:</b> the MGU makes two atoms identical with the most general substitution; the occurs "
              "check forbids x/f(x). <b>Skolemisation:</b> ∃ inside ∀x₁…∀xₖ becomes a Skolem function f(x₁,…,xₖ); "
              "an outermost ∃ becomes a Skolem constant.",
              "<b>Counting interpretations:</b> a binary relation on n elements is an n×n 0/1 matrix (2^(n²) choices); "
              "reflexive 2^(n²−n), symmetric 2^(n(n+1)/2), antisymmetric 2^n·3^(n(n−1)/2), asymmetric 3^(n(n−1)/2)."]:
        s.append(B(t))

    # ------------------------------------------------------------- Uncertainty notes
    s.append(PageBreak())
    s.append(H("Revision Notes 3 — Reasoning under Uncertainty", "h1", toc=(0, "Revision notes: Uncertainty")))
    for t in ["Product rule P(a ∧ b) = P(a | b) P(b); Bayes' rule P(a | b) = P(b | a) P(a) / P(b); "
              "normalisation P(X | e) = α P(X, e) = α Σ<sub>y</sub> P(X, e, y).",
              "X ⊥ Y | Z iff P(X, Y | Z) = P(X | Z) P(Y | Z) iff P(X | Y, Z) = P(X | Z).",
              "<b>Bayesian network semantics:</b> P(x₁,…,xₙ) = Π P(xᵢ | parents(Xᵢ)). Each node is conditionally "
              "independent of its non-descendants given its parents, and of everything else given its Markov blanket "
              "(parents, children, children's other parents).",
              "<b>Parameter count:</b> Σ (|Xᵢ| − 1) Π<sub>U ∈ Pa(Xᵢ)</sub> |U| (versus Π|Xᵢ| − 1 for the full joint)."]:
        s.append(B(t))
    # three canonical structures
    d = Drawing(480, 95)
    from reportlab.graphics.shapes import Group
    for k, (title, edges) in enumerate([("Chain X → Z → Y", [("X", "Z"), ("Z", "Y")]),
                                        ("Fork X ← Z → Y", [("Z", "X"), ("Z", "Y")]),
                                        ("Collider X → Z ← Y", [("X", "Z"), ("Y", "Z")])]):
        pos = {"X": (0, 0.0), "Z": (0.5, 1.0), "Y": (1, 0.0)}
        g = graph_drawing(pos, [(a, b, None) for a, b in edges], directed=True, width=150, height=80,
                          fills={"Z": EVID_FILL}, margin=18, title=title)
        grp = Group(*g.contents)
        grp.translate(k * 160, 0)
        d.add(grp)
    s.append(KeepTogether([H("d-separation: the three canonical connections", "h3"), d,
                           tbl([["Structure", "Z unobserved", "Z observed (or, for a collider, a descendant of Z)"],
                                ["Chain X → Z → Y", "active (X, Y dependent)", "blocked: X ⊥ Y | Z"],
                                ["Fork X ← Z → Y", "active", "blocked: X ⊥ Y | Z (common cause)"],
                                ["Collider X → Z ← Y", "blocked: X ⊥ Y", "active — “explaining away”"]],
                               widths=[120, 140, 230], align="LEFT")]))
    s.append(Spacer(1, 5))
    s.append(H("Exact inference by variable elimination", "h3"))
    for t in ["Start with one factor per CPT, instantiating the evidence. For each hidden variable Z (in the chosen order): "
              "multiply all factors mentioning Z (pointwise product), then sum Z out. Multiply the remaining factors "
              "and normalise.",
              "Cost is dominated by the largest factor created — exponential in its number of variables. On polytrees "
              "(singly connected networks) VE is linear in network size; in general exact inference is NP-hard "
              "(#P-hard) and the best ordering is itself NP-hard to find.",
              "Every variable that is not an ancestor of the query or evidence variables is irrelevant and can be removed "
              "before elimination (it sums out to 1)."]:
        s.append(B(t))
    s.append(H("Approximate inference by sampling", "h3"))
    s.append(tbl([["Method", "How a sample is produced", "Estimate of P(X | e)", "Notes"],
                  ["Prior (direct)", "sample every variable in topological order from P(Xᵢ | parents)",
                   "fraction of samples (no evidence)", "S<sub>PS</sub>(x) = P(x); consistent"],
                  ["Rejection", "prior sample; discard samples inconsistent with e", "N(x, e) / N(e)",
                   "wastes samples when P(e) is small"],
                  ["Likelihood weighting", "fix evidence; sample the rest; weight w = Π P(eᵢ | parents)",
                   "Σ w over samples with X=x / Σ w", "consistent; degrades with downstream evidence"],
                  ["Gibbs (MCMC)", "start anywhere; repeatedly resample one non-evidence variable from "
                                   "P(Xᵢ | mb(Xᵢ))", "fraction of states visited", "converges to the posterior "
                                                                                   "(stationary distribution)"]],
                 widths=[70, 175, 115, 130], align="LEFT"))
    s.append(Spacer(1, 4))
    s.append(P("Gibbs conditional: P(xᵢ | mb(Xᵢ)) = α P(xᵢ | parents(Xᵢ)) Π<sub>Y ∈ children(Xᵢ)</sub> "
               "P(y | parents(Y)). Inverse-CDF rule for a Boolean variable: X = T iff u &lt; P(X = T | parents)."))
    pos = {"Cl": (0.5, 1), "Sp": (0.1, 0.5), "Ra": (0.9, 0.5), "We": (0.5, 0)}
    s.append(KeepTogether([H("Worked example — enumeration on the sprinkler network", "h3"),
                           graph_drawing(pos, [("Cl", "Sp", None), ("Cl", "Ra", None), ("Sp", "We", None),
                                               ("Ra", "We", None)], directed=True, width=260, height=130,
                                         fills={"Ra": QUERY_FILL, "We": EVID_FILL}),
                           P("With P(c)=0.5, P(s|c)=0.1, P(s|¬c)=0.5, P(r|c)=0.8, P(r|¬c)=0.2, P(w|s,r)=0.99, "
                             "P(w|s,¬r)=0.90, P(w|¬s,r)=0.90, P(w|¬s,¬r)=0: P(r, w) = Σ<sub>c,s</sub> P(c)P(s|c)P(r|c)P(w|s,r) "
                             "= 0.4581 and P(w) = 0.6471, so P(r | w) = 0.4581 / 0.6471 ≈ 0.708.")]))
    return s
