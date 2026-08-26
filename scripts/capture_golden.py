#!/usr/bin/env python3
"""Record the current response of every endpoint in tests/golden/cases.py.

Run this ONLY when a change to the API contract is intended and approved. The
diff it produces is the record of what changed.

    python scripts/capture_golden.py            # write fixtures
    python scripts/capture_golden.py --check    # report drift, write nothing
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from fastapi.testclient import TestClient

from hora.api.main import app
from tests.golden.cases import CASES

OUT = ROOT / "tests" / "golden" / "responses"


def record(client, method: str, path: str, body):
    response = client.request(method, path, json=body)
    try:
        payload = response.json()
    except ValueError:
        payload = {"__text__": response.text}
    return {"status": response.status_code, "body": payload}


def main() -> int:
    check_only = "--check" in sys.argv
    OUT.mkdir(parents=True, exist_ok=True)
    client = TestClient(app)

    changed, written = [], 0
    for case_id, method, path, body in CASES:
        got = record(client, method, path, body)
        target = OUT / f"{case_id}.json"
        text = json.dumps(got, indent=2, sort_keys=True) + "\n"
        if target.exists() and target.read_text() != text:
            changed.append(case_id)
        if not check_only:
            target.write_text(text)
            written += 1

    if check_only:
        if changed:
            print(f"DRIFT in {len(changed)} case(s): {', '.join(changed)}")
            return 1
        print(f"no drift across {len(CASES)} cases")
        return 0

    print(f"wrote {written} fixtures to {OUT.relative_to(ROOT)}")
    if changed:
        print(f"  {len(changed)} changed: {', '.join(changed)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
