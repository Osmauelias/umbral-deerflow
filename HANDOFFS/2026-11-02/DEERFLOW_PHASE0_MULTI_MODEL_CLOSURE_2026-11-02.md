# HANDOFF — DEERFLOW CLOUD — MODELOS CONECTADOS / CIERRE DE JORNADA
**Fecha operativa (México):** 2026-11-02  
**Owner:** DEERFLOW_CLOUD_CONTINUITY_ENGINEER  
**Autoridad humana:** Osvaldo  
**Estado:** `PHASE0_WORKSPACE_PASS / FIVE_MODELS_CHAT_REPORTED_PASS / SAFETY_CONTINUITY_PENDING / HUMAN_PAUSE`  
**Naturaleza:** evidencia y relevo técnico, NO cierre integral de Fase 0 ni autorización de producto.

## Qué cambió respecto al handoff 2026-11-01
1. **Autenticación de administrador y Workspace**: el bloqueo `Cross-site auth request denied` (403) dejó de aparecer después de autorizar temporalmente el origen HTTPS del puerto privado Codespaces y `http://localhost:2026` y recrear únicamente gateway. Chrome mostró `initialize` HTTP 201 seguido de 409 por reintento; posteriormente se abrió `/workspace/chats/new`. **Hipótesis**: reescritura/intermediación de Origin; aún NO comprobada en el backend. La excepción loopback debe auditarse y minimizarse, conservando CSRF.
2. **Modelos registrados en la interfaz**:
   - Meta Muse Spark: `muse-spark-1.3`, proveedor personalizado compatible.
   - Google Gemini Flash-Lite: `gemini-3.5-flash-lite`, proveedor personalizado compatible.
   - xAI Grok: `grok-build-0.1`, proveedor personalizado compatible.
   - Anthropic Claude: `claude-sonnet-5-5`, proveedor Anthropic; falló un `Test connection` previo, pero **Osvaldo confirmó posteriormente que contestó desde DeerFlow**. Se compraron US$5 de créditos Anthropic por decisión del operador.
   - OpenAI Codex mediante login de ChatGPT: `Codex — ChatGPT Plus`, adaptador `deerflow.models.openai_codex_provider:CodexChatModel`, registrado en `config.yaml` como `codex-chatgpt`. Inicialmente `gpt-5.4` devolvió HTTP 400 desde DeerFlow; se sustituyó por `gpt-6.1-sol`, se recreó gateway y **Osvaldo confirmó respuesta «CODEX CONECTADO»**. Causa exacta del 400 no demostrada únicamente por el cambio de modelo.
3. **Herramientas CLI** instaladas en host Codespaces: `@openai/codex` y Claude Code 2.1.316. `codex login --device-auth` devolvió `Successfully logged in`. El gateway confirmó lectura del archivo de auth Codex mediante `CODEX_MOUNT_OK` sin imprimir el secreto. Esta integración **no equivale a instalación de Codex CLI dentro del contenedor**.
4. **Evidencia de conversación**: Meta/Gemini/Grok dieron respuestas básicas; Codex y Claude confirmados por el operador como conectados. **`BASIC_CHAT_RESPONSE != TOOLS_WORKING != SUBAGENT_WORKING != PRODUCTION_READY`**. Ejemplo Gemini consumió ~67.2K tokens de entrada para una petición breve: pendiente evaluar costo/contexto por tarea, sin extrapolar.
5. **Jerarquía deseada por Osvaldo**: rol director/modelo de mayor capacidad (OpenAI SOL en programación), rol operador/modelo más económico suficiente (OpenAI LUNA), autoridad humana final. Aplicar principio equivalente a Claude y otros proveedores si sus capacidades/modelos lo permiten. **Es diseño propuesto, NO jerarquía implementada.**

## Decisión humana de cierre de jornada
- **STOP por hoy** para proteger sueño/operador. No continuar trabajos ni pruebas en segundo plano.
- Próxima sesión: asegurar/documentar y revalidar conexión Claude/Codex solamente si es necesario; **antes de configurar jerarquías, inventariar en vivo TODAS las capacidades de DeerFlow**: Capability Center, skills instaladas/desactivadas, herramientas, subagentes, web/browser, programación, archivos y artefactos, investigación, imágenes/video/audio/presentaciones, conectores/MCP, Projects, Scheduled tasks, costos, permisos y seguridad.
- Presentar comparación contra harness convencional. Criterio de supervivencia: capacidad incremental demostrable, costos y carga del operador. Si sólo ofrece selector multi-modelo, no justificar infraestructura adicional.
- Luego decidir qué activar y definir director/operador por tareas, sin cinco directores simultáneos.

## Riesgos y pendientes de Fase 0
- **Continuidad**: `config.yaml`, `.env`, credenciales y el catálogo cifrado de modelos viven en estado local ignorado por Git. Configuración de Codex usa overlay temporal `/tmp/deerflow-codex-only.yaml`; no asumir portabilidad ni recuperación. No respaldar secretos en GitHub.
- **Seguridad**: revisar excepción CSRF/CORS `http://localhost:2026` añadida para el proxy; confirmar cabeceras/backend antes de eliminarla o mantenerla. El puerto de Codespaces se mantiene `Private`.
- **Modelo/sesión**: no afirmar persistencia de OAuth tras reinicios prolongados ni acceso garantizado a cualquier modelo; revisar caducidad y límites con pruebas acotadas.
- **Infraestructura**: Codespaces dev, sandbox local, aislamiento por trabajador no verificado; sin ejecución productiva, sin publicación, sin cambios a repos de producto.
- **Costo**: usuario reportó compra US$5 Anthropic; Meta/Gemini/xAI con facturación propia. No asumir costo cero de ChatGPT/CLI ni gasto nulo de Codex en límites de plan; revisar consumo por tarea.
- **Funcionalidad**: `Agents` mostraba `Feature not enabled`; herramientas y skills no auditadas. La aplicación se ha probado principalmente como chat. Ninguna prueba de handoff entre workers, branch/PR/preview ni Human Pass de activo.
- **Repos protegidos**: Cafetería MVP-003, Frankenstein V1/V2, Booking, Torre, Vía Hábitat, PAO siguen sin tocarse. Fase 1 landing AIDOH NO iniciada. Fase 2 Frankenstein V2 permanece BLOQUEADA hasta Phase 1 PASS y desbloqueo explícito.

## Evidencia y provenance
- Handoff previo: [2026-11-01 — Codespaces Day-1](../2026-11-01/DEERFLOW_PHASE0_CODESPACES_DAY1_STATUS.md).
- Investigación/repo: `Osmauelias/umbral-deerflow` y definición institucional `Osmauelias/umbral-documentador/issues/19`.
- Resultados terminal suministrados por Osvaldo: `CODEX_AUTH_OK`, `CODEX_MOUNT_OK`, `CODEX_MODEL_UPDATED: gpt-6.1-sol`, `deer-flow-gateway Started`; captura del selector con los cinco modelos; confirmación explícita de chat `CODEX CONECTADO` y Claude conectado.
- Evidencia es de la sesión guiada por navegador/Codespaces y reportes humanos; sin diagnóstico exhaustivo de seguridad ni instrumentación de costos.

## RELEVO
`NEXT_SESSION_GATE_1 = CAPABILITY_AUDIT_BEFORE_HIERARCHY`  
`PHASE_0 = PARTIAL_ADVANCED`  
`FIVE_MODELS = REGISTERED_AND_BASIC_RESPONSES_REPORTED`  
`WORKER_TEST = NOT_RUN`  
`HUMAN_PASS = NOT_GRANTED`  
`PHASE_1 = NOT_STARTED`  
`PHASE_2 = LOCKED`  
`OSVALDO_ACTION_REQUIRED = NONE_TONIGHT`  
`PORTFOLIO_ATTENTION_REQUIRED = NO_PRIORITY_CHANGE`

## VEREDICTO
**Qué:** registrar y congelar avances del experimento; auditoría de capacidades antes de configurar jerarquías.  
**Quién:** hijo DeerFlow, con Documentador/Oficialía y ULM en custodia de evidencia y aprendizaje.  
**Cuándo:** siguiente sesión sólo por activación humana.  
**Métrica:** capacidades reales verificadas, requisitos/costos/permisos y comparación frente al harness; no sólo un chat con cinco modelos.
