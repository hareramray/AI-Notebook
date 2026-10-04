"""Build the GATE DA (Section 7: AI) mock-test book: 100 full sets with keys and worked solutions."""
import importlib
import os
import random
import sys
import traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "banks"))

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak,
                                KeepTogether, Table, TableStyle, CondPageBreak, Flowable)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.graphics.shapes import Drawing

from common import Q, ST, tbl, num, ACCENT, BLUE
import gen_search as S
import gen_games as GM
import gen_logic as L
import gen_bn as BN
import notes

N_SETS = int(os.environ.get("N_SETS", "100"))
OUT = os.environ.get("OUT", os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                         "GATE_DA_AI_Mock_Tests_100_Sets.pdf"))
N_ONE, N_TWO = 10, 15

# Generator groups: each set draws one generator from every group.
GROUPS = [
    [S.q_bfs_order, S.q_dfs_order],
    [S.q_counting, GM.q_ab_bestcase, S.q_greedy],
    [S.q_ucs, S.q_astar],
    [S.q_astar, S.q_heuristic_props],
    [GM.q_minimax],
    [GM.q_alphabeta, GM.q_expectimax, GM.q_alphabeta],
    [L.q_model_count],
    [L.q_tautology, L.q_equivalence],
    [L.q_entailment, L.q_resolution],
    [L.q_forward_chaining, L.q_count_relations, L.q_count_unary],
    [L.q_fol_structure],
    [BN.q_bn_inference],
    [BN.q_dsep],
    [BN.q_ve],
    [BN.q_markov_blanket, BN.q_param_count, BN.q_bn_marginal],
    [BN.q_prior_prob, BN.q_uniform_sample],
    [BN.q_rejection, BN.q_likelihood_weighting, BN.q_gibbs],
]

TOPIC_ORDER = ["Uninformed Search", "Informed Search", "Adversarial Search", "Local Search", "Problem Formulation",
               "Propositional Logic", "Predicate Logic", "Probability for AI", "Conditional Independence",
               "Bayesian Networks", "Exact Inference", "Variable Elimination", "Sampling"]


def area(topic):
    if "Search" in topic or topic in ("Problem Formulation",):
        return "Search"
    if "Logic" in topic:
        return "Logic"
    return "Uncertainty"


def load_banks():
    out = []
    for mod in ("bank_search", "bank_logic", "bank_uncertainty"):
        try:
            m = importlib.import_module(mod)
        except Exception as e:  # noqa
            print("bank missing:", mod, e)
            continue
        for d in m.BANK:
            t = d["type"]
            if t == "NAT":
                a = d["answer"]
                ans = (a["lo"], a["hi"])
                opts = None
            else:
                ans = list(d["answer"])
                opts = list(d["options"])
            out.append(Q(d["topic"], t, int(d["marks"]), d["q"], opts, ans, [d["solution"]], [], "Concept"))
    return out


class BankPicker:
    def __init__(self, bank, rng):
        self.rng = rng
        self.pools = {}
        for q in bank:
            self.pools.setdefault((q.marks, area(q.topic)), []).append(q)
        self.queues = {k: [] for k in self.pools}

    def take(self, marks, ar, exclude):
        keys = [(marks, ar)] + [(marks, a) for a in ("Search", "Logic", "Uncertainty") if a != ar]
        for k in keys:
            if k not in self.pools:
                continue
            for _ in range(2):
                if not self.queues[k]:
                    self.queues[k] = self.pools[k][:]
                    self.rng.shuffle(self.queues[k])
                while self.queues[k]:
                    q = self.queues[k].pop()
                    if id(q) not in exclude:
                        return q
        return None


def gen_safe(fn, rng):
    for _ in range(25):
        try:
            return fn(random.Random(rng.random()))
        except Exception:
            continue
    raise RuntimeError(f"generator {fn.__name__} failed repeatedly")


def make_set(idx, picker):
    rng = random.Random(7919 * idx + 17)
    qs = []
    for grp in GROUPS:
        qs.append(gen_safe(rng.choice(grp), rng))
    ones = [q for q in qs if q.marks == 1]
    twos = [q for q in qs if q.marks == 2]
    rng.shuffle(ones)
    rng.shuffle(twos)
    ones, twos = ones[:7], twos[:11]
    used = set()
    cnt = {"Search": 0, "Logic": 0, "Uncertainty": 0}
    for q in ones + twos:
        cnt[area(q.topic)] += 1

    def need():
        return min(cnt, key=lambda a: cnt[a] + rng.random() * 0.5)
    while len(ones) < N_ONE:
        a = need()
        q = picker.take(1, a, used)
        used.add(id(q))
        cnt[area(q.topic)] += 1
        ones.append(q)
    while len(twos) < N_TWO:
        a = need()
        q = picker.take(2, a, used)
        used.add(id(q))
        cnt[area(q.topic)] += 1
        twos.append(q)
    key = lambda q: (["Search", "Logic", "Uncertainty"].index(area(q.topic)), rng.random())
    ones.sort(key=key)
    twos.sort(key=key)
    return ones + twos


# ------------------------------------------------------------------------ rendering
class Bookmark(Flowable):
    def __init__(self, title, key, level=0):
        super().__init__()
        self.title, self.key, self.level = title, key, level
        self.width = self.height = 0

    def draw(self):
        c = self.canv
        c.bookmarkPage(self.key)
        c.addOutlineEntry(self.title, self.key, level=self.level, closed=self.level > 0)


class Doc(BaseDocTemplate):
    def __init__(self, fn, **kw):
        super().__init__(fn, pagesize=A4, leftMargin=16 * mm, rightMargin=16 * mm, topMargin=17 * mm,
                         bottomMargin=15 * mm, title="GATE DA – AI Section: 100 Mock Tests",
                         author="AI-Notebook", subject="GATE Data Science & AI, Section 7 (AI)", **kw)
        fr = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="f")
        self.addPageTemplates([PageTemplate("p", [fr], onPage=self.decor)])
        self.cur_set = ""

    def decor(self, c, doc):
        c.saveState()
        if doc.page > 1:
            c.setFont("DejaVu", 7.5)
            c.setFillColor(colors.HexColor("#6b7280"))
            c.drawString(16 * mm, A4[1] - 11 * mm, "GATE DA · Section 7: Artificial Intelligence · 100 Mock Tests")
            c.drawRightString(A4[0] - 16 * mm, A4[1] - 11 * mm, self.cur_set)
            c.setStrokeColor(colors.HexColor("#d1d5db"))
            c.line(16 * mm, A4[1] - 12.5 * mm, A4[0] - 16 * mm, A4[1] - 12.5 * mm)
            c.drawCentredString(A4[0] / 2, 8 * mm, f"— {doc.page} —")
        c.restoreState()

    def beforeDocument(self):
        self.cur_set = ""

    def afterFlowable(self, f):
        if isinstance(f, Paragraph) and getattr(f, "_toc", None):
            lvl, text = f._toc
            self.notify("TOCEntry", (lvl, text, self.page))
        if isinstance(f, SetMarker):
            self.cur_set = f.label


class SetMarker(Flowable):
    def __init__(self, label):
        super().__init__()
        self.label = label
        self.width = self.height = 0

    def draw(self):
        pass


def H(text, style, toc=None):
    p = Paragraph(text, ST[style])
    if toc is not None:
        p._toc = toc
    return p


def banner(text, sub):
    t = Table([[Paragraph(f"<font color='#fbbf24'><b>{text}</b></font>", ParagraphStyle_banner()),
                Paragraph(f"<font color='white'>{sub}</font>", ST["small"])]],
              colWidths=[95 * mm, 83 * mm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#6b1d1d")),
                           ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 8),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 8), ("LEFTPADDING", (0, 0), (-1, -1), 8)]))
    return t


_BS = None


def ParagraphStyle_banner():
    global _BS
    if _BS is None:
        from reportlab.lib.styles import ParagraphStyle
        _BS = ParagraphStyle("ban", fontName="DejaVu-Bold", fontSize=17, leading=21)
    return _BS


def qtag(q):
    neg = ""
    if q.qtype == "MCQ":
        neg = " · negative: −1/3" if q.marks == 1 else " · negative: −2/3"
    else:
        neg = " · no negative marking"
    return (f"<font color='#7f1d1d'><b>Q.{{n}}</b></font> &nbsp;<font size=7.5 color='#1a56db'>[{q.qtype} · "
            f"{q.marks} mark{'s' if q.marks > 1 else ''}{neg}]</font> &nbsp;<font size=7.5 color='#6b7280'>"
            f"{q.topic}{(' – ' + q.subtopic) if q.subtopic and q.subtopic != 'Concept' else ''}</font>")


def question_block(n, q):
    items = [Paragraph(qtag(q).replace("{n}", str(n)), ST["q"]), Spacer(1, 2),
             Paragraph(q.text, ST["q"])]
    for f in q.figures:
        items += [Spacer(1, 4), f]
    items.append(Spacer(1, 3))
    if q.qtype == "NAT":
        items.append(Paragraph("<font color='#6b7280'>Answer (numerical): ______________</font>", ST["opt"]))
    else:
        box = "☐" if q.qtype == "MSQ" else "○"
        for i, o in enumerate(q.options):
            items.append(Paragraph(f"{box} ({chr(65 + i)}) &nbsp;{o}", ST["opt"]))
    # questions with big figures may not fit on one page; keep header+text together at least
    return [KeepTogether(items), Spacer(1, 9)]


def key_str(q):
    if q.qtype == "NAT":
        lo, hi = q.answer
        return f"{num(lo, 4)}" if lo == hi else f"{num(lo, 4)} to {num(hi, 4)}"
    return ", ".join(chr(65 + i) for i in q.answer)


def solution_block(n, q):
    head = Paragraph(f"<font color='#7f1d1d'><b>Q.{n}</b></font> &nbsp;<font size=8 color='#1a56db'>[{q.qtype}, "
                     f"{q.marks}M · {q.topic}]</font> &nbsp;&nbsp;<b>Answer: {key_str(q)}</b>"
                     + (f" &nbsp;<font size=8 color='#6b7280'>(" + "; ".join(
                         f"{chr(65 + i)}: {q.options[i]}" for i in q.answer) + ")</font>"
                        if q.qtype != "NAT" and len("".join(q.options[i] for i in q.answer)) < 160 else ""),
                     ST["sol"])
    items = [head, Spacer(1, 2)]
    for s in q.solution:
        if isinstance(s, str):
            items.append(Paragraph(s, ST["sol"]))
        else:
            items.append(Spacer(1, 2))
            items.append(s)
            items.append(Spacer(1, 2))
    out = []
    if sum(1 for s in q.solution if not isinstance(s, str)) == 0 and len(q.solution) < 8:
        out.append(KeepTogether(items))
    else:
        out.append(KeepTogether(items[:3]))
        out += items[3:]
    out.append(Spacer(1, 7))
    return out


def set_story(idx, qs):
    story = [PageBreak(), SetMarker(f"Mock Test {idx:03d}"), Bookmark(f"Mock Test {idx:03d}", f"set{idx}")]
    story.append(H(f"Mock Test {idx:03d}", "h1", toc=(0, f"Mock Test {idx:03d}")))
    marks = sum(q.marks for q in qs)
    cnt = {}
    for q in qs:
        cnt[area(q.topic)] = cnt.get(area(q.topic), 0) + q.marks
    tcount = {}
    for q in qs:
        tcount[q.qtype] = tcount.get(q.qtype, 0) + 1
    info = [["Questions", "Total marks", "Time", "MCQ / MSQ / NAT", "Search / Logic / Uncertainty (marks)"],
            [str(len(qs)), str(marks), "75 minutes", f"{tcount.get('MCQ', 0)} / {tcount.get('MSQ', 0)} / "
                                                      f"{tcount.get('NAT', 0)}",
             f"{cnt.get('Search', 0)} / {cnt.get('Logic', 0)} / {cnt.get('Uncertainty', 0)}"]]
    story.append(tbl(info, widths=[60, 60, 65, 95, 180]))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Q.1 – Q.10 carry 1 mark each; Q.11 – Q.25 carry 2 marks each. MCQ: one correct option, "
                           "wrong answer −1/3 (1-mark) or −2/3 (2-mark). MSQ: one or more correct options, full "
                           "credit only if exactly all correct options are chosen, no negative marking. NAT: enter a "
                           "number, no negative marking. Unless stated otherwise, ties are broken alphabetically and "
                           "all random variables are Boolean.", ST["small"]))
    story.append(Spacer(1, 6))
    story.append(H("Section A — 1-mark questions", "h3"))
    for i, q in enumerate(qs, 1):
        if i == N_ONE + 1:
            story.append(H("Section B — 2-mark questions", "h3"))
        story += question_block(i, q)
    # answer key
    story.append(CondPageBreak(90 * mm))
    story.append(H(f"Answer Key — Mock Test {idx:03d}", "h2", toc=None))
    rows = [["Q", "Type", "Marks", "Topic", "Key"] * 2]
    half = (len(qs) + 1) // 2
    for i in range(half):
        r = []
        for j in (i, i + half):
            if j < len(qs):
                q = qs[j]
                r += [str(j + 1), q.qtype, str(q.marks), q.topic, f"<b>{key_str(q)}</b>"]
            else:
                r += [""] * 5
        rows.append(r)
    story.append(tbl(rows, widths=[20, 30, 30, 92, 70] * 2))
    story.append(Spacer(1, 8))
    story.append(H("Detailed Solutions", "h2"))
    for i, q in enumerate(qs, 1):
        story += solution_block(i, q)
    return story


def cover():
    st = []
    st.append(Spacer(1, 30 * mm))
    st.append(banner("GATE DA · Section 7 · AI", "Data Science and Artificial Intelligence"))
    st.append(Spacer(1, 14 * mm))
    st.append(Paragraph("<b>100 Full-Length Mock Tests</b>", ST["h1"]))
    st.append(Paragraph("Artificial Intelligence: Search · Logic · Reasoning under Uncertainty", ST["h2"]))
    st.append(Spacer(1, 6 * mm))
    st.append(Paragraph(
        "Every set follows the GATE DA question pattern: <b>25 questions, 40 marks</b> (10 × 1-mark + 15 × 2-mark), "
        "with Multiple-Choice (MCQ), Multiple-Select (MSQ) and Numerical-Answer (NAT) questions and GATE negative "
        "marking. Each set ends with an answer key and <b>step-by-step worked solutions</b>: full search traces, "
        "annotated game trees, truth tables, resolution derivations, enumeration tables, variable-elimination "
        "factor tables and sampling computations.", ST["body"]))
    st.append(Spacer(1, 5 * mm))
    rows = [["Syllabus unit (GATE DA 2027, Section 7)", "Covered by"],
            ["Search — uninformed", "BFS / DFS traces, UCS, IDS / DLS / BFS node counts, concept questions"],
            ["Search — informed", "A*, greedy best-first, admissibility & consistency, effective branching factor"],
            ["Search — adversarial", "Minimax, alpha–beta pruning (leaf counting), expectimax, move ordering"],
            ["Logic — propositional", "Model counting, validity, equivalence, entailment, resolution, forward chaining"],
            ["Logic — predicate", "Finite-model semantics, quantifier order, counting interpretations, unification"],
            ["Conditional independence representation", "Bayesian networks, d-separation, Markov blanket, parameters"],
            ["Exact inference — variable elimination", "Enumeration, factor scopes and sizes, elimination orderings"],
            ["Approximate inference — sampling", "Prior, rejection, likelihood weighting, Gibbs sampling"]]
    st.append(tbl(rows, widths=[200, 290], align="LEFT"))
    st.append(Spacer(1, 8 * mm))
    st.append(Paragraph("Diagrams (graphs, game trees, Bayesian networks, relation graphs) are drawn as vector "
                        "graphics. All numerical questions were generated and solved by exact computation, so "
                        "the answer keys are reproducible.", ST["small"]))
    return st


def build():
    bank = load_banks()
    print("bank questions:", len(bank))
    picker = BankPicker(bank, random.Random(42))
    doc = Doc(OUT)
    story = cover()
    story.append(PageBreak())
    story.append(H("Contents", "h1"))
    toc = TableOfContents()
    from reportlab.lib.styles import ParagraphStyle
    toc.levelStyles = [ParagraphStyle("t0", fontName="DejaVu", fontSize=8.6, leading=10.6, leftIndent=6),
                       ParagraphStyle("t1", fontName="DejaVu", fontSize=7.5, leading=9, leftIndent=24,
                                      textColor=colors.HexColor("#6b7280"))]
    story.append(toc)
    story.append(PageBreak())
    story.append(SetMarker("How to use this book"))
    story += notes.story(H)
    for i in range(1, N_SETS + 1):
        qs = make_set(i, picker)
        story += set_story(i, qs)
        if i % 10 == 0:
            print("set", i)
    doc.multiBuild(story)
    print("written", OUT)


if __name__ == "__main__":
    build()
