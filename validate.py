"""
For measuring the engine against the labelled cases.
"""

from lab_engine import build_result
from validation_cases import CASES

def run():
    level_ok = 0
    pat_total = pat_found = 0
    mismatches = []

    for case in CASES:
        r = build_result(case["panel"])
        got_level = r["conclusion"]["level"]
        got_patterns = {p[0] for p in r["patterns"]}

        if got_level == case["expect_level"]:
            level_ok += 1
        else:
            mismatches.append(f"[{case['name']}] level: expected {case['expect_level']}, got {got_level}")

        for want in case["expect_patterns"]:
            pat_total += 1
            if want in got_patterns:
                pat_found += 1
            else:
                mismatches.append(f"[{case['name']}] missing pattern: {want}")

    n = len(CASES)
    print("=" * 56)
    print("  VALIDATION REPORT")
    print("=" * 56)
    print(f"  Cases                : {n}")
    print(f"  Conclusion-level acc : {level_ok}/{n}  ({level_ok/n:.0%})")
    if pat_total:
        print(f"  Pattern recall       : {pat_found}/{pat_total}  ({pat_found/pat_total:.0%})")
    if mismatches:
        print("\n  Mismatches:")
        for m in mismatches:
            print("   -", m)
    else:
        print("\n  No mismatches — engine matches all expected labels. ✓")
    print("=" * 56)
    return level_ok == n and pat_found == pat_total


if __name__ == "__main__":
    ok = run()
    raise SystemExit(0 if ok else 1)


