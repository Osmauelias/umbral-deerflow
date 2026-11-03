# DEERFLOW C0 — ERROR DE INDENTACIÓN EN CONFIG — 2026-11-03
**Estado:** ERROR OBSERVADO / CORRECCIÓN INDICADA / VALIDACIÓN DE REINICIO PENDIENTE

## Síntoma
El usuario ejecutó una validación PyYAML de `/app/project/config.yaml`. Resultado:
`yaml.parser.ParserError`: while parsing a block mapping at line 2174 col 3, unexpected mapping start line 2181 col 4.

## Causa probable sustentada
El archivo mostraba `   deferred_discovery: true` (3 espacios) bajo el bloque `skills`. La plantilla upstream `config.example.yaml` usa `  deferred_discovery: true` (2 espacios). YAML exige sangría consistente.

## Contexto previo
- `token_budget` pasó de dos bloques a uno; config textual final: enabled true, max_tokens 50000, max_input_tokens 45000, max_output_tokens 5000, thresholds .8/1.0.
- `CODEX_MOUNT_PRESENTE` confirmado por inspección de destinos de Docker; overlay de Compose en /tmp faltaba, pero no se pretendió recrear contenedor.
- El reinicio anterior era condicional con `&&`; el ParserError se produjo primero, por lo que no hay evidencia de que se reiniciara.
- **NO DECLARAR RESTART_PASS NI C0_COST_PASS** hasta recibir salida nueva.

## Corrección proporcionada
Respaldar local `config.yaml` bajo /tmp, convertir exactamente `^   deferred_discovery: true$` a `  deferred_discovery: true`; validar parseo y los tres valores requeridos con Python de contenedor; solo si valida, `docker restart deer-flow-gateway` (no `docker compose up`, que necesitaría overlay para mount). Luego smoke Codex y Gemini en chats separados; registrar tokens.

## Nunca / Señal / Contramedida
- NEVER: editar YAML por búsqueda sin validar sintaxis ni asumir que guardar = aplicar.
- SIGNAL: YAML parser error indicando columnas desiguales junto a clave recién habilitada.
- COUNTERMEASURE: backup + mutación localizada + parser gate + reinicio condicional + smoke de auth.
- No versionar secretos ni config.yaml. No tocar AIDOH ni Frankenstein.

## Aprendizaje
`CONFIG_TEXT_EDITED != CONFIG_PARSED != RUNTIME_APPLIED != PROVIDER_SMOKE_PASS`.
Fuente upstream: `config.example.yaml` del owner.
