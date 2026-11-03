# C0 — Codex direct PASS vs. DeerFlow 400 — 2026-11-03

**Estado:** DIFERENCIA AISLADA / CAUSA ESPECÍFICA PENDIENTE

## Observaciones verificadas en conversación
1. Gateway reiniciado tras YAML validado. Gemini contestó `GEMINI_OK` desde DeerFlow UI.
2. Codex desde DeerFlow UI falló HTTP 400 en `https://chatgpt.com/backend-api/codex/responses`.
3. YAML efectivo muestra `codex-chatgpt`, modelo `gpt-6.1-sol`, adaptador `deerflow.models.openai_codex_provider:CodexChatModel`; no es una regresión visible al ID modelo antiguo.
4. Prueba aislada **en el mismo Gateway**: `CodexChatModel(model="gpt-6.1-sol")._call_codex_api([HumanMessage(...)], tools=[])` devolvió `CODEX_DIRECT_PASS`; las credenciales pudieron cargarse.

## Interpretación y límites
La integración de Codex, credencial y modelo funcionan para solicitudes mínimas. HTTP 400 desde UI probablemente se debe a elementos adicionales del payload de agente (tools/schema/tool_choice, system prompt, historial o middleware) o cambios de contexto por runtime, pero no está aún probado cuál. `DIRECT_PASS != DEERFLOW_TOOLING_PASS`.

## Evidencia del código
`backend/packages/harness/deerflow/models/openai_codex_provider.py`:
- `_convert_messages` concatena SystemMessage en instructions, convierte historial user/assistant/tool.
- `_convert_tools` emite function tools (name,description,parameters,strict cuando presente).
- `_call_codex_api` añade opcionalmente tools y tool_choice; usa respuesta streaming.
- `bind_tools` convierte tool schemas del harness a OpenAI function format.

## Siguiente gate pequeño
Probar UNA solicitud directa con exactamente UNA herramienta ficticia de lectura, sin mutaciones ni llamada a herramientas ejecutables, y capturar sólo estado/código/motivo sanitario de error. Si PASS, inspeccionar schemas/conteo/contexto del harness; si FAIL 400, revisar compatibilidad tool payload del adaptador. NO reinstalar, no renovar credenciales a ciegas, no modificar producción.

## Seguridad
Nunca registrar access token, account ID, headers, payload completo, ni error cuerpo crudo. Habilitar sólo comandos de diagnóstico acotado, no reconfigurar overlay perdido ni recrear contenedores. Sin nuevas escrituras a Cafetería/Frankenstein.

## Lección
`MODEL_AUTH_PASS != AGENT_PAYLOAD_COMPATIBILITY_PASS` y `NO_USES_HERRAMIENTAS` en prompt no implica que el harness omita definiciones de herramientas.
