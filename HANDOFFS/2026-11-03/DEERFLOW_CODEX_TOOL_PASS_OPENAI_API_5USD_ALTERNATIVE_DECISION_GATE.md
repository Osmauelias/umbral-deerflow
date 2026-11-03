# DEERFLOW — CODEX TOOL PASS / API OPENAI ALTERNATIVE — 2026-11-03

**Status:** CODEx_DIRECT_TOOL_PASS / UI_HTTP_400 / API_ALTERNATIVE_RESEARCHED_NOT_PURCHASED / R2_NOT_STARTED
**Human decision:** operator proposed comparing US$5 OpenAI API credit versus debugging ChatGPT-backed Codex adapter.

## Evidence from controlled tests
1. YAML parsed and existing Docker gateway restarted. Gemini UI `GEMINI_OK`, Codex UI 400 at chatgpt.com/backend-api/codex/responses.
2. Gateway effective model: `codex-chatgpt`, `gpt-6.1-sol`, custom `CodexChatModel`.
3. In same Gateway `_call_codex_api` with one HumanMessage and tools=[] PASS.
4. Repeated with one innocuous function tool `umbral_ping` passed as tool schema, PASS: `CODEX_CON_HERRAMIENTA_PASS`. This did NOT execute tool, create files, or delegate workers.
5. Full DeerFlow request still fails HTTP 400; cause unknown. Broad hypothesis: composition of tool schema, full system context, history, tool_choice, middleware serialization. The result rules out unconditional inability to send *any* tool schema.

## Architectural distinction
- Route A: `Codex CLI/ChatGPT account via custom adapter` uses ChatGPT authenticated session and Codex endpoint; can make model requests from Gateway when payload is acceptable, but is not itself ACP worker or Codex Cloud job.
- Route B: `OpenAI API key + standard OpenAI Responses API in DeerFlow`. This is a normal LLM provider, billed separately from ChatGPT Plus; avoids maintaining unofficial/custom ChatGPT endpoint adapter in the chat path. It still does NOT create Codex Cloud workers or automatic quota failover. Connect ACP/CLI or Cloud separately if desired.
- Route C: `Codex CLI/ACP executor or Codex Cloud`. Separate identity, authorization, tools, persistence, execution contract and gates; model chats do not prove Codex worker dispatch.

## Cost research (as at 2026-11-03)
Official OpenAI API prepaid initial purchase minimum US$5, auto-recharge on by default during setup (turn OFF for bounded experiment); prepaid balance can lag/overrun slightly and expires after one year. OpenAI API credits are not ChatGPT/Codex signed-in usage credits. Official GPT-6.1 Sol API model available via Responses: standard $2/M uncached input, $10/M output; GPT-6 Luna $0.10/M input, $0.50/M output. At 50K input + 500 output, Sol approximately US$0.105 and Luna US$0.00525 before caching, tools, taxes and any variant surcharge; these are examples, not measured invoices.
Sources:
https://help.openai.com/es-419/articles/8264644-setting-up-and-managing-prepaid-api-billing
https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex
https://developers.openai.com/api/docs/models/gpt-6.1-sol
https://developers.openai.com/api/docs/models/gpt-6-luna
https://help.openai.com/es-419/articles/20001545-using-codex-cloud
Repo example: config.example.yaml OpenAI Responses API uses `langchain_openai:ChatOpenAI`, `api_key: $OPENAI_API_KEY`, `use_responses_api: true`; tool calling on gpt-6.1-sol requires Responses. No key creation/purchase or runtime change executed.

## Proposed decision and smallest test
Recommend stop costly blind debugging of 400 for now; if operator approves spending US$5, buy exactly that through OpenAI API Platform with auto-recharge disabled and check existing available grants. Create project-restricted API key; store privately in .env/secret manager, never chat/Git. Add one OpenAI standard Responses API model in scratch/test config; do not alter existing `codex-chatgpt`; run chat+one tool+usage bill measurement. Preserve current Codex OAuth adapter as fallback subject to separate repair. Need future ACP worker test for real code execution, Git artifact persistence and provider failover.
`NO_API_PURCHASE_AUTHORIZED`; `NO_OPENAI_API_CONFIG_CHANGE`; `R2_WORKER_PASS=NO`; `CODEX_TOOL_SCHEMA_PASS=YES_MINIMAL`.

## Lessons
`CUSTOM_CHATGPT_ADAPTER != OPENAI_API != CODEX_CLOUD_WORKER`.
`TOOL_SCHEMA_ACCEPTED != TOOL_EXECUTED`.
`PREPAID_5USD != GUARANTEED_HARD_COST_CEILING`.
