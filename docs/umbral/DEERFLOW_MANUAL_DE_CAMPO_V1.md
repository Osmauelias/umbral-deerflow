# UMBRAL · Manual de campo DeerFlow (v1)
**Fecha:** 2026-11-03  
**Responsable funcional:** DEERFLOW_FIELD_DIRECTOR (manual operativo, no agente automáticamente ejecutable)  
**Mandato:** decidir en pruebas si DeerFlow nos sirve, mostrar cómo se usa, cuánto cuesta y cómo entregar trabajo real.  
**Regla madre:** una respuesta bonita no es un activo; un archivo en la mesa sin commit tampoco.  
**Estado:** MANUAL PUBLICADO, CADENA MULTIAGENTE AUTOMÁTICA NO CONECTADA.

## 0. Decide primero si sirve (semáforo)
| Pregunta | Evidencia actual | Gate para continuar |
|---|---|---|
| ¿Accede a modelos? | Gemini respondió; la API OpenAI recibió parche de Responses; Codex OAuth directo respondió, pero el chat de DeerFlow arrojó HTTP 400. | Luna/Sol responden en la UI después del parche, sin 400. |
| ¿Usa herramientas? | Luna utilizó `write_file` y `read_file` en R2. | Verificar recepción de archivos y hashes. |
| ¿Ejecuta pruebas? | NO: `sandbox.allow_host_bash=false` y el agente reportó herramienta de ejecución no disponible. | Un ejecutor *aislado* ejecuta los cinco tests existentes; recibo + exit code. |
| ¿Hace relevo entre agentes? | R1 retuvo contexto conversacional; NO hubo relevo autónomo durable. | Agente B lee un commit del agente A SIN copiar mensajes; entrega su propio commit/PR. |
| ¿Controla costo? | R2 Luna inició con 10.5K input; captura posterior 49.6K tokens acumulados del hilo. `token_budget: 50000` por run. | Ledger por tarea y modelo; coste total y actos humanos medidos, no inferidos del contador. |
| ¿Conecta Codex Cloud? | NO. Tener Codex en selector de modelos ≠ worker Cloud. | Una tarea Cloud/ACP/Agents API que haga commit con recibo verificable. |

**Decisión provisional: EXPERIMENTO CONDICIONADO, no plataforma adoptada.** Si un flujo nativo Codex Cloud/Agents API → GitHub → CI hace lo mismo con menos operación, DeerFlow no cobra renta y se descarta del camino principal.

## 1. Mapa de controles: qué botón hace QUÉ
**Nivel 0 / Empezar** — DeerFlow Workspace → **Settings / Models**. Registrar un proveedor y prueba de respuesta. Esto sólo da un cerebro; no programa. Para OpenAI GPT-6, el *backend* debe emplear `/v1/responses`, no Chat Completions con tools + reasoning. La reparación del preset managed se guardó en rama `fix/managed-gpt6-responses-20261103` commit `34b124954`; evidencia de carga `RESPONSES_OK`, todavía requiere smoke de UI en el reporte de turno.

**Nivel 1 / Capacidades** — **Capability Center**. Skills = instrucciones/recetas que el modelo puede descubrir, NO permisos para ejecutar. Configuración observada: 23 skills Enabled; `skills.deferred_discovery=true` para reducir carga del prompt. Verificar si en una tarea se invoca realmente una skill (nombre, resultado). No habilitar las 23 para todas las tareas si aumentan el contexto sin utilidad.

**Nivel 2 / Herramientas** — `config.yaml > tools`: lectura (`ls`, `read_file`, `glob`, `grep`), escritura (`write_file`, `str_replace`), `bash` definido pero puede NO estar expuesto sin sandbox adecuado. R2 demostró escritura y lectura; NO ejecución.

**Nivel 3 / Taller de ejecución** — `config.yaml > sandbox`. Local: corre en el contenedor Gateway y `allow_host_bash=false` debe permanecer así en prueba de bajo riesgo: Gateway también ve credenciales y config. AIO requiere montaje Docker socket (riesgo host root, revisar seguridad); alternativas: sandbox remoto o runner efímero CI/GitHub Actions para tests; **la opción inicial es runner efímero sin shell de modelo** que prueba los archivos originales, sin socket expuesto al agente.

**Nivel 4 / Trabajadores** — `subagents` = delegaciones propias del harness, `acp_agents` = procesos externos compatibles ACP (ej. Codex CLI a través de adaptador) dentro del Gateway, NO solo instalado en host. `Agents API` de OpenAI = Codex harness administrado y ejecución en sandbox (otro producto, facturación API). `Codex Cloud` de ChatGPT = entorno de tareas con GitHub/plan (otro producto). **No asumir que están conectados por listar un modelo.** Estado reportado: `acp_agents=[]`, `agents_api.enabled=false`.

**Nivel 5 / Relevo durable** — GitHub ramas/PR y CI, no historia del chat ni filesystem de cada sesión.

## 2. Arquitectura aprobada para probar, no declarada implementada
```text
OPERADOR: define resultado, presupuesto, restricciones, aprobación de merge
       |
       v
COLA / MANIFIESTO EN GIT (RUN_ID, issue, repo, rama, presupuesto, acceptance)
       |
       v
AGENTE A / MESA EFÍMERA: checkout limpio -> implementa -> tests locales
       |  escribe commit y PUSH en rama protegida de experimento
       v
GITHUB / ÚNICA FUENTE DE VERDAD:
  código + pruebas + MANIFEST + recibo (hashes, test exit, commit, modelo/tokens)
       |
       v
CI INDEPENDIENTE: ejecuta tests sin secretos y registra PASS/FAIL
       |
       v
AGENTE B / MESA NUEVA: lee commit verificado A -> revisa/refactoriza
       |  nuevo commit/PR + evidencia; NO copiar chat A
       v
HUMAN PASS: revisión/coste/seguridad -> merge o rechazo
       |
       v
CLEANUP: destruir mesas/sesiones; Git conserva la capacidad de reconstruir
```
**Límites:** dos agentes jamás hacen push concurrente a `main`. Cada uno usa rama identificada; se evita overwrite/force-push y se exige CI y autorización humana para acciones productivas. Para archivos grandes/binarios: object storage o Drive con checksum; Git guarda manifiesto y referencia, nunca credenciales.

La conversación de cada agente puede ser temporal; el **orquestador sí necesita estado mínimo** (`run_id`, fase, commit SHA, PR URL, idempotencia, permisos, presupuesto) para recuperarse sin duplicar trabajo. No necesita volcar el pensamiento ni chats completos.

## 3. Tutorial tipo videojuego: del nivel 0 al 5
**Regla:** no pasar al siguiente nivel sin el trofeo verificable anterior. Una sola prueba por gate.

**Nivel 0 — ¿Qué ya funciona? (congelar):** selector tiene modelos, Gateway reiniciado y parche Responses versionado. No más test `OK` salvo regresión. Trofeo: evidencia previa.

**Nivel 1 — Archivo real (PASS parcial ya conseguido):** Luna creó y leyó `/mnt/user-data/workspace/prueba_r2_normalizar_folio/normalizar_folio.py` y `test_normalizar_folio.py`. R2 confirmó dos archivos + 5 pruebas presentes, NO ejecutadas. Trofeo: captura y rutas.

**Nivel 2 — Ejecutar originales SIN dar shell al agente:** el script `ops/umbral/r2/verify_r2.py` busca los archivos reales en el runtime de DeerFlow, o acepta `--path`, obtiene SHA-256 y llama a un contenedor efímero de Python sin red, con filesystem read-only, sin privilegios y con límite CPU/memoria, para `unittest discover`. Requiere Docker **en el host Codespaces**, no en el agente. Si no está disponible o no encuentra los archivos: `BLOCKED`, NO simular. Ejecutar desde un checkout de esta rama:
```bash
python3 ops/umbral/r2/verify_r2.py --repo . --dry-run
python3 ops/umbral/r2/verify_r2.py --repo . --receipt /tmp/umbral_r2_receipt.json
```
Advertencia: si Git está en `/workspaces/deer-flow` y la ruta de runtime de DeerFlow es un volumen Docker no montado en el host, el script requiere `--path` al directorio original visible en Codespaces. NO crear archivos sucedáneos para hacer pasar la prueba. No publicar automáticamente el recibo si contiene rutas privadas; redactar y guardar solo SHA/exit code cuando corresponda.

**Nivel 3 — Commit fuente:** transferir artefactos R2 a rama experimental sin secretos; registrar `source_commit`, hashes, stdout de pruebas y `cost_ledger`. Trofeo: URL de commit y CI.

**Nivel 4 — Segunda mesa:** actor B parte de checkout LIMPIO del commit A, lee `MISSION.json` + `RECEIPT.json`, cambia solo un aspecto y entrega su commit, nueva evidencia. No se le pega conversación A. Trofeo: dos commits/autoría diferenciada y diff B.

**Nivel 5 — Orquestación automática:** un runner determinista observa CI PASS y despacha siguiente actor con límites, confirma que toma el commit esperado, evita duplicados, detiene en FAIL, solicita Human Pass para merge. Si no hay disparo real ni recibo, NO declarar cadena autónoma.

## 4. Tres caminos de Codex; no mezclar
| Camino | Qué hace / mesa | Cómo se conecta | Costo principal | ¿Conectado? |
|---|---|---|---|---|
| **Codex Cloud ChatGPT** | Tareas aisladas en máquinas administradas, repos de GitHub, conserva tareas; cada tarea nuevo espacio | Configurar entorno publicado en Codex web/desktop + GitHub. Un nuevo task no hereda cambios sin commit. | Cupo/credits del plan Codex; entornos estándar sin VM extra en lanzamiento | NO verificado con repo Umbral |
| **Codex CLI / ACP** | Worker externo que DeerFlow puede invocar si CLI + adaptador ACP + autenticación están disponibles EN el Gateway | `acp_agents` con `command`, `args`, permisos acotados; Codex ACP adapter `@zed-industries/codex-acp`; probar escritura+commit real. | Cupos Codex de cuenta o facturación por uso según autenticación/plan | NO conectado |
| **OpenAI Agents API** | Harness de Codex administrado; crea sesiones, herramientas y sandbox; se integra mediante una capa/servicio orquestador propio | API key con `api.agents.read/write` y `api.responses.write`; OpenAI-hosted sandbox o propio, GitHub/PR vía tools aprobadas | Tokens a precio API + contenedores + herramientas | NO conectado |

**Preferencia de experimento:** comparar **Agents API → GitHub → CI** contra DeerFlow+ACP sólo si la arquitectura del segundo demuestra menor costo/carga. No añadir los dos simultáneamente. No usar Custom ChatGPT CodexChatModel viejo para dirigir una cadena crítica mientras su UI arroje 400.

## 5. Costos: números, no humo (USD; precios verificados 2026-11-03)
| Componente | Tarifa referencial | Contabilidad |
|---|---|---|
| GPT-6 Luna API estándar | entrada $0.10/M, salida $0.50/M (cache hit entrada $0.01/M) | Input uncached × 0.10/1M + cached × 0.01/1M + output × 0.50/1M |
| GPT-6.1 Sol API estándar | entrada $2.00/M, salida $10.00/M (cache hit entrada $0.10/M) | Misma fórmula |
| Claude Sonnet 5.5 API | entrada $2.00/M, salida $10.00/M | Puede tener ajustes por caching/batch |
| OpenAI-hosted sandbox pequeño | contenedor 1GB $0.03/20 min (mínimo y esquema vigentes según pricing) | Adicional a tokens; verificar la factura real |
| GitHub Codespaces | 2-core $0.18/hr; 4-core $0.36/hr; storage $0.07/GB-mes fuera de cuota | Factura distinta; gratis según tipo de cuenta/cuota |
| Codex Cloud con ChatGPT | uso de cuota/créditos Codex del plan; no confundir con $5 comprados para OpenAI API | No inventar equivalencia en USD por tarea |
| DeerFlow (software del fork) | no tarifa SaaS propia por el código | La infraestructura, tokens, contenedores y tiempo del operador sí cuestan |

**Ejemplos exclusivamente aritméticos:** Luna 10,500 input y 417 output, todo uncached → ~$0.00126 (sin servicios/tool extras). Un hilo de ~50,000 input + 500 output Luna → ~$0.00525; Sol → ~$0.105. No son cargos confirmados: el contador 49.6K de R2 es acumulado, incluye posibles llamadas y caché, no equivale al consumo facturado de una sola petición.

**Estimar correctamente**: `US$ real/activo aceptado = (todos los tokens + tool fees + contenedores + Codespaces facturable + reintentos fallidos) / activos que pasaron CI y Human Pass`. Añadir **minutos de intervención humana** como segunda métrica. No mezclar USD con tokens sin precio ni comparar entradas de distintas tareas.

**Fusible del piloto**: presupuesto económico experimental por tarea US$0.25 estimado en API, **no es tope garantizado del proveedor**; detener nuevas llamadas al superarlo, máximo 2 intentos por fase, 1 agente inicial y 1 revisor. `token_budget: 50000` limita una ejecución *a posteriori*, NO una primera llamada gigante ni facturación total del hilo. Revisar estado de auto-recarga y presupuestos en Platform.

## 6. Token audit (no desactivar seguridad para ahorrar contexto)
1. Toma **un mismo prompt** en hilos NUEVOS; una llamada por modelo.
2. Anota: model ID, `input_tokens`, `cached_input`, `output_tokens`, total per-call, prompts system/skills/tools incluidos, precio y latencia. No pegar claves o prompt completo con secretos.
3. Variar SOLO UNA condición entre muestras: `skills.deferred_discovery` / `tool_search.enabled` / lista herramientas / historial.
4. El cuadro de DeerFlow muestra total acumulado del hilo; R2 Luna mostró inicialmente 10.9K total y más tarde 49.6K total. No inferir gasto directo de esos números.
5. Gate de ingeniería: tarea micro con un máximo objetivo de 15K input por primera llamada; si supera 25K sin justificación, revisar ensamblado antes de agregar workers. Es meta de diseño, no garantía. Coste por activo y operador son los árbitros.

## 7. Matriz de permisos y protección del operador
- GitHub: por agente, ramas `experiment/<run-id>/<role>`, PR obligatorio, cero `push main`, `force push` prohibido, proteger secretos. Flujo `read-only` para auditorías y `write` scoped para implementadores.
- Codex Cloud: acceso al repo seleccionado y su env de ejecución, no asumir escritura por conexión.
- ACP/DeerFlow: `auto_approve_permissions=false` inicialmente. Docker socket no se monta en Gateway por default por ser acceso root equivalente.
- Sandboxes: no dar host bash al Gateway con credenciales. CI sobre commits acotados o sandbox remoto con red limitada.
- Repeticiones: error 400 ⇒ detener, capturar código y error redactado, corregir compatibilidad demostrada, UNA retest. No reintentar 10 veces.
- Dosis máxima de operador: 1 pantalla de instrucciones, 1 acción humana, 1 resultado binario por gate.

## 8. Veredicto y regla de salida
**Continuar 1 piloto únicamente si**: (a) nivel 2 ejecuta tests originales, (b) git registra commit + CI, (c) segundo worker consume A desde Git sin copiar chat, (d) se entrega costo total, (e) ninguna credencial filtrada ni acción productiva ejecutada. Si falla o requiere al operador hacer de mensajero, **descartar DeerFlow como orquestador principal** y probar Agents API + CI directamente.

## Fuentes del código / manual original
- [README del fork](../../README.md) (setup wizard, herramientas, modelos y ACP).
- [Configuración técnica](../../backend/docs/CONFIGURATION.md) (sandbox, permisos, subagentes, skills).
- [Plantilla de configuración](../../config.example.yaml) (tools, deferred skills, budget).
- [Skill UX](../../docs/skill-usage-ui.md) (experiencia de uso de skills).
- [Verify R2](../../ops/umbral/r2/verify_r2.py) (runner diseñado, falta ejecución live y CI).
- [OpenAI Codex Cloud](https://help.openai.com/en/articles/20001545-using-codex-cloud).
- [OpenAI Codex ChatGPT allowance](https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan).
- [OpenAI Agents API](https://developers.openai.com/api/docs/guides/agents-api/overview) y [Quickstart](https://developers.openai.com/api/docs/guides/agents-api/quickstart).
- [Precios OpenAI API y contenedores](https://developers.openai.com/api/docs/pricing).
- [Anthropic precios](https://platform.claude.com/docs/en/about-claude/pricing).
- [GitHub Codespaces facturación](https://github.com/github/docs/blob/main/content/billing/concepts/product-billing/github-codespaces.md).

## VEREDICTO
**Qué hacemos:** cerrar nivel 2 de R2 con ejecución segura de archivos existentes, luego dos commits + CI antes de volver a añadir proveedores.  
**Quién:** director DeerFlow prepara arquitectura/código/recibo; actores de IA hacen sus propios commits cuando haya executor real; operador autoriza gastar y merge.  
**Cuándo:** próximo bloque de ejecución, no seguimiento automático inventado.  
**Cómo sabemos si funcionó:** `TESTS_PASS` + commit A + CI PASS + commit B + gasto medido + operador intervino una vez.
