# Cierre técnico del experimento DeerFlow — 2026-11-06

**Decisión humana (Osvaldo):** retirar DeerFlow del stack activo de Umbral/AIDOH. Clasificación reversible: `FROZEN / EVALUATED_NOT_WORTH_CONTINUING_NOW`, no incapacidad universal ni `DISCARD_FINAL`.

## Problema que queríamos resolver
Relevo Codex ↔ Claude ↔ Codex al agotarse cuota o bloquearse un proveedor, manteniendo código, tests y contexto durable sin que Osvaldo mueva mensajes ni mantenga infraestructura. Alternativas permitidas: suscripciones y/o APIs si costo total e intervención humana son aceptables.

## Hechos recuperados
- R1: cambio manual de modelos dentro del mismo hilo preservó instrucciones. NO hubo failover automático, continuidad de archivos entre workers ni segundo worker real.
- R2: Luna escribió/leyó `normalizar_folio.py` y `test_normalizar_folio.py`; cinco test methods presentes. No se corrieron desde DeerFlow por falta de ejecución autorizada. Captura/UI: `FILES_PASS`, 49.6K tokens de conversación (47.4K input y 2,228 output), no costo facturado ni consumo aislado por petición.
- El 2026-11-06 el operador localizó ambos archivos originales en la carpeta privada de thread bajo `backend/.deer-flow/users/<user-id>/threads/<thread-id>/user-data/workspace/prueba_r2_normalizar_folio/`. Su contenido se presentó íntegro y se preservó en esta rama con huellas verificadas:
  - `EVIDENCE/2026-11-06/R2/normalizar_folio.py` — SHA256 `c8ecc8769ec9f5c2ad73d661fb0cdd1e4a5bd54e7a62e3ed38fd5cbda2b4ddb8`
  - `EVIDENCE/2026-11-06/R2/test_normalizar_folio.py` — SHA256 `a659d304fef6dc075c326c98ff6d9dfb91b409b6f22bdae72bc7a9ec00839b24`
- **Preservación:** copia reconstruida de la transcripción completa enviada por el operador y cotejada por SHA256; no se accedió por API al filesystem original del Codespace. No afirmar ejecución de tests.
- Owner main a la revisión: `0e5dc15420bfcdc69931273b5392015c694d2c79`.
- Rama experimental `architecture/umbral-r2-execution-gates-20261103` / PR #1 DRAFT: `verify_r2.py`, `token_audit.py`, `cloud_smoke.py`, manual y pruebas offline. GitHub Actions `UMBRAL R2 and Cloud adapter contract checks` = SUCCESS sobre utilidades (11 pruebas offline reportadas); NO los cinco tests originales R2. Lint backend = FAIL (orden de imports, Ruff I001). PR no es PASS de orquestación.
- Codespace al cierre: `/workspaces/deer-flow`, branch `fix/managed-gpt6-responses-20261103`; archivos no versionados `.extensions_config.json.lock` y `backend/packages/harness/deerflow/config/managed_model_providers.py.umbral-backup` no fueron examinados ni descartados.
- Terminal: `docker info` = 29.9.2-2; imagen `python:3.12-slim` NO descargada; verificador en ref `origin/architecture/...` local NO localizado, aunque está confirmado en remoto GitHub.
- `config.yaml` local: `# acp_agents:` está comentado y `agents_api.enabled: false`; no prueba impossibilidad de configurar ACP. UI lista Codex Plus y Claude como modelos conversacionales, no como coding workers con relevo.
- `CODEX_CLOUD_WORKER_CONNECTED=NO`; `CLAUDE_REVIEW_WORKER_PASS=NO`; `AUTOMATIC_FAILOVER_PASS=NO`; `COST_PER_HANDOFF_VERIFIED=NO`.

## Causa de descarte por ahora
El esfuerzo del operador, mantenimiento de Codespaces, contexto caro y necesidad de instrumentar workers/failover superaron la evidencia de valor. La decisión es económica/operativa de Umbral a fecha del cierre, no prueba negativa sobre todo DeerFlow.

## Cambios y límites
- Esta rama `archive/deerflow-closed-20261106` conserva código de la prueba R2 y este documento; NO merge a main ni deploy.
- No se ejecutaron Docker tests, llamadas Codex/Claude/Gemini, APIs de agentes o servicios pagados para producir este cierre.
- PR #1 y rama experimental se conservan como procedencia histórica; no desplegar ni reactivar.
- No eliminar Codespace, volumen, copia `.umbral-backup`, configuración privada ni otras ramas hasta revisar archivos únicos. Detener computación sí puede evitar seguir acumulando horas de Codespaces, pero conservar almacenamiento puede seguir facturando según cuota.
- No tocar AIDOH/Cafetería, Frankenstein, Booking, Torre ni producción.

## Condición de reabrir (sin backlog activo)
Solo cuando exista una necesidad de negocio demostrable Y una capacidad nueva/actualización concreta que permita un relevo Codex→Claude→Codex con GitHub durable, ejecución de pruebas independiente, una sola intervención humana inicial, costes por tarea medidos, topes/preflight y comparación de referencia sin DeerFlow. Nueva autorización humana requerida. No abrir por curiosidad ni por un modelo nuevo en menú.

## Fuentes / continuidad
- [PR #1](https://github.com/Osmauelias/umbral-deerflow/pull/1)
- [Manual de campo](https://github.com/Osmauelias/umbral-deerflow/blob/architecture/umbral-r2-execution-gates-20261103/docs/umbral/DEERFLOW_MANUAL_DE_CAMPO_V1.md)
- [Issue #20](https://github.com/Osmauelias/umbral-documentador/issues/20)
- Central: `Osmauelias/umbral-documentador/INBOX/ENTRADAS/2026-11-06_DEERFLOW_CIERRE_EXPERIMENTO_OSVALDO.md`.
- Radar: `Osmauelias/umbral-documentador/RADAR/TOOL_RADAR.md`.
- AIDOH: `Osmauelias/Umbral-AIDOH/SCOUT/2026-11-03_DEERFLOW_ORCHESTRATION_MULTI_PROVIDER_COST_CONTINUITY_EVALUATION.md`.

**Resultado:** `TECH_EXP CLOSED_BY_HUMAN`; `R1_MANUAL_CONTEXT_PASS`; `R2_FILE_WRITE_READ_PASS`; `AUTOMATED_WORKER_HANDOFF_NOT_PROVEN`; `HARD_COST_CAP_NOT_PROVEN`; `PRODUCTION_AUTHORIZED=NO`.
