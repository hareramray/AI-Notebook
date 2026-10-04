"""Validate one or more set files and (optionally) render a preview PDF.

usage: python3 tools/validate.py sets/set_07.py [sets/set_08.py ...] [--pdf PREVIEW.pdf] [--no-run]
Exit code 1 if any errors.
"""
import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from schema import load_set, validate_set  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("files", nargs="+")
ap.add_argument("--pdf")
ap.add_argument("--no-run", action="store_true")
a = ap.parse_args()

import build  # noqa: E402  (registers fonts used by diagram rendering)

bad = False
for f in a.files:
    try:
        S = load_set(f)
    except Exception as e:
        print("%s: FAILED TO IMPORT: %r" % (f, e))
        bad = True
        continue
    errs, warns, stats = validate_set(S, run=not a.no_run, path=f)
    print("== %s  (set %s: %s)" % (f, S.get("number"), S.get("title")))
    print("   stats:", stats)
    for w in warns:
        print("   WARN ", w)
    for e in errs:
        print("   ERROR", e)
    if errs:
        bad = True
if a.pdf and not bad:
    build.build(a.files, a.pdf, front=False)
    print("preview written to", a.pdf)
sys.exit(1 if bad else 0)
