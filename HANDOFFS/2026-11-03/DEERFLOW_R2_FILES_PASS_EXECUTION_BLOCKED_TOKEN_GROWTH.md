# R2 — First real file writes verified (execution still blocked)
Date: 2026-11-03
Source: operator screenshot of DeerFlow R2 UI; user-visible evidence, not direct filesystem audit.

## Verified in screenshot
- Luna used `write_file` and `read_file` to create and read:
  - `/mnt/user-data/workspace/prueba_r2_normalizar_folio/normalizar_folio.py`
  - `/mnt/user-data/workspace/prueba_r2_normalizar_folio/test_normalizar_folio.py`
- UI reported `FILES_PASS`; two files edited (+58 lines); five automated test methods exist but were **not run**.
- Agent reported no authorized code-execution tool available in the session.
- UI token counter displayed **49.6K total for the chat at screenshot time**, vs 10.9K on first blocked stage. This must not be misrepresented as 49.6K for a single request or as confirmed billable spend.
- Screenshot shows normalizer with regex for optional UMB- followed by digits, preserving leading zeros; exact test correctness unverified.

## Gate statuses
`R2_FILES_WRITE_READ=PASS_REPORTED_AND_UI_EVIDENCE`
`R2_UNIT_TEST_EXECUTION=BLOCKED`
`GIT_ARTIFACT_DURABILITY=NOT_PROVEN`
`TOKEN_EFFICIENCY=NOT_PROVEN`
`CODEX_CLOUD_WORKERS=NOT_CONNECTED`

## Critical configuration
LocalSandboxProvider maps virtual `/mnt/user-data/workspace` to a thread-specific physical folder under gateway runtime home; not necessarily the same physical path to `docker exec`. Sandbox local `allow_host_bash=false`; do not enable unrestricted host bash in gateway just to pass a proof. Need isolated worker/sandbox for execution, test both execution and persistence across tasks. Avoid further trivial model smoke tests.

## Decision
Stop chasing provider chat; the next experiment must focus on securely executing the **existing five tests**, not rebuilding examples from scratch. Document exact toolbox and isolation, then one end-to-end result. Operator time and tokens are primary measured costs.
