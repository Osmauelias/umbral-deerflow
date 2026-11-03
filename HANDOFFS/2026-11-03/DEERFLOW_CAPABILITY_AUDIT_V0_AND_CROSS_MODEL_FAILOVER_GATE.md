# AUDITORÍA DE CAPACIDADES Y RELEVO ENTRE MODELOS — DEERFLOW
**Fecha:** 2026-11-03 (México)  
**Origen:** DEERFLOW_CLOUD_CONTINUITY_ENGINEER  
**Autoridad de alcance:** Osvaldo; cierre anterior 2026-11-02  
**Estado:** `STATIC_SOURCE_AUDIT_DONE / RUNTIME_CAPABILITY_AUDIT_PENDING / FAILOVER_NOT_TESTED`

## Problema humano que debe resolver
El operador quiere trabajar con Codex y Claude en nube desde navegador, de modo que cuando uno agote cuota o falle **el otro continúe** sin rehacer prompts, contexto, archivos, pruebas ni decisiones. DeerFlow sólo merece conservarse si reduce fricción neta frente a un harness convencional y evita dependencia de PC local. **No confundir disponibilidad de cinco chats con continuidad de desarrollo.**

## Base de evidencia
- [Handoff de cinco modelos conectados](../2026-11-02/DEERFLOW_PHASE0_MULTI_MODEL_CLOSURE_2026-11-02.md); cinco respuestas básicas reportadas, ninguna validación de programación o delegación.
- `README.md` — Core Features, Projects, Scheduled Tasks, Security.
- `skills/public/*/SKILL.md` — 23 skills publicadas en el árbol Git; presencia en Git NO prueba activación en el Gateway.
- `backend/packages/harness/deerflow/capabilities/builtin.json` — 15 conectores/capacidades catalogados; catálogo NO equivale a instalación ni OAuth.
- `config.example.yaml` y `backend/packages/harness/deerflow/config/` — flags y backstops por defecto.
- `backend/packages/harness/deerflow/tools/builtins/invoke_acp_agent_tool.py` + `backend/packages/harness/deerflow/config/acp_config.py`: ACP externo con workspace por conversación `threads/<thread_id>/acp-workspace`, límites, autorización y errores.
- `backend/packages/harness/deerflow/agents/lead_agent/agent.py` — selección de modelo y autorización; fallback documentado cuando un modelo NO existe o permiso es denegado, NO evidencia de sustitución automática durante un fallo de cuota o API.
- `backend/Dockerfile` — Node.js + npx disponibles en imagen Gateway. Las CLI instaladas en host Codespaces no implican CLI instaladas en Gateway.

## Inventario ESTÁTICO (no declarar runtime PASS)
### Skills empaquetadas (23)
`academic-paper-review`, `bootstrap`, `chart-visualization`, `claude-to-deerflow`, `code-documentation`, `consulting-analysis`, `data-analysis`, `deep-research`, `find-skills`, `frontend-design`, `github-deep-research`, `image-generation`, `music-generation`, `newsletter-generation`, `podcast-generation`, `ppt-generation`, `skill-creator`, `skill-reviewer`, `surprise-me`, `systematic-literature-review`, `vercel-deploy`, `video-generation`, `web-design-guidelines`.
Skills de generación audiovisual pueden requerir API pagada/credenciales y ejecución real de scripts. En particular `video-generation` incluye rutas Gemini Veo/MiniMax; mera existencia de `SKILL.md` no genera video.
### Capabilities builtin catalog (15)
`lark`, `dingtalk`, `wecom`, `tencent-docs`, `notion`, `openviking`, `web-search`, `web-fetch`, `exa`, `firecrawl`, `database`, `hubspot`, `github`, `atlassian`, `browser`.
MCP/CLI/API/provider auth según plugin; la conexión de GitHub a ChatGPT **NO se transmite automáticamente** a un Gateway DeerFlow.
### Plataformas/capacidades de aplicación
- Projects: instrucciones compartidas, documentos, archivos y conversaciones; estado físico/persistencia por revalidar.
- Subagents: builtins `general-purpose`, `bash` y custom por modelo/skills/tools, límites de turnos/concurrencia/tokens; feature de administración UI `agents_api.enabled` es **false por defecto**.
- Scheduled tasks: una vez/cron/intervalo con persistencia/cola; `scheduler.enabled` es **false por defecto**.
- ACP agentes externos: configuración documenta adaptadores `@zed-industries/codex-acp` y `@zed-industries/claude-agent-acp`; comandos `codex`/`claude` estándar no hablan ACP sin adaptador. Invocación desde Gateway con espacio por thread. `auto_approve_permissions=false` DENIEGA peticiones; nunca habilitar aprobación indiscriminada para poder «hacer que funcione».
- Tooling: herramientas de file read/write, bash controlado, web search/fetch, navegador; permisos y sandbox deben verificarse.
- RAG: RAGFlow, LightRAG, WeKnora y otros como extensiones; requieren servicio y scopes adicionales. No conectar datos de clientes antes de aislamiento.
- Seguridad/costo: `sandbox.local` NO es contenedor aislado por trabajador; ejemplo `sandbox.allow_host_bash=false`. `token_budget.enabled=false` en plantilla, aunque subagents tienen backstop propio amplio. `task_continuity.enabled=false`, `tool_search.enabled=false`, `skill_evolution.enabled=false` en plantilla. Estado efectivo en `config.yaml` privado PENDIENTE.

## Hallazgo principal: hay DOS rutas distintas a evaluar
1. **Modelos en el agente DeerFlow**: alternar turnos Codex/Claude en una conversación, usar tools del propio harness y subagentes nativos. Relevo manual de contexto; todavía no prueba creación ni continuidad de ficheros.
2. **Agentes de programación ACP**: DeerFlow puede invocar herramientas de Codex/Claude Code mediante adaptadores separados con un workspace por thread; esto se parece más a dos ejecutores reales en el mismo expediente. Requiere que Gateway acceda a launcher, permiso y credenciales independientes; el host instaló CLI pero todavía NO validó ACP dentro de Gateway. El modelo Anthropic registrado en Settings **no habilita automáticamente Claude Code ACP**.

No se ha hallado respaldo para anunciar `AUTO_PROVIDER_FAILOVER_ON_QUOTA=PASS`. Debe tratarse como `NOT_IMPLEMENTED_OR_NOT_PROVEN` hasta prueba controlada. Si es necesario, diseñar orquestación explícita que captura error, cancela sin duplicar trabajo, realiza checkpoint Git y selecciona al sustituto.

## Secuencia de validación autorizada
**GATE A — inspección solo lectura.** Confirmar stack vivo, flags efectivos, skills activas, tools, ACP configurados y caminos de persistencia. No imprimir llaves/tokens ni env. Confirmar que UI del puerto 2026 privado abre.

**GATE B — cambio de modelo sin pérdida de contexto.** En thread descartable: Codex escribe plan corto sin tools; Claude retoma el mismo plan/cita estado anterior. Sin falla forzada ni cargo artificial.

**GATE C — relevo REAL en un directorio scratch.** En thread descartable y sin repos de producto, Codex produce un pequeño activo + prueba; Claude desde el mismo thread debe leer, cambiar una función y repetir prueba. Probar preferentemente ACP para comparar con simple modelo+tools. No auto-approve; permisos estrictos. Comparar con harness existente.

**GATE D — portabilidad.** Guardar fuente, pruebas, bitácora y checklist en rama aislada del owner repo; reabrir desde otro thread/entorno y continuar. `UNTRACKED_LOCAL != RECOVERABLE`.

**GATE E — fallo de proveedor.** No quemar cuota real: simular un error recuperable controlado a nivel de orquestación, verificar respuesta con estado estable y humano autorizado, sin reintentar operaciones con efectos dos veces. Medir latencia/tiempo humano y tokens.

**Criterio de negocio:** menor tiempo humano por tarea y esfuerzo de recuperación; capacidad incremental frente a harness; costo total (API + Codespaces + nuevas integraciones) medido; seguridad y privacidad dentro de alcance. Falla en estos gates -> no implementar jerarquías ni activar APIs adicionales sólo por curiosidad.

## Frontiers
`CODESPACE_DEV_ONLY`; `NO_PRODUCTION`; `AIDOH_LANDING_PHASE1_NOT_STARTED`; `CAFETERIA_UNTOUCHED`; `FRANKENSTEIN_V1_V2_LOCKED`; `HUMAN_PASS_REQUIRED`. Salvo nueva instrucción humana no tocar frontend/productivos, credenciales ni deployment.

## SIGUIENTE ACCIÓN
Recoger salida de diagnóstico READ-ONLY del Gateway; si Codespace dormido, reactivarlo; inspeccionar Capability Center en vivo. Luego configurar UN camino de relevo y correr Gate B antes de ampliar a ACP.

## VEREDICTO
`OUTPUT=STATIC_CAPABILITY_AUDIT_AND_TEST_GATE`; `RUNTIME_PASS=NO`; `FIVE_CHAT_MODELS=REPORTED_CONNECTED`; `MULTIAGENT_FAILOVER=NOT_PROVEN`; `NEXT=LIVE_READ_ONLY_STATUS_AND_GATES_B_TO_E`.
