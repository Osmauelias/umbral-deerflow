# UMBRAL / DeerFlow — arquitectura de cierre, no mapa ornamental
**Fecha:** 2026-11-03. **Dueño humano:** Osvaldo. **Área:** desarrollo experimental exclusivamente.

## Resultado obligatorio
`MISIÓN -> agente programador -> archivos -> ejecución aislada -> pruebas -> Git (commit/PR) -> revisor Claude -> evidencia -> decisión humana`.
El operador no debe copiar código ni trasladar prompts entre agentes. Nadie modifica repositorios de producto (AIDOH, Cafetería, Frankenstein) ni publica sistemas sin aprobación.

### Regla epistemológica
No confundir:
- `MODEL_API_PASS` con `TOOL_EXECUTION_PASS`.
- `write_file/read_file` con `bash` autorizado.
- `ChatGPT Codex Cloud` (tareas del producto/plan) con `OpenAI Agents API` (harness Codex administrado con factura API).
- `DeerFlow agents_api.enabled` (feature interna) con OpenAI Agents API.
- `CODEX_CHAT` con `CODEX_ACP_WORKER`.
- `50K token_budget` con límite de gasto instantáneo/preflight.
- `HANDOFF_POSTED` con `CONSUMER_ACK`.

## Arquitectura elegida — mínima
```
OPERADOR: misión + autorizaciones
   -> CONTROL: DeerFlow recibe/encamina tarea, no ejecuta shell en Gateway
   -> WORKER: OpenAI Agents API hospedado (programático, presupuesto separado)
   -> ARTIFACT: rama Git de experimento + sha256 + pruebas CI
   -> REVIEW: Claude API lee ese commit, revisión en PR (no contexto en chat)
   -> GATE: humano autoriza merge/producto
```
**Alternativa de menor factura API:** tarea nativa de Codex Cloud conectada al mismo repo, desde su web/app. No se presenta como ejecución programática desde DeerFlow hasta probar el disparo/retorno mediante una interfaz oficialmente soportada. Claude API ya conectado a DeerFlow para chat, no verificado como review worker.

Fuentes:
- https://developers.openai.com/api/docs/guides/agents-api/overview
- https://developers.openai.com/api/docs/guides/agents-api/quickstart
- https://help.openai.com/en/articles/20001545-using-codex-cloud
- https://github.com/bytedance/deer-flow/blob/main/backend/docs/CONFIGURATION.md

## GATE A — tokens / costos
**Observado:** ~42.1K input para Gemini en chat previo; ~10.5K input Luna primera etapa R2, ~49.6K tokens acumulados visibles tras continuar R2. No comparar totales de hilo con una sola llamada. No extrapolar US$ de contadores UI.
**Ya activo:** `skills.deferred_discovery=true`; `token_budget.enabled=true`, `max_tokens=50000`, `max_input_tokens=45000`, `max_output_tokens=5000`; `token_usage.enabled` documentado. `tool_search.enabled=false` según plantilla — habilitar solo cuando exista inventario MCP y un A/B que lo justifique.
**Pendiente instrumentar:** por ejecución y modelo, número de llamadas, input uncached/cache hit, output, costo API, tamaño fijo de system/tools, tamaño de historial, reintentos; guardar recibo sin prompts/credenciales. Se puede extraer usage_metadata de la infraestructura existente sin crear una segunda medida ficticia.
**Política de cierre experimental (no afirmación de pass):**
- Parar si el primer llamado de una misión pequeña trae >12K input; identificar componente dominante y reducirlo antes de continuar.
- Parar si la misión pequeña acumula >30K tokens o la estimación API supera US$0.20. Estos son límites propuestos de aceptación, **no controles ya implementados**.
- No encadenar reintentos 400 ni modelos alternos sin clasificación; controlar recarga automática de OpenAI Platform desde el panel.
- Comparar dos misiones idénticas recién creadas en Luna/Gemini, con el mismo conjunto de tools, considerando tokens de llamada vs acumulados y calidad de entregable.
- Gate A solo PASS cuando hay dos ejecuciones independientes con métricas por llamada y costo, resultados útiles, sin sobrepasar límites.

## GATE B — Codex Cloud / trabajo real
- **Elegido para automatizar:** OpenAI Agents API, que administra la sesión/harness Codex y puede alojar sandbox de ejecución; requiere credencial API del proyecto **sin compartirla en chat o GitHub**, derechos y costos de contenedores. Sesión creada y prueba real con shell, código, tests, artifacts, reanudación y usage. Si falla elegibilidad/permisos, no inventar integración.
- **ChatGPT Codex Cloud:** usar un entorno publicado conectado al fork para tareas humanas o fallback, con Git como artefacto; no confundir sus cuotas del plan con uso de Agents API. No hay todavía puente de llamada automáticamente desde DeerFlow al Codex Cloud del plan.
- **ACP CLI:** ruta de respaldo para ejecución local si el sandbox aislado puede iniciar Codex; no montar Docker socket en Gateway, no convertir `allow_host_bash` a true por atajo.
- Gate B PASS: sesión remota ejecuta una prueba, conserva resultado/commit/sha, puede retomarse y reporta costo.

## GATE C — cadena autónoma
1. Lead recibe JSON de trabajo (id, objetivo, reglas de folio, límites, repo scratch).
2. Dispatcher idempotente crea/retoma work_id y selección de worker.
3. Worker Codex (Agents API) lee solo rama del experimento, escribe código, corre tests en sandbox, produce test-log.
4. Publica rama Git con commit SHA y recibo de resultados.
5. Claude revisa **el commit exacto** y comenta en PR; **no reemplaza un fallo de tests por redacción**.
6. CI verifica tests sin secretos; reporte PASS/FAIL.
7. Solo con PASS y autorización humana se propone merge. Ningún deploy.
8. Si 400/401/403/permiso/validación: BLOCKED sin retries. Si 429/5xx transitorios: retry acotado y registrar costo; no fallback ciego. Si falta contexto: contrato explícito, no solicitar specs ya proporcionadas.
9. Reanudar desde Git + work_id + hashes, no desde otra conversación completa.

### Contrato de recibo obligatorio
```json
{"work_id":"umbral-r2-001","provider":"agents-api","session_id":"...",
 "branch":"experiment/...","commit_sha":"...", "artifact_sha256":"...",
 "tests":{"command":"python -m unittest","passed":5,"failed":0},
 "usage":{"input":0,"cached":0,"output":0,"usd_estimate":0},
 "review":{"agent":"claude","revision_sha":"...","decision":"APPROVE|CHANGES"},
 "status":"PASS|FAIL|BLOCKED","next_action":"..."}
```
Campos `...` son forma de contrato, no datos reales. No fabricar recibos.

## Ejecución ya creada en esta rama
- `ops/umbral/r2/verify_r2.py`: localiza los DOS archivos originales de R2 en el runtime de DeerFlow, valida identidad/sha256 y ejecuta los tests **dentro de Docker descartable** con network=none, read-only, sin secretos ni privilegios. No ejecuta en Gateway y no inventa nuevos archivos.
- `ops/umbral/r2/test_verify_r2.py`: pruebas offline del verificador, sin costos de modelo.
- `.github/workflows/umbral-r2-verifier.yml`: CI mínimo para herramienta.
- `backend/tests/test_umbral_managed_gpt6_responses.py`: regresión del parche Responses.
Resultado de UNIT tests del verificador ejecutados fuera de repo, 5/5 PASS. **No es el 5/5 del código generado por Luna**. Pendiente el reporte de ejecución en Codespaces sobre los archivos originales.

### Cómo ejecutar verificación real en el Codespace (sin desproteger Gateway)
En checkout con esta rama:
```sh
python3 ops/umbral/r2/verify_r2.py --repo /workspaces/deer-flow
```
Si hay más de una carpeta, usar `--path` al original. Puede requerir obtener la imagen `python:3.12-slim` inicialmente; esa descarga ocurre antes del runner network=none y no implica acceso de test a Internet.

## Estado y NO HECHOS
- `R2_FILE_WRITE_READ=PASS` según captura.
- `R2_TEST_EXECUTION=NO` hasta ejecutar verificador en el Codespace.
- `GATE_A=FAIL_UNCLOSED`
- `GATE_B=BLOCKED_NOT_CONNECTED`
- `GATE_C=BLOCKED_NOT_AUTOMATED`
- `CODEX_CHATGPT_ADAPTER=HTTP_400_FULL_HARNESS` sin causa aislada.
- `OPENAI_MANAGED_GPT6_RESPONSES_PATCH=LOCAL_VALIDATION_PASS` + push a fork, no test automatizado todavía.
No considerar la documentación, GitHub issue o PR como ejecución Cloud exitosa.

## División de responsabilidades
**Arquitectura (asistente):** contratos, rutas, pruebas, auditoría, commits, clasificación de fallos.
**Servicios:** sandbox y runners ejecutan tests; GitHub conserva activos; proveedores facturan/ejecutan dentro del acceso autorizado.
**Operador:** solo aprobación de gasto, permisos Cloud y merge/proyecto. No copiado manual de contexto.

## Actualización técnica — 2026-11-03
La rama también incluye:
- `ops/umbral/r2/token_audit.py`: extrae del Gateway las líneas existentes `LLM token usage` por llamada; no imprime logs crudos ni hace llamadas API. No atribuye modelos sin trace_id y no confunde métricas con facturación. Corrida real en Codespaces todavía pendiente.
- `ops/umbral/r2/cloud_smoke.py`: prueba programática con SDK oficial `client.beta.agents.sessions.create(..., environment={"type":"openai_hosted"})`. Solo envía API con `--execute`, requiere `OPENAI_API_KEY` de un proyecto con permisos `api.agents.read/write`, `api.responses.write`; descarga ZIP publicado con ruta contractual y calcula SHA-256. Un ZIP descargado tampoco prueba por sí solo que los tests se ejecutaron sin revisar el registro, por eso su resultado es parcial.
- Tests sin red para los dos módulos, incorporados al flujo CI de esta rama.
**No se ha autorizado ni ejecutado llamada Agents API, no se ha conectado ChatGPT-plan Codex Cloud y no hay promesa de límite de costo duro.**

Comandos de inspección, **sin gasto API** (desde checkout de la rama):
```sh
python3 ops/umbral/r2/token_audit.py --since 60m
python3 ops/umbral/r2/cloud_smoke.py
```
Comandos con efectos requieren aprobación humana previa. El verificador R2 puede ejecutar Python generado por modelo, pero solo dentro de Docker con filesystem de código read-only, sin red y sin privilegios.
