# C0 — POST RESTART: CODEX HTTP 400 / GEMINI PASS — 2026-11-03
Status: PARTIAL PASS / CODEX BLOCKED / ROOT CAUSE NOT YET ISOLATED

## Human-observed result
The edited config YAML parsed successfully (`YAML_OK`), then existing `deer-flow-gateway` Docker container restarted. A fresh Codex chat prompt `Responde únicamente: CODEX_OK. No uses herramientas.` returned `LLM request failed: Client error '400 Bad Request' for url 'https://chatgpt.com/backend-api/codex/responses'` after ~2s. A separate Gemini Flash-Lite chat responded exactly `GEMINI_OK` on the same post-restart DeerFlow frontend.
Prior Docker inspection showed `CODEX_MOUNT_PRESENTE`, meaning mount destination present, not proof of usable auth.
The token totals for these post-restart prompts are not yet supplied.

## Distinguish
`GATEWAY_RESTART_PASS = YES` (command exited and named container returned)
`GEMINI_CHAT_POST_RESTART = PASS`
`CODEX_CHAT_POST_RESTART = FAIL_400`
`CODEX_AUTH_INTACT = UNKNOWN`
`SKILL_DEFERRED_CONFIGURED = YES`
`SKILL_EXECUTION = NOT_TESTED`
`TOKEN_EFFICIENCY_IMPROVED = NOT_MEASURED`
`ROOT_CAUSE = UNKNOWN`

## Code source and prior history
The custom Codex adapter `backend/packages/harness/deerflow/models/openai_codex_provider.py` calls `https://chatgpt.com/backend-api/codex/responses` with a `model` field, streaming. Its Python class default is `gpt-5.4`. On 2026-11-02, a Codex 400 was followed by selecting `gpt-6.1-sol` and a reported successful chat, but that observation was not a controlled causal isolation.
Check currently loaded `models[]` config for `name/model/use` (safe fields only) BEFORE altering auth, model or retrying paid requests. If `gpt-6.1-sol` is already configured, next step should collect a minimized upstream error reason securely without leaking token or user information. 400 cannot be assumed to mean auth expired or a single model mismatch.

## Safety
No more blind restarts; no overlay recreation; no secrets in repo; no production project edits. Codespaces remains dev-only. Do not claim five-provider healthy after restart.

## Next test
Read-only effective model config diagnosis. Then a single justified smoke test after correcting a proven cause. Continue with low-cost skill execution test only when stable.
