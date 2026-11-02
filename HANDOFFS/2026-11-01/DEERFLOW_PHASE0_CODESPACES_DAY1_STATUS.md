# DEERFLOW PHASE 0 — CODESPACES DAY-1 HANDOFF
**Fecha:** 2026-11-01
**Misión:** DEERFLOW_CLOUD_CONTINUITY_ENGINEER
**Autoridad humana:** Osvaldo
**Estado:** `PHASE_0_PARTIAL / FIRST_BOOT_PASS / ADMIN_AUTH_BLOCKED`
**Naturaleza:** reporte de ejecución, no promoción de herramienta ni autorización de producto.

## Resultado comprobado
- Fork propio: `Osmauelias/umbral-deerflow` (código heredado de `bytedance/deer-flow`, MIT). Git remoto del Codespace cambiado a fork; el Codespace fue creado originalmente desde upstream.
- Ambiente remoto: GitHub Codespaces `crispy-funicular`, Linux, Docker y Docker Compose. Máquina de 4 vCPU / ~15 GiB de RAM; capacidad suficiente sólo para experimento, no validada como producción.
- `make config` generó archivos locales ignorados por Git; `sandbox_mode=local` verificado. Local significa que la ejecución de herramientas comparte el entorno del proceso dentro del Codespace, **no sandbox aislado por worker**.
- `make docker-init` confirmó Docker listo sin imagen AIO adicional. `make docker-start` construyó interfaz y gateway y arrancó el stack de desarrollo. Frontend de DeerFlow visible por navegador, puerto 2026 de Codespaces marcado `Private`.
- Configuración de `GATEWAY_CORS_ORIGINS` con el HTTPS exacto del puerto Codespaces, escrita en `.env` y verificada **dentro** de `deer-flow-gateway` tras recrearlo. No copiar aquí valores de configuración sensibles.
- Una prueba controlada POST `/api/v1/auth/initialize` con Origin autorizado y cuerpo vacío produjo `HTTP 422`: llegó a validación de payload sin bloqueo de origen para **esa solicitud**.

## Bloqueo vigente
- Chrome aún muestra `Cross-site auth request denied.` al intentar crear la cuenta administrativa. Registro admin **NO verificado**; workspace funcional **NO verificado**.
- Diferencia entre solicitud real del navegador y prueba controlada **todavía no diagnosticada**. Siguiente paso: Chrome DevTools → Network → petición `initialize` → examinar únicamente `Origin`, `Host`, `X-Forwarded-Proto` si son visibles y código de estado (sin contraseñas, cookies, payload ni tokens). Diagnosticar antes de modificar proxies.
- No conectados modelos externos, APIs privadas, GitHub tokens de agentes ni repos productivos. No hay prueba de workers A→B, PR, preview de producto ni costo real medido.
- La persistencia durable de archivos `config.yaml`/`.env` no está resuelta: son locales e ignorados por Git. Sólo alias y procedimientos deben quedar durables; secretos nunca en Git.
- Docker usa cuota de cómputo/almacenamiento de Codespaces. Gasto extra no autorizado; revisar uso/cuota y detener Codespace al cerrar.

## Próximo trabajo autorizado — sin scope creep
1. Resolver auth browser con CSRF intacto, puerto `Private` y sin exponer URLs, tokens ni secretos.
2. Verificar acceso al Workspace, salud de los cuatro servicios y reproducción de instalación desde GitHub + configuración no secreta.
3. Evaluar modelo económico/control de costos, aislamiento por trabajador y respaldo/continuidad antes de cualquier agente con capacidad de escritura.
4. Sólo con **Phase 0 PASS** y alcance acotado, iniciar **Phase 1: experiencia pública landing AIDOH** en `Osmauelias/Umbral-AIDOH`, rama aislada y Human Pass. **Cafetería MVP-003 no se toca**.
5. **Phase 2 Frankenstein V2 BLOQUEADA** hasta Phase 1 PASS + `UNLOCK PHASE 2` explícito; V1, runtime y recovery intocables.

## Hipótesis y métrica humana
`DEERFLOW = HARNESS`; `GITHUB = VERDAD DURABLE`; `MODELS = WORKERS SUSTITUIBLES`.
Hipótesis por probar: un operador puede dirigir por interfaz web, sin consola Linux cotidiana, un relevo entre trabajadores/modelos que deja commit, PR, test y vista previa recuperables desde GitHub. Todavía **NO demostrado**.
No volver la herramienta infraestructura obligatoria por lograr arrancar Docker.

## Entrega institucional
Destinatarios: Cerebro (arquitectura/gates), Torre de Control (observabilidad y prioridades, sólo lectura), Oficialía/Documentador (provenance).
Fuente de autoridad: `Osmauelias/umbral-documentador/issues/19` y `SPECS/DEERFLOW_CLOUD_CONTINUITY_EXPERIMENT_V1.md`.
`POSTED != READ/ACK` · `TECHNICAL_BOOT_PASS != WORKER_PASS != HUMAN_PASS`.

## VEREDICTO
**Qué:** continuar Fase 0 sólo para diagnosticar autenticación y validar Workspace.
**Quién:** hijo DeerFlow, bajo dirección de Osvaldo; Cerebro revisa diseño, Torre sólo observa.
**Cuándo:** siguiente sesión, sin ejecución en segundo plano.
**Criterio:** admin autenticado, Workspace operativo, control de seguridad/costo; Phase 1 permanece bloqueada hasta entonces.
