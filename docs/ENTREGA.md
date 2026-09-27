# Entrega final: qué evalúa el jurado

**Plazo: domingo 27 de septiembre de 2026.** Plantilla: `USACH-Submission-Template.pdf` (6 páginas). La redacta y la envía el equipo; Bárbara solo aporta información y valida.

La plantilla dice que el informe debe permitir **"al jurado verificar lo realizado y a la PYME continuar usando la solución"**.

## Criterios y qué necesitamos para cada uno

| Criterio | Peso | Qué nos falta para cumplirlo |
|----------|------|------------------------------|
| 1. Diagnóstico AX | 20 % | Ya está casi todo en el zip (AX_DIAGNOSIS.md). Hay que ajustarlo a los límites de caracteres. |
| 2. Completitud | 25 % | La app **publicada en una URL** que el jurado pueda abrir y usar hasta obtener un resultado. |
| 3. Usabilidad | 20 % | **Bárbara usa la app ella misma** en 3 tareas mientras observamos si lo logra sin ayuda. Hay que registrar qué falló y qué corregimos. |
| 4. Impacto | 15 % | Al menos un indicador con valor **antes y después**, medido en la prueba con Bárbara. |
| 5. Seguridad | 10 % | Volver a abrir la app y repetir el flujo. Explicar cómo protegemos la API key, qué datos usamos y qué controles aplicamos. |
| 6. Handover | 10 % | Guía de uso, registro de pruebas, video o capturas, costos en CLP y próximos pasos. |

## Las 3 tareas del Acceptance Test

Deben coincidir con las 3 tareas de la sección 1.5 y con los 3 módulos de la app. **El ACCEPTANCE_TEST.md del zip no sirve**: sus tareas describen el negocio (fabricar guateros, dar terapias), no el uso de la app.

1. **Convertir una idea suya en un post** (✍️ Guion para redes). Esperado: guion y texto que ella publicaría con pocos cambios.
2. **Aterrizar una inspiración en una experiencia** (🌱 Laboratorio). Esperado: una experiencia concreta que ella ofrecería, como "Crea tu guatero conmigo".
3. **Preparar una propuesta de difusión** (🤝 Difusión). Esperado: un mensaje listo para enviar a una junta de vecinos u otra organización.

En la sección 1.5 los tres módulos van en el cuadrante **Creative catalyst** (la IA propone y Bárbara elige), porque un error cuesta poco y es fácil de corregir.

## Indicadores propuestos (se miden con cronómetro en la prueba)

El aumento de alcance no se puede medir antes del domingo. Hay que separar lo **medido** de la **proyección**, como pide la plantilla.

| Indicador | Antes | Después | Tipo |
|-----------|-------|---------|------|
| Tiempo para tener un post listo | Lo que diga Bárbara (hoy lo improvisa o no publica) | Medido en la prueba | Medido |
| Ideas de contenido o servicios utilizables | 0 preparadas | Las que salgan de una sesión con la app | Medido |
| Alcance en Instagram | Captura de estadísticas actuales | Estadísticas del post publicado, si lo sube | Proyección / evidencia inicial |

## Entregables (cada uno con nombre y enlace exactos)

- [ ] URL de la app en Streamlit Cloud (que funcione sin que estemos presentes)
- [ ] `Guia_de_uso_BarbaraIA.pdf`: cómo abrir la app, cómo usarla, qué revisión humana no se puede saltar y un error frecuente
- [ ] `Registro_de_pruebas.xlsx`: fecha, tarea, dato utilizado, resultado y evidencia
- [ ] Video de 1 a 2 minutos, o capturas del flujo completo
- [ ] Tabla de costos en CLP: API de OpenAI (por uso), hosting ($0 en Streamlit Community Cloud)
- [ ] Próximos pasos: acción, responsable, plazo y resultado esperado

## Ojo

- Si en el futuro la app pide iniciar sesión, **el jurado necesitará una cuenta demo o un modo invitado**. Para esta entrega no hay inicio de sesión.
- Si la API key no tiene saldo, la app muestra respuestas de ejemplo (modo demo). Hay que cargar créditos antes de la prueba con Bárbara.
- No incluir contraseñas ni datos sensibles en el informe ni en las capturas.
- Si falta un dato, hay que decirlo y explicar la limitación, no inventarlo.
