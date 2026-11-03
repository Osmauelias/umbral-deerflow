#!/usr/bin/env python3
"""Opt-in proof of OpenAI Agents API hosted Codex harness. No billing without --execute.

Use a separate OPENAI_API_KEY with api.agents.read/write and api.responses.write.
This is NOT ChatGPT-plan Codex Cloud.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import zipfile

OUTPUT = "/workspace/outputs/umbral_r2_bundle.zip"

TASK = (
    "Create normalizar_folio.py and test_normalizar_folio.py with at least five "
    "executed Python unittest tests. Rules: strip outer whitespace, uppercase letters, "
    "accept digits with optional UMB- prefix, preserve leading zeros, reject internal "
    'spaces, bad punctuation, empty and non-string values. " 123 " => UMB-123, '
    '"umb-00123" => UMB-00123, " 0007 " => UMB-0007, "UMB- 12" must raise ValueError. '
    "Execute tests with Python, capture the real stdout/stderr and exit status in "
    "test_output.txt, and put exactly normalizar_folio.py, test_normalizar_folio.py "
    f"and test_output.txt in a ZIP at {OUTPUT}. "
    "No external websites, package installations or repository changes. "
    "Report actual tests; never fabricate successful execution."
)

def plan(model: str) -> dict:
    return {
        "provider": "OpenAI Agents API (billed separately from ChatGPT Plus)",
        "model": model, "environment": "openai_hosted",
        "expected_artifact": OUTPUT, "execution_requires": "--execute",
        "cost_note": "Prepaid balance is not a reliable per-run hard cost cap",
    }

def run_worker(model: str, output: Path) -> dict:
    if not os.environ.get("OPENAI_API_KEY", "").strip():
        raise RuntimeError("Missing local OPENAI_API_KEY; do not share secrets in chat")
    try:
        from openai import OpenAI
    except ImportError as error:
        raise RuntimeError("Current official openai Python SDK not installed") from error
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        raise RuntimeError("Refusing to overwrite an existing artifact receipt")
    with OpenAI() as client:
        with client.beta.agents.sessions.create(
            agent={
                "model": model,
                "instructions": "Write code, execute tests and publish actual artifacts under /workspace/outputs.",
            },
            environment={"type": "openai_hosted"},
            input=TASK,
            stream=True,
        ).with_result_collection() as stream:
            event_count = 0
            for _event in stream:
                event_count += 1
            result = stream.get_final_result()
        session_id = result.session_id
        if not session_id:
            raise RuntimeError("Agent session did not return a session ID")
        artifact = None
        for item in client.beta.agents.sessions.artifacts.list(session_id):
            if item.path == OUTPUT:
                artifact = item
        if artifact is None:
            raise RuntimeError("Expected ZIP was not published in the cloud session")
        with client.beta.agents.sessions.artifacts.with_streaming_response.content(
            artifact.id, session_id=session_id,
        ) as response:
            response.stream_to_file(output)
    with zipfile.ZipFile(output) as zf:
        expected = {"normalizar_folio.py", "test_normalizar_folio.py", "test_output.txt"}
        if set(zf.namelist()) != expected or any(i.file_size > 200_000 for i in zf.infolist()):
            raise RuntimeError("ZIP does not satisfy artifact name/size contract")
    return {
        "status": "ARTIFACT_DOWNLOADED_TESTS_NOT_INDEPENDENTLY_REVERIFIED",
        "provider": "openai-agents-api", "model": model,
        "session_id": session_id, "artifact_id": artifact.id,
        "artifact_sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
        "bytes": output.stat().st_size, "event_count": event_count,
        "path": str(output),
    }

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default="gpt-6.1-sol")
    parser.add_argument("--execute", action="store_true", help="Authorize a paid Agents API session")
    parser.add_argument("--output", type=Path, default=Path("/tmp/umbral_r2_cloud_bundle.zip"))
    args = parser.parse_args(argv)
    if not args.execute:
        print(json.dumps(plan(args.model), ensure_ascii=False, indent=2))
        return 0
    try:
        print("PAID_AGENT_SESSION_REQUESTED", flush=True)
        print(json.dumps(run_worker(args.model, args.output), ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        print("BLOCKED: " + type(exc).__name__ + "; inspect locally, never copy auth error bodies", file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
