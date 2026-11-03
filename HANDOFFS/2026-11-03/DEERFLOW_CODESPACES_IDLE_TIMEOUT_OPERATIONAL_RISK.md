# DeerFlow — Riesgo operativo de suspensión de Codespaces
**Fecha:** 2026-11-03
**Estado:** PENDIENTE / NO RESUELTO
**Observación del operador:** Mientras trabaja desde la interfaz web de DeerFlow publicada en el puerto de Codespaces, GitHub puede advertir inactividad y suspender el Codespace aunque DeerFlow parezca estar en uso. La terminal/VS Code no muestran actividad perceptible.

## Verificación externa (GitHub Docs)
- https://docs.github.com/en/codespaces/setting-your-user-preferences/setting-your-timeout-period-for-github-codespaces
- https://docs.github.com/en/codespaces/about-codespaces/understanding-the-codespace-lifecycle

GitHub define actividad como interacciones personales con Codespace y/o entradas/salidas de la terminal. Tráfico de página sobre puerto reenviado sin salida en terminal no garantiza reiniciar el contador.
- Idle default 30 min; configuración de usuario 5–240 min, aplicada a nuevos Codespaces; límites de política organizacional pueden prevalecer.
- Vida máxima de una sesión hasta 12 h incluso con actividad.
- Los Codespaces detenidos conservan cambios guardados pero suspenden procesos; se sigue cobrando almacenamiento, no CPU.
- Uso activo de Codespaces tiene costo de cómputo, por lo que no conviene simular actividad artificial.

## Consecuencia
El Codespace actual sirve para experimentación y desarrollo, pero NO debe declararse hosting durable para tareas autónomas, fallover entre proveedores, programación nocturna, equipos comerciales, automatizaciones ni Frankenstein/AIDOH.

## Plan
1. **Ahora**: mantener Codespaces dev-only; no instalar keepalive engañoso ni abrir puerto público; aceptar reinicios conservando estado seguro y secretos fuera de Git.
2. **Después del Gate R1/R2**: medir tiempo real de operación vs tiempo suspendido y costo de Codespaces.
3. **Si DeerFlow demuestra valor**: diseñar migración del Gateway a cómputo persistente controlado (VM/VPS/instancia o infraestructura equivalente), con discos persistentes, Postgres/Redis, secretos, TLS y acceso privado, respaldos y recuperación probada. Desarrollo sigue en Codespaces; el servicio deja de depender de sesiones interactivas.
4. Verificar mediante una prueba de cierre/reapertura sin perder archivos, checkpoints y autenticaciones; cero secretos en GitHub.
5. Separar disponibilidad 24/7 de tolerancia a fallos de modelos: un servidor siempre encendido NO implementa automáticamente failover Codex/Claude.

## Nota de gobernanza
No modificar timeout, machine type ni plataforma todavía: requiere evaluación de consumo, seguridad, costo y aprobación humana. AIDOH productivo y Frankenstein congelado no se tocan.

## VEREDICTO
**Salida:** 🟡 Diseñar experimento de hosting y continuidad DESPUÉS de demostrar valor de DeerFlow.
**Quién:** Coordinación técnica + aprobación del operador.
**Cuándo:** Luego de probar relevo real de trabajo entre Codex y Claude y auditar costo.
**Éxito:** DeerFlow accesible de manera durable, reinicios sin pérdida de estado, bajo costo neto, sin scripts de keepalive artificial.
