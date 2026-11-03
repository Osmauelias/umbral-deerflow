#!/usr/bin/env python3
"""Read DeerFlow's existing per-call token logs without any model/API requests.

Do not print raw logs. These records may mix models; provider attribution needs traces.
"""
import argparse
import json
import re
import subprocess
import sys

USAGE = re.compile(r"LLM token usage: input=(\d+) output=(\d+) total=(\d+)")

def extract(text: str) -> list[dict]:
    return [
        {"input": int(m[1]), "output": int(m[2]), "total": int(m[3])}
        for m in USAGE.finditer(text)
    ]

def summarize(rows: list[dict], limit: int, threshold: int) -> dict:
    latest = rows[-limit:]
    return {
        "status": "MEASURED_UNATTRIBUTED" if latest else "NO_DATA",
        "sample_calls": len(latest),
        "model_attribution_available": False,
        "total_input": sum(r["input"] for r in latest),
        "total_output": sum(r["output"] for r in latest),
        "max_input_per_call": max((r["input"] for r in latest), default=None),
        "calls_over_threshold": sum(r["input"] > threshold for r in latest),
        "threshold_input_per_call": threshold,
        "calls": latest,
        "caveat": "Mixed models; per-call logs are neither UI thread totals nor billed charges.",
    }

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--since", default="60m")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--max-input", type=int, default=12000)
    a = parser.parse_args(argv)
    if a.limit <= 0 or a.max_input <= 0 or not re.fullmatch(r"\d+[smh]", a.since):
        print("INVALID_PARAMETERS", file=sys.stderr)
        return 2
    try:
        result = subprocess.run(
            ["docker", "logs", "--since", a.since, "deer-flow-gateway"],
            text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            timeout=15, check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        print("BLOCKED_DOCKER_LOG_READ", file=sys.stderr)
        return 2
    if result.returncode != 0:
        print("BLOCKED_DOCKER_LOG_READ", file=sys.stderr)
        return 2
    data = extract(result.stdout + "\n" + result.stderr)
    report = summarize(data, a.limit, a.max_input)
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "MEASURED_UNATTRIBUTED" else 2

if __name__ == "__main__":
    raise SystemExit(main())
