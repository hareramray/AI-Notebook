"""Self-test for topic modules.

    python selftest.py topics.regression            # stress-test every template (300 seeds each)
    python selftest.py topics.regression --pdf      # + preview PDF build/preview_<module>.pdf

Checks: every template runs for many seeds, returns the declared qtype/marks,
passes Q.validate(), and ReportLab can lay the text out (catches bad markup).
"""
import importlib
import os
import sys
import traceback

import numpy as np
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate

import core
from core import Figure, generate

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    mod = sys.argv[1]
    want_pdf = "--pdf" in sys.argv
    n_seeds = 300
    importlib.import_module(mod)
    temps = [t for t in core.REGISTRY if t.name.startswith(mod + ".")]
    print(f"{len(temps)} templates in {mod}")
    from render import S, question_flowables, solution_flowables
    bad = 0
    for t in temps:
        try:
            for s in range(n_seeds):
                q = generate(t, np.random.default_rng(10_000 + s))
                # markup check (no figures, they are slow): lay out paragraphs
                txt = [q.text] + q.options + [b for b in (q.solution if isinstance(q.solution, list) else [q.solution])
                                               if isinstance(b, str)] + [b for b in q.blocks if isinstance(b, str)]
                if s < 40:
                    for x in txt:
                        Paragraph(x, S["body"]).wrap(16 * cm, 30 * cm)
        except Exception:
            bad += 1
            print(f"FAIL {t.name} seed={10_000 + s}")
            traceback.print_exc()
    from collections import Counter
    print("by (marks,qtype):", dict(Counter((t.marks, t.qtype) for t in temps)))
    print("by subtopic:", dict(Counter(t.subtopic for t in temps)))
    print("figures used by", sum(1 for t in temps if any(isinstance(b, Figure) for b in
                                                           generate(t, np.random.default_rng(1)).blocks)), "templates")
    if want_pdf:
        os.makedirs("build", exist_ok=True)
        out = f"build/preview_{mod.split('.')[-1]}.pdf"
        doc = SimpleDocTemplate(out, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=1.8 * cm,
                                bottomMargin=1.8 * cm)
        story = []
        for i, t in enumerate(temps, 1):
            q = generate(t, np.random.default_rng(i))
            story += question_flowables(i, q, show_topic=True)
            story += solution_flowables(i, q)
            story.append(Paragraph("<font color='#999999'>" + t.name + "</font>", S["small"]))
        doc.build(story)
        print("preview:", out)
    print("FAILURES:", bad)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
