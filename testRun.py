#!/usr/bin/env python3
import subprocess
import sys
import time
from pathlib import Path

BIN = Path(".csse6400/bin").resolve()
USE = sys.stdout.isatty()
S = {"b": "1", "d": "2", "r": "31", "g": "32", "y": "33", "u": "34", "c": "36"}


def col(text, key):
    return f"\033[{S[key]}m{text}\033[0m" if USE else text


def hr():
    print(col("-" * 64, "d"))


def run(p: Path) -> int:
    proc = subprocess.Popen(
        ["bash", str(p)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    for line in proc.stdout or []:
        print(line, end="")
    return proc.wait()


def main() -> int:
    if not BIN.is_dir():
        print(f"{col('Error:', 'r')} folder not found: {BIN}")
        return 1

    files = sorted(p for p in BIN.iterdir() if p.is_file() and p.suffix == ".sh")
    if not files:
        print(f"{col('No .sh files found in', 'y')} {BIN}")
        return 1

    passed, failed = 0, []
    t_all = time.time()

    hr()
    print(f"{col(col('BASH RUNNER', 'c'), 'b')} {col(time.strftime('%H:%M:%S'), 'd')}")
    print(f"{col('Directory:', 'b')} {BIN}")
    print(f"{col('Files found:', 'b')} {len(files)}")
    print(f"{col('Mode:', 'b')} verbose")
    hr()

    for i, f in enumerate(files, 1):
        print(
            f"{col(f'[{i}/{len(files)}]', 'd')} {col('▶ Running', 'u')} {col(f.name, 'b')}"
        )
        print(f"{col('Command:', 'd')} bash {f}")
        t = time.time()
        try:
            rc = run(f)
        except Exception as e:
            rc = 1
            print(col(f"Runner error: {e}", "r"))

        dt = time.time() - t
        if rc == 0:
            passed += 1
            print(f"{col('✔ PASS', 'g')} {f.name} {col(f'({dt:.2f}s)', 'd')}")
        else:
            failed.append((f.name, rc))
            print(
                f"{col('✘ FAIL', 'r')} {f.name} {col(f'(exit {rc}, {dt:.2f}s)', 'd')}"
            )
        hr()

    names = ", ".join(n for n, _ in failed) if failed else "none"
    print(col(col("SUMMARY", "c"), "b"))
    print(f"  {col('Ran:', 'b')}    {len(files)}")
    print(f"  {col(col('Pass:', 'b'), 'g')}   {col(str(passed), 'g')}")
    print(
        f"  {col(col('Fail:', 'b'), 'r')}   {col(str(len(failed)), 'r')} {col(f'({names})', 'd')}"
    )
    print(f"  {col('Time:', 'b')}   {time.time() - t_all:.2f}s")
    hr()

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
