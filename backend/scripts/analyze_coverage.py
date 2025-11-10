#!/usr/bin/env python3
"""Analyze test coverage and identify gaps."""
import sys
from pathlib import Path

import coverage


def analyze_coverage(min_coverage: float = 99.0) -> int:
    """Analyze coverage and return exit code."""
    # Load coverage data
    cov = coverage.Coverage()

    try:
        cov.load()
    except Exception as e:
        print(f"Error loading coverage data: {e}")
        return 1

    # Generate report
    total = cov.report(show_missing=True)

    print("\n" + "=" * 80)
    print(f"COVERAGE SUMMARY: {total:.2f}%")
    print("=" * 80)

    if total < min_coverage:
        print(f"\n⚠️  WARNING: Coverage {total:.2f}% is below target {min_coverage}%")
        print(f"Gap: {min_coverage - total:.2f}%")

        # Get missing files
        analysis = cov.analysis2("")
        if analysis:
            print("\nFiles with missing coverage:")
            for filename, statements, missing, _ in analysis:
                if missing:
                    coverage_pct = (
                        (len(statements) - len(missing)) / len(statements) * 100
                    )
                    print(f"  {filename}: {coverage_pct:.2f}% (missing: {len(missing)} lines)")

        return 1

    print(f"\n✅ SUCCESS: Coverage {total:.2f}% meets target {min_coverage}%")
    return 0


if __name__ == "__main__":
    target = float(sys.argv[1]) if len(sys.argv) > 1 else 99.0
    sys.exit(analyze_coverage(target))
