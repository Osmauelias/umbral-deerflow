# R1 — RELEVO DE CONTEXTO ENTRE MODELOS EN DEERFLOW
Fecha: 2026-11-03, Mexico. Fuente: observación directa del chat de DeerFlow en Codespaces por Browser read-only.
Conversación: https://crispy-funicular-q7w5xxrp956gh4px4-2026.app.github.dev/workspace/chats/91f9892d-79df-4539-a9fd-6f893ad75de9

## Pasos ejecutados por el operador
1. Codex — ChatGPT Plus, prompt sin herramientas: función Python `normalizar_folio(texto)`, elegir prefijo de tres letras, normalizar entrada y validar vacío.
2. Claude — Programador Umbral, MISMO thread, nuevo modelo seleccionado manualmente: preservar prefijo elegido por Codex y añadir rechazo de espacios internos.
3. Gemini Flash-Lite — Umbral, MISMO thread, nuevo modelo seleccionado manualmente: auditar ambos turnos y detectar errores.

## Resultado observado
Codex eligió `UMB`; retornó formato `UMB-{folio}`, trim, uppercase y error por vacío.
Claude identificó literalmente `UMB` del turno anterior, conservó la función y añadió `if any(c.isspace() for c in folio): raise ValueError(...)`; proporcionó tres pruebas esperadas, **no ejecutadas**.
Gemini identificó `UMB`, confirmó conservación y revisó requisitos; no ejecutó herramientas.
`R1_MANUAL_SHARED_THREAD_CONTEXT = PASS`.
`LIVE_CODE_EXECUTION = NOT_TESTED`.
`PERSISTENT_SHARED_FILES = NOT_TESTED`.
`DELEGATED_SUBAGENT = NOT_TESTED`.
`QUOTA_ERROR_AUTOMATIC_FAILOVER = NOT_TESTED`.
Grok no participó en los tres turnos iniciales; se ha propuesto un cuarto turno acotado, pendiente de ejecución.

## Telemetría observada en UI, interpretación limitada
- Codex: input 13.8K, output 123, total mostrado 14.0K.
- Claude: input 26.1K, output 712, total mostrado 26.8K.
- Gemini: input 102.1K, output 326, total mostrado 102.5K.
- Total de hilo mostrado: 143.2K tokens.
Nota: token counts provienen de UI; no se ha reconciliado con facturación, cache/prompt serialization o mecanismo exacto. Crecimiento desproporcionado para tarea trivial; `CONTEXT_COST_AUDIT = BLOCKER_FOR_SCALE`. No equiparar cifra de tokens con cargo monetario.

## Hallazgos
- Relevo manual entre tres proveedores funcionó y disminuye copiar/pegar contexto.
- No confundir cambio de modelo por UI con un agente que delega por su cuenta, ni con failover automático.
- El cuello de botella emergente es tamaño del prompt/contexto por cambio de proveedor, posible ampliación por configuración de skills/historia/metadata; antes de llamar más modelos reiteradamente medir composición de prompt y límites, sin exponer credenciales.
- Frankenstein puede aspirar a ser motor/herramienta propia detrás de DeerFlow vía API/MCP sujeto a gate; esta R1 NO valida dicha integración ni autoriza descongelamiento.

## Siguiente gate
R1 cuarto turno opcional: Grok revisa el trabajo previo, identifica prefijo y mejora con validación alfanumérica sin herramientas. Medir tokens. Luego pausar llamadas y auditar inflación del prompt. Gate R2: entrega/retoma de archivos persistentes sin tocar AIDOH ni Frankenstein; Gate R3: error de proveedor simulado, relevo determinista.

## VEREDICTO
`OUTPUT=R1_MANUAL_CONTEXT_PASS`; `OPERATOR_INTERVENTIONS=3_MANUAL_MODEL_SELECTIONS`; `AUTOMATIC_FAILOVER=NOT_PROVEN`; `TOKEN_CONTEXT_EFFICIENCY=NEEDS_AUDIT`; `PROJECT_REPOS_UNTOUCHED`.
