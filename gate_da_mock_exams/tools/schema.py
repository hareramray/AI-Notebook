"""Loading + validation of mock-test set files (sets/set_XX.py, each defining SET = {...})."""
import contextlib
import importlib.util
import io
import re
import signal
import sys
import traceback

LETTERS = "ABCD"
QTYPES = ("MCQ", "MSQ", "NAT")


def load_set(path):
    spec = importlib.util.spec_from_file_location("set_mod_%d" % abs(hash(path)), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.SET


class _Timeout(Exception):
    pass


def _alarm(signum, frame):
    raise _Timeout()


def run_snippet(code, verify, answer, timeout=10):
    """Run question code (capturing stdout as OUTPUT) then verify code. Returns error str or None."""
    ns = {"__name__": "__main__"}
    buf = io.StringIO()
    old = signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(timeout)
    try:
        if code:
            with contextlib.redirect_stdout(buf):
                exec(compile(code, "<question code>", "exec"), ns)
        ns["OUTPUT"] = buf.getvalue()
        ns["ANSWER"] = answer
        if verify:
            with contextlib.redirect_stdout(io.StringIO()):
                exec(compile(verify, "<verify>", "exec"), ns)
        return None
    except _Timeout:
        return "timed out"
    except AssertionError as e:
        return "verify assertion failed: %s\n--- program output ---\n%s" % (e, buf.getvalue()[:600])
    except Exception:
        return traceback.format_exc(limit=3)
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old)


def validate_set(S, run=True, path=""):
    errs, warns = [], []
    stats = {"verified": 0, "MCQ": 0, "MSQ": 0, "NAT": 0, "diagrams": 0}
    for key in ("number", "title", "questions"):
        if key not in S:
            errs.append("SET missing key %r" % key)
    qs = S.get("questions", [])
    if len(qs) != 20:
        errs.append("expected 20 questions, found %d" % len(qs))
    from diagrams import render
    for i, q in enumerate(qs, 1):
        tag = "Q%d" % i
        t = q.get("type")
        if t not in QTYPES:
            errs.append("%s: bad type %r" % (tag, t))
            continue
        stats[t] += 1
        exp_marks = 1 if i <= 10 else 2
        if q.get("marks") != exp_marks:
            errs.append("%s: marks must be %d (Q1-10 = 1 mark, Q11-20 = 2 marks)" % (tag, exp_marks))
        for k in ("topic", "text", "solution", "answer"):
            if not q.get(k):
                errs.append("%s: missing %r" % (tag, k))
        ans = q.get("answer")
        if t in ("MCQ", "MSQ"):
            opts = q.get("options", [])
            if len(opts) != 4:
                errs.append("%s: needs exactly 4 options" % tag)
            if t == "MCQ" and not (isinstance(ans, str) and ans in LETTERS):
                errs.append("%s: MCQ answer must be one of 'A'..'D'" % tag)
            if t == "MSQ":
                if not (isinstance(ans, (list, tuple)) and ans and all(a in LETTERS for a in ans)
                        and len(set(ans)) == len(ans)):
                    errs.append("%s: MSQ answer must be a non-empty list of distinct letters" % tag)
        else:
            if q.get("options"):
                errs.append("%s: NAT must not have options" % tag)
            ok = False
            if isinstance(ans, (int, float)):
                ok = True
            elif isinstance(ans, str):
                ok = re.fullmatch(r"-?\d+(\.\d+)?", ans.strip()) is not None
            elif isinstance(ans, (list, tuple)) and len(ans) == 2:
                try:
                    ok = float(ans[0]) <= float(ans[1])
                except Exception:
                    ok = False
            if not ok:
                errs.append("%s: NAT answer must be a number, numeric string, or [low, high]" % tag)
        for fld in ("code", "solution_code"):
            c = q.get(fld)
            if c:
                for ln, line in enumerate(c.splitlines(), 1):
                    if len(line) > 78:
                        warns.append("%s: %s line %d is %d chars (>78, will wrap)" % (tag, fld, ln, len(line)))
        for fld in ("diagrams", "solution_diagrams"):
            for dg in q.get(fld, []) or []:
                stats["diagrams"] += 1
                try:
                    render(dg)
                except Exception as e:
                    errs.append("%s: %s render error: %r" % (tag, fld, e))
        if run:
            code = q.get("code") if q.get("run_code", True) else None
            verify = q.get("verify")
            if verify or code:
                if code and not verify and q.get("run_code") is None:
                    # still make sure displayed code at least runs
                    pass
                err = run_snippet(code, verify, ans)
                if err:
                    errs.append("%s: execution error:\n%s" % (tag, err))
                elif verify:
                    stats["verified"] += 1
    if stats["MCQ"] < 6 or stats["MSQ"] < 3 or stats["NAT"] < 4:
        warns.append("type mix MCQ=%d MSQ=%d NAT=%d (aim ~8/5/7)" % (stats["MCQ"], stats["MSQ"], stats["NAT"]))
    return errs, warns, stats
