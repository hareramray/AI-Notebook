"""Core data model and helpers for the GATE DA Machine Learning mock-exam generator.

Every question is produced by a *template*: a function ``gen(rng) -> Q`` that is
registered with the ``@template(...)`` decorator.  Templates draw random
parameters from ``rng`` (a ``numpy.random.Generator``) so each mock set gets a
fresh instance, and they compute the answer in code so that the key is correct
by construction.

Text markup
-----------
Question text, options and solutions use ReportLab's paragraph mini-HTML:
``<b>``, ``<i>``, ``<sub>``, ``<super>``, ``<br/>``, ``<font face="Mono">``.
The characters ``&``, ``<`` and ``>`` must be escaped (``&amp;``, ``&lt;``,
``&gt;``) or, better, replaced by Unicode (≤, ≥, ≠, ×, ·, −, θ, λ, Σ, √, ∈ ...).

Blocks
------
``Q.blocks`` and ``Q.solution`` are lists whose items are one of
  * ``str``                              -> a paragraph
  * ``Table(rows, header=True)``         -> a data table (rows: list of lists of str)
  * ``Matrix(name, M, fmt_digits=2)``    -> a bracketed matrix shown as ``name = [..]``
  * ``Figure(draw, width_cm=9, height_cm=6)`` -> ``draw(fig)`` draws on a matplotlib Figure
  * ``Code(text)``                       -> monospaced pseudo-code / Python
A plain ``str`` is also accepted for ``Q.solution``.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from typing import Any, Callable, List, Optional, Sequence, Union

import numpy as np


# ----------------------------------------------------------------------------
# Blocks
# ----------------------------------------------------------------------------
@dataclass
class Table:
    rows: List[List[str]]
    header: bool = True
    col_widths_cm: Optional[List[float]] = None


@dataclass
class Matrix:
    name: str
    M: Any
    digits: int = 2


@dataclass
class Figure:
    draw: Callable[[Any], None]  # draw(fig: matplotlib.figure.Figure)
    width_cm: float = 9.0
    height_cm: float = 6.0
    caption: str = ""


@dataclass
class Code:
    text: str


Block = Union[str, Table, Matrix, Figure, Code]


# ----------------------------------------------------------------------------
# Question
# ----------------------------------------------------------------------------
@dataclass
class Q:
    text: str                       # main stem (markup)
    qtype: str                      # "MCQ" | "MSQ" | "NAT"
    marks: int                      # 1 or 2
    answer: Any                     # MCQ: int index; MSQ: sorted list of int; NAT: (lo, hi)
    solution: Union[str, List[Block]]
    options: List[str] = field(default_factory=list)  # 4 options for MCQ / MSQ
    blocks: List[Block] = field(default_factory=list)  # extra blocks after the stem
    nat_hint: str = ""             # e.g. "rounded off to two decimal places"
    topic: str = ""               # filled by the registry
    subtopic: str = ""

    def validate(self) -> None:
        assert self.qtype in ("MCQ", "MSQ", "NAT"), self.qtype
        assert self.marks in (1, 2), self.marks
        if self.qtype == "MCQ":
            assert len(self.options) == 4, "MCQ needs 4 options"
            assert isinstance(self.answer, (int, np.integer)) and 0 <= self.answer < 4
            assert len(set(self.options)) == 4, f"duplicate options: {self.options}"
        elif self.qtype == "MSQ":
            assert len(self.options) == 4, "MSQ needs 4 options"
            assert isinstance(self.answer, (list, tuple)) and len(self.answer) >= 1
            assert all(0 <= a < 4 for a in self.answer)
            assert len(set(self.options)) == 4, f"duplicate options: {self.options}"
        else:
            lo, hi = self.answer
            assert lo <= hi, (lo, hi)
            assert np.isfinite(lo) and np.isfinite(hi)


# ----------------------------------------------------------------------------
# Registry
# ----------------------------------------------------------------------------
@dataclass
class Template:
    name: str
    topic: str
    subtopic: str
    marks: int
    qtype: str
    fn: Callable[[np.random.Generator], Q]


REGISTRY: List[Template] = []


def template(topic: str, subtopic: str, marks: int, qtype: str):
    """Register a question generator.  ``qtype``/``marks`` must match what ``fn`` returns."""

    def deco(fn):
        REGISTRY.append(Template(fn.__module__ + "." + fn.__name__, topic, subtopic, marks, qtype, fn))
        return fn

    return deco


def generate(t: Template, rng: np.random.Generator) -> Q:
    q = t.fn(rng)
    q.topic = q.topic or t.topic
    q.subtopic = q.subtopic or t.subtopic
    assert q.marks == t.marks and q.qtype == t.qtype, (t.name, q.marks, q.qtype)
    if q.qtype == "MSQ":
        q.answer = sorted(int(a) for a in q.answer)
    q.validate()
    return q


# ----------------------------------------------------------------------------
# Formatting helpers
# ----------------------------------------------------------------------------
def fmt(x: float, d: int = 2) -> str:
    """Format a number with at most ``d`` decimals, dropping trailing zeros; uses a real minus sign."""
    if isinstance(x, Fraction):
        x = float(x)
    if abs(x) < 0.5 * 10 ** (-d):
        x = 0.0
    s = f"{x:.{d}f}"
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    if s == "-0":
        s = "0"
    return s.replace("-", "−")


def frac(fr: Fraction) -> str:
    fr = Fraction(fr)
    if fr.denominator == 1:
        return fmt(fr.numerator, 0)
    return f"{fr.numerator}/{fr.denominator}".replace("-", "−")


def vec(v: Sequence[float], d: int = 2) -> str:
    return "(" + ", ".join(fmt(x, d) for x in v) + ")"


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def nat_range(value: float, d: int = 2, tol: Optional[float] = None):
    """Answer range for a NAT question whose answer is to be rounded to ``d`` decimals."""
    if tol is None:
        tol = 10 ** (-d)
    return (round(value - tol, d + 2), round(value + tol, d + 2))


def nat_hint(d: int) -> str:
    if d == 0:
        return "(Answer in integer)"
    word = {1: "one", 2: "two", 3: "three"}.get(d, str(d))
    return f"(rounded off to {word} decimal place{'s' if d > 1 else ''})"


# ----------------------------------------------------------------------------
# Option builders
# ----------------------------------------------------------------------------
def mcq(rng: np.random.Generator, correct: str, distractors: Sequence[str]):
    """Return (options, answer_index) with the correct option placed randomly.

    ``distractors`` may contain more than 3 items; 3 distinct ones different
    from ``correct`` are picked.
    """
    pool = []
    for d in distractors:
        if d != correct and d not in pool:
            pool.append(d)
    if len(pool) < 3:
        raise ValueError(f"need 3 distinct distractors, got {pool} for {correct}")
    idx = rng.choice(len(pool), 3, replace=False)
    opts = [pool[i] for i in idx] + [correct]
    perm = rng.permutation(4)
    opts = [opts[i] for i in perm]
    return opts, int(opts.index(correct))


def mcq_numeric(rng: np.random.Generator, value: float, d: int = 2, distractor_values: Sequence[float] = (),
                unit: str = ""):
    """MCQ with numeric options.  Distractors that collide with the answer after formatting are dropped
    and replaced by perturbations of the correct value."""
    c = fmt(value, d) + unit
    ds = [fmt(v, d) + unit for v in distractor_values]
    k = 1
    while len(set(x for x in ds if x != c)) < 3:
        delta = (abs(value) if value != 0 else 1) * 0.25 * k
        ds.append(fmt(value + delta * (1 if k % 2 else -1), d) + unit)
        k += 1
    return mcq(rng, c, ds)


def msq_from_statements(rng: np.random.Generator, true_stmts: Sequence, false_stmts: Sequence,
                        n_true: Optional[int] = None):
    """Build an MSQ from statement pools.

    Each pool item is either a string or a tuple ``(statement, explanation)``.
    Returns ``(options, answer_indices, explanation_lines)`` where explanation_lines
    is a list of strings like "(A) TRUE – explanation".
    """
    if n_true is None:
        n_true = int(rng.integers(1, 5))  # 1..4 correct options
    n_true = max(1, min(n_true, len(true_stmts), 4))
    n_false = 4 - n_true
    if n_false > len(false_stmts):
        n_false = len(false_stmts)
        n_true = 4 - n_false
    ti = rng.choice(len(true_stmts), n_true, replace=False)
    fi = rng.choice(len(false_stmts), n_false, replace=False) if n_false else []
    items = [(true_stmts[i], True) for i in ti] + [(false_stmts[i], False) for i in fi]
    perm = rng.permutation(4)
    items = [items[i] for i in perm]
    opts, ans, expl = [], [], []
    for j, (s, ok) in enumerate(items):
        st, ex = (s if isinstance(s, tuple) else (s, ""))
        opts.append(st)
        if ok:
            ans.append(j)
        tag = "TRUE" if ok else "FALSE"
        expl.append(f"<b>({'ABCD'[j]}) {tag}.</b> {ex}".rstrip())
    return opts, ans, expl


LETTERS = "ABCD"
