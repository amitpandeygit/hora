"""CLI: ``python -m hora.benchmark tests/benchmark/fixtures/*.json``."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from hora.benchmark.runner import (
    compare_fixture,
    compare_variants,
    format_report,
    format_variant_report,
    load_fixture,
    summarise,
)


def main() -> int:
    ap = argparse.ArgumentParser(description="Diff the engine against recorded Jagannatha Hora output")
    ap.add_argument("fixtures", nargs="+", type=Path)
    ap.add_argument("--tolerance", type=float, default=1.0, help="arcseconds")
    ap.add_argument("--strict", action="store_true", help="treat unverified slots as failures")
    ap.add_argument("--variants", action="store_true",
                    help="run each fixture under every declared settings variant and "
                         "print them side by side instead of picking one")
    args = ap.parse_args()

    total = {"match": 0, "mismatch": 0, "unverified": 0}
    for path in args.fixtures:
        fixture = load_fixture(path)
        if args.variants:
            results = compare_variants(fixture, args.tolerance)
            print(format_variant_report(fixture, results))
            print()
            continue
        comparisons = compare_fixture(fixture, args.tolerance)
        print(format_report(fixture, comparisons))
        print()
        for k, v in summarise(comparisons).items():
            total[k] += v

    if args.variants:
        return 0
    print(f"TOTAL: {total['match']} match, {total['mismatch']} mismatch, {total['unverified']} unverified")
    if total["mismatch"]:
        return 1
    if args.strict and total["unverified"]:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
