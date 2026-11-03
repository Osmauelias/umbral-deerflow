# DEERFLOW — CAPABILITY LEARNING / R1 / NEXT EXPERIMENTS
**Fecha:** 2026-11-03 · **Owner:** DEERFLOW_CLOUD_CONTINUITY_ENGINEER
**Estado:** DOCUMENTADO / R1_CONTEXT_PASS / R2_NOT_STARTED / COST_ROOT_CAUSE_NOT_PROVEN

## Qué probamos y qué vimos
- Cinco modelos responden a chat básico; ninguno demostró todavía ejecución autónoma o failover automático.
- En un mismo thread, Codex creó función de folios con prefijo UMB; Claude conservó el prefijo y añadió validación de espacios internos; Gemini auditó el resultado. R1 manual = PASS. Grok fue invitado a cuarto turno pero no hay resultado observado confirmado.
- Tokens UI reportados: Codex input 13.8K/output 123; Claude input 26.1K/output 712; Gemini input 102.1K/output 326; conversación aproximadamente 143.2K. NO equivale a facturación medida, ni se ha aislado la causa.
- Capability Center: 23 skills built-in figuran Enabled; 5 MCP de despliegue registrados inicialmente Disabled (github, parallel-search, openviking, postgres, long-running-reports). Browser automation en catálogo abre documentación; NO instala nada. Es herramienta nativa Playwright que requiere config y Chromium; GitHub del ChatGPT != GitHub del Gateway.
- Diagnóstico seguro del Gateway previo: contenedores nginx/gateway/frontend/redis UP; agents_api/scheduler/task_continuity/token_budget/host_bash False; acp_agents=[].
- El operador detectó que actividad en UI web DeerFlow no evita necesariamente suspensión de Codespaces. Codespaces = desarrollo temporal, NO hosting durable.
- config.yaml está gitignored (.gitignore), por lo que VS Code Ctrl+P puede no encontrarlo; abrir por ruta exacta `code -r /workspaces/deer-flow/config.yaml`. Todavía NO hay evidencia de que los cambios sugeridos (skills.deferred_discovery=true, token_budget.enabled=true, 50000 tokens/run) se hayan guardado o surtido efecto.

## Decisiones y su PORQUÉ
1. Mantener Codespaces dev-only. No scripts keepalive; gastar para imitar actividad encubre una frontera del producto. Evaluar hosting persistente sólo si R2/R3 muestran beneficio real.
2. Comparar modelos con tareas acotadas. Modelo premium cambia precio por token, no explica por sí solo el tamaño del prompt; diagnosticar inflación antes de habilitar más proveedores/servicios.
3. No conectar todo el catálogo. Priorizar GitHub persistente + investigación y navegador de pruebas en entorno aislado; verificar conexión, permisos, costos y OAuth de cada Gateway.
4. Separar chat multmodelo, delegación real, archivos persistentes y failover por cuota. NO promover un PASS de etapa 1 a etapa 4.
5. No usar AIDOH productivo, Cafetería ni Frankenstein congelado para la prueba. Frankenstein como eventual proveedor API/MCP es hipótesis de arquitectura, NO implementación o autorización.
6. Gobernanza transversal: owner mantiene verdad operativa; Oficialía recibe; Documentador contrasta/distribuye; Cerebro diseña límites; AIDOH decide intervención técnica; ULM River A captura patrones con provenance, sin canon automático ni datos crudos.

## Evidencias
- [Auditoría estática y gates](https://github.com/Osmauelias/umbral-deerflow/blob/main/HANDOFFS/2026-11-03/DEERFLOW_CAPABILITY_AUDIT_V0_AND_CROSS_MODEL_FAILOVER_GATE.md)
- [R1 contexto + telemetría](https://github.com/Osmauelias/umbral-deerflow/blob/main/HANDOFFS/2026-11-03/DEERFLOW_R1_CODEX_CLAUDE_GEMINI_CONTEXT_RELAY_OBSERVATION.md)
- [Riesgo Codespaces](https://github.com/Osmauelias/umbral-deerflow/blob/main/HANDOFFS/2026-11-03/DEERFLOW_CODESPACES_IDLE_TIMEOUT_OPERATIONAL_RISK.md)
- [Handoff previo](https://github.com/Osmauelias/umbral-deerflow/blob/main/HANDOFFS/2026-11-02/DEERFLOW_PHASE0_MULTI_MODEL_CLOSURE_2026-11-02.md)

## Plan de pruebas con gates
**Gate C0 — restaurar eficiencia y continuidad segura de entorno (NEXT).** Acceder a config.yaml ignorado vía VS Code terminal, verificar YAML, comparar configuración efectiva antes/después, activar deferred_discovery con bajo riesgo y presupuesto de tokens (advertencia: presupuesto es per-run y puede contabilizar tras la primera llamada, NO presupuesto monetario preventivo). Confirmar overlay Codex privado antes de reiniciar Gateway. Prueba barata de un solo turno con conteo tokens, comparar antes y después usando similar prompt/model; sin llamar masivamente proveedores.

**Gate R1b — cuarto relevo Grok (OPCIONAL/PENDIENTE).** Si se completó, inspeccionar respuesta y tokens; no inferir que ocurrió sin evidencia.

**Gate R2 — dos modelos, mismos archivos:** Scratch NO productivo, Codex genera un archivo+test, Claude lee y corrige sobre mismo directorio, test PASS. Preferir ACP cuando auth/CLI launcher y permisos estén auditados; de lo contrario usar herramientas nativas, registrar diferencia. Commit a rama aislada con evidencia durable.

**Gate R3 — continuidad desde nuevo entorno:** reabrir con la misma evidencia Git y continuar sin conversación original ni PC local. PASS = recuperación verificada, no solo scroll historial.

**Gate R4 — caída simulada del modelo:** simular error sin agotar cuotas; checkpoint y relevo seguro, sin doble ejecución. Medir minutos humanos, pasos, latencia, tokens y facturación por fuente.

**Gate R5 — valoración AIDOH:** comparar tiempo/costo/calidad con harness alterno. Fase 1 AIDOH Landing sigue NO STARTED; Frankenstein LOCKED.

## LEARNING
R1: shared thread context PASS ≠ files/automation/failover PASS.
Prompt-token inflation: observed, root cause UNKNOWN; model tier alone insufficient.
Ignored local config != recovered config; persistence/restart and human intervention matter.
Codespaces active UI != Codespaces session activity; development compute != permanent service.

## VEREDICTO
`OUTPUT=LEARNING_HANDOFF`; `ACTUAL_IMPLEMENTATION_CHANGE=NO`; `R1=PASS`; `R2=NOT_STARTED`; `AUTO_FAILOVER=UNPROVEN`; `COST_ROOT_CAUSE=UNPROVEN`; `NEXT=CONFIG_EFFECTIVE_BASELINE_AND_CHEAP_TOKEN_RETEST`; `OSVALDO_ACTION_REQUIRED=OPEN_IGNORED_CONFIG_FOR_EXISTING_CHANGE`.
