# DEERFLOW — Managed OpenAI GPT-6 Responses patch applied and gateway restarted
**Date:** 2026-11-03
**State:** LOCAL_PATCH_PASS / RUNTIME_RESTART_PASS / PROVIDER_CHAT_SMOKE_PENDING / WORKER_PASS_PENDING

## Human-reported validation
Operator ran scoped patch to `backend/packages/harness/deerflow/config/managed_model_providers.py` so managed OpenAI gpt-6 models receive `use_responses_api=True` and `output_version="responses/v1"`.
Terminal output:
```
PARCHE_INSTALADO
gpt-6-luna RESPONSES_OK
gpt-6-sol RESPONSES_OK
gpt-6.1-sol RESPONSES_OK
deer-flow-gateway
GATEWAY_REINICIADO
```

These are local configuration and restart checks, not proof of live model response or worker execution. The local source modification may be uncommitted; do not assume recoverability in a new Codespace until the limited diff is committed and pushed.

## Codex ChatGPT Plus is a separate bug
An earlier direct `CodexChatModel` call to `chatgpt.com/backend-api/codex/responses` passed both with no tools and one inert function tool, but the full DeerFlow chat returned HTTP 400. That endpoint already uses Responses semantics and does not benefit from the managed OpenAI routing patch. A small corrective patch may be possible once the rejecting field is isolated; do not claim same root cause.

## Next gates
1. Fresh Luna chat smoke `LUNA_RESPONSES_OK`.
2. Fresh Sol chat smoke `SOL_RESPONSES_OK`; verify model ID in selector.
3. Real scratch-file + tests using available tools; if only text returned, mark `WORKER_FAIL/BLOCKED`.
4. Preserve source patch in a narrowly scoped Git commit/branch once smoke confirmed, without touching production repos or secrets.
5. Later instrument sanitized upstream Codex 400 reason to identify precise incompatible payload parameter before patching old adapter.

## Invariants
`CONFIG_FLAGS_PASS != PROVIDER_CHAT_PASS != WORKER_PASS`; `CODEX_CLOUD_NOT_CONNECTED`; `SECRET_KEY_NOT_COMMITTED`.
