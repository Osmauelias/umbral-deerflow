# DEERFLOW — OpenAI API managed GPT-6 models route to Chat Completions, HTTP 400
Date: 2026-11-03. State: ROOT CAUSE SOURCE CONFIRMED / FIX INSTRUCTED / LOCAL APPLY & SMOKE NOT YET VERIFIED.

## Observed from user
- Operator connected OpenAI API models gpt-6-luna and gpt-6-sol via DeerFlow Settings > Models.
- Both in DeerFlow chat failed 400: `Function tools with reasoning_effort are not supported for gpt-6-luna [or gpt-6-sol] in /v1/chat/completions. To use function tools, use /v1/responses or set reasoning_effort to 'none'`.
- This is a different endpoint and server error than ChatGPT OAuth Codex adapter's 400 at `chatgpt.com/backend-api/codex/responses`. Underlying similarities possible but NOT proven same cause.
- UI previous Gemini run reported ~42.1K tokens input for `GEMINI_OK`, much smaller than earlier ~102.1K but still high; different history/prompt, no causal attribution.

## Repo source confirms routing gap
- `backend/packages/harness/deerflow/config/managed_model_providers.py`: preset `openai` supplies `base_url=https://api.openai.com/v1` through `resolve_preset_model`; no `use_responses_api` in defaults/capabilities for gpt-6.
- `backend/packages/harness/deerflow/models/factory.py`: `_apply_openai_responses_api_default` correctly enables Responses for gpt-6 when endpoint unset, but **skips when `base_url` exists**, even if official OpenAI endpoint. Thus managed OpenAI presets from UI bypass safety routing.
- `ModelConfig` already supports `use_responses_api` and `output_version`; managed model UI does not expose these options.

## Bounded local workaround provided to operator
In `_capabilities(provider, model)` directly below `result = {"reasoning": ...}` add:
```python
if provider == "openai" and model.startswith("gpt-6"):
    result.update(use_responses_api=True, output_version="responses/v1")
```
Operator given idempotent backup + exact-text edit, container-side resolver assertions using a DUMMY key and conditional existing-container restart. API key stays encrypted in managed catalog; not printed, copied or committed.

## Next proof
- Confirm local output: PARCHE_INSTALADO, Responses flags for gpt-6-luna/gpt-6-sol/gpt-6.1-sol, GATEWAY_REINICIADO.
- In new DeerFlow chats smoke Luna and Sol with no tools, then one cheap real scratch-file creation/test mission, no product repos.
- Mark `OPENAI_RESPONSES_PASS` and `FILE_TOOL_PASS` only after real observable results.
- Durable source patch/unit test and Git commit needed after local smoke. This handoff alone is not source code fix or tested service.
- ACP/Codex Cloud remains unconnected. Frontend chat success alone is not worker execution.

## Lessons
`MODEL_REGISTERED != WIRE_PROTOCOL_COMPATIBLE`
`CUSTOM_BASE_URL != THIRD_PARTY_GATEWAY` when URL is official vendor.
`ROOT_CAUSE_SOURCE_A != ROOT_CAUSE_SOURCE_B` even if both return 400.
