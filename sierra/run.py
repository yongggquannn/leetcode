"""
Run practice tests (stdlib only, no pytest needed).

    python sierra/run.py 1          # your code for problem 1
    python sierra/run.py 1 -v       # with tracebacks
    python sierra/run.py all --ref  # reference solutions
"""
import argparse
import importlib
import os
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))


def run_module(path: Path, verbose: bool) -> tuple[int, int]:
    mod = importlib.import_module(path.stem)
    tests = [(n, f) for n, f in vars(mod).items() if n.startswith("test_") and callable(f)]
    passed = 0
    print(f"\n== {path.stem} ==")
    for name, fn in tests:
        detail = ""
        try:
            fn()
            status = "PASS"
            passed += 1
        except NotImplementedError:
            status = "TODO"
        except AssertionError as err:
            status, detail = "FAIL", str(err)
        except Exception as err:  # noqa: BLE001 - report any crash as a test error
            status, detail = "ERROR", f"{type(err).__name__}: {err}"
        print(f"  {status:5} {name}" + (f"  -> {detail}" if detail else ""))
        if verbose and status in ("FAIL", "ERROR"):
            traceback.print_exc()
    return passed, len(tests)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("problem", help="problem number (e.g. 3) or 'all'")
    parser.add_argument("--ref", action="store_true", help="run against solutions/")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()
    if args.ref:
        os.environ["SIERRA_REF"] = "1"

    files = sorted((ROOT / "tests").glob("test_problem_*.py"), key=lambda p: int(p.stem.split("_")[2]))
    if args.problem != "all":
        files = [f for f in files if f.stem.split("_")[2] == args.problem]
    if not files:
        sys.exit(f"no tests for problem {args.problem}")

    total_pass = total = 0
    for f in files:
        p, n = run_module(f, args.verbose)
        total_pass += p
        total += n
    print(f"\n{total_pass}/{total} passed")
    sys.exit(0 if total_pass == total else 1)


if __name__ == "__main__":
    main()
