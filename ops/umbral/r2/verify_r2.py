#!/usr/bin/env python3
"""Run the ORIGINAL DeerFlow R2 files in a disposable networkless Docker container.

This script never creates replacement folio files and never calls an LLM.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

FILES = ("normalizar_folio.py", "test_normalizar_folio.py")
SUBDIR = "prueba_r2_normalizar_folio"
IMAGE = "python:3.12-slim"

def discover(repo: Path) -> list[Path]:
    matches = []
    for root in (repo / "backend" / ".deer-flow", repo / ".deer-flow"):
        if not root.is_dir():
            continue
        for folder in root.glob(f"**/user-data/workspace/{SUBDIR}"):
            if folder.is_dir() and all((folder / name).is_file() for name in FILES):
                matches.append(folder.resolve())
    return sorted(set(matches), key=lambda p: (p.stat().st_mtime, str(p)), reverse=True)

def check_folder(path: Path) -> Path:
    p = path.expanduser().resolve(strict=True)
    if p.name != SUBDIR or not p.is_dir():
        raise ValueError("Expected the original prueba_r2_normalizar_folio directory")
    if not all((p / f).is_file() and not (p / f).is_symlink() for f in FILES):
        raise ValueError("Original Python files absent or symlinked")
    return p

def receipt(folder: Path, status: str, code: int | None = None) -> dict:
    return {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "original_workspace": str(folder),
        "files": {
            name: {"sha256": hashlib.sha256((folder / name).read_bytes()).hexdigest(),
                   "bytes": (folder / name).stat().st_size}
            for name in FILES
        },
        "status": status,
        "exit_code": code,
        "isolation": {"network": "none", "filesystem": "read-only",
                      "privileges": "none", "model_requests": 0},
    }

def docker_command(folder: Path) -> list[str]:
    return [
        "docker", "run", "--rm", "--network", "none", "--read-only",
        "--security-opt", "no-new-privileges", "--cap-drop", "ALL",
        "--pids-limit", "64", "--memory", "256m", "--cpus", "1",
        "--user", "65534:65534", "-e", "PYTHONDONTWRITEBYTECODE=1",
        "--mount", f"type=bind,source={folder},target=/work,readonly",
        "-w", "/work", IMAGE,
        "python", "-m", "unittest", "discover", "-v", "-p", "test_normalizar_folio.py",
    ]

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument("--path", type=Path, help="Location of the original R2 folder")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--receipt", type=Path, help="Write a JSON evidence receipt")
    args = parser.parse_args(argv)
    try:
        folders = [args.path] if args.path else discover(args.repo)
        if len(folders) != 1:
            print("BLOCKED: expected exactly one original R2 folder", file=sys.stderr)
            for folder in folders:
                print(folder, file=sys.stderr)
            return 2
        folder = check_folder(folders[0])
        if args.dry_run:
            print(json.dumps(receipt(folder, "FILES_FOUND_TESTS_NOT_RUN"), indent=2))
            return 0
        if shutil.which("docker") is None:
            print("BLOCKED: Docker is required for isolated execution", file=sys.stderr)
            return 3
        print("Executing the original tests in an isolated, networkless runner", flush=True)
        result = subprocess.run(docker_command(folder), timeout=90, check=False)
        status = "TESTS_PASS" if result.returncode == 0 else "TESTS_FAIL"
        data = receipt(folder, status, result.returncode)
        print(json.dumps(data, indent=2))
        if args.receipt:
            args.receipt.write_text(json.dumps(data, indent=2) + "\n")
        return 0 if result.returncode == 0 else 1
    except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
        print(f"BLOCKED: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 3

if __name__ == "__main__":
    raise SystemExit(main())
