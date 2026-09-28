# Informe de entrega final · Hackatón FAE USACH 2026

Borrador para copiar en `USACH-Submission-Template.pdf`. Cada respuesta larga está entre marcas `<!-- max:N -->` y respeta el máximo de caracteres con espacios de la plantilla. Los datos de la PYME vienen de las entrevistas, de la sesión de prueba con Bárbara (27/09/2026, grabada) y de `docs/Registro_de_pruebas_BarbaraIA.xlsx`.

**Quedan 2 cosas por completar ([COMPLETAR]):** el link del video y las capturas (sección 6.1) y el responsable de la entrega (final).

## Identificación de la entrega

| Campo | Respuesta |
|---|---|
| Nombre del equipo | Nexus |
| Integrantes | Pablo Cayo, Pavel Andrade, Benjamín Pérez, Sofía Acevedo |
| PYME asignada | Terapias Dalmeet |
| Contraparte consultada | Bárbara Galdames, fundadora y terapeuta holística transpersonal |
| Nombre de la solución | Bárbara.IA: la compañera de Bárbara para ganar alcance |
| Enlace o ruta de acceso | https://nexus-dalmeet.streamlit.app · código: https://github.com/pawvilion/Nexus-Solution |

---

## 1. Diagnóstico AX · 20%

### 1.1 ¿Qué proceso, usuario y problema real aborda la solución?

<!-- max:700 -->
Proceso: convertir la visión de Bárbara en contenido y difusión que le traigan clientas. Empieza cuando tiene una idea, una anécdota o un sueño y termina cuando publica, ofrece una experiencia o mide cómo le fue. Lo hace sola: Bárbara es terapeuta holística transpersonal, atiende, fabrica guateros a mano y lleva sus redes. Problema: su pasión no se transforma en contenido constante; decide en el momento qué publicar, le toma de 3 horas a 2 días tener un post listo y publica 1 vez por semana. Consecuencia: poco alcance (88 cuentas en su último reel) y pocas clientas (unas 3 consultas por semana), aunque lo cercano, como la feria de su villa, sí le ha funcionado.
<!-- /max -->

### 1.2 Reconstruyan un caso reciente y expliquen la causa raíz.

<!-- max:900 -->
Caso relatado en la entrevista: Bárbara cree que el cariño con que hace cada guatero le llega a quien lo usa, y sueña con una experiencia "Crea tu guatero conmigo". En una semana con sesiones y pedidos no tuvo tiempo de pensar cómo contarlo. Al abrir Instagram tuvo que decidir en el momento tema, foto y texto; lo postergó y esa semana publicó poco o nada. La idea de la experiencia siguió sin nombre, formato ni forma de ofrecerse. Lo que sí le trajo clientas constantes fue algo cercano: una feria en su villa con la junta de vecinos y terapias express, que no ha repetido. Punto crítico: el paso de la idea a algo publicable, y saber si lo publicado le trae clientas. Causa raíz: no tiene quién la ayude a aterrizar sus ideas con su voz, planificarlas y medirlas en el poco tiempo que le queda. Hipótesis por confirmar: más constancia y difusión cercana aumentan las consultas.
<!-- /max -->

### 1.3 ¿Cuál era la situación inicial y con qué evidencia la respaldan?

<!-- max:500 -->
Fuentes: entrevistas, reunión 1 y sesión del 27/09 con Bárbara (Registro_de_pruebas_BarbaraIA.xlsx, hoja Indicadores). Tener un post listo le tomaba de 3 horas a 2 días; publicaba 1 vez por semana, sin calendario de contenido ni web. Recibe unas 3 consultas por semana y el 70% de sus clientas son mujeres de 30 a 55 años. Su último reel ("Productos Terapias Dalmeet Spa") alcanzó 88 cuentas, según la captura de Instagram que subió en la sesión. Sesiones de $10.000 a $25.000.
<!-- /max -->

### 1.4 ¿Qué quedó dentro y fuera del alcance de esta entrega?

<!-- max:500 -->
Dentro: Bárbara.IA con 5 módulos de conversación y memoria editable; Marketing Executor (la IA crea la campaña, Bárbara aprueba, pide cambios o rechaza, registra resultados y el reporte genera el siguiente plan); calendario semanal; kit con tarjeta digital y afiches QR; "Tu alcance" con sus métricas de Instagram; revisor de promesas de salud. Fuera: costos y precios (otro equipo), publicación automática en Instagram (fase 2, requiere la API de Meta), inicio de sesión y base de datos permanente.
<!-- /max -->

### 1.5 Distribución de tareas entre IA y personas

| Tarea (máx. 120) | Cuadrante AX y motivo (máx. 180) | Qué realiza la IA (máx. 180) | Quién revisa y cuándo (máx. 180) |
|---|---|---|---|
| Convertir una idea o anécdota de Bárbara en un post para Instagram | Creative catalyst: la IA propone y Bárbara elige. Un borrador con error cuesta poco y se corrige antes de publicar. | Con su esencia y memoria entrega formato, guion, texto, idea visual, día y hora sugeridos y hashtags, sin nombrar condiciones de salud. | Bárbara lee y ajusta antes de publicar. El revisor automático marca en rojo promesas de salud y datos por completar. Solo ella publica. |
| Planificar una campaña de 2 semanas y decidir qué se publica (Marketing Executor) | Human first: lo que sale hacia afuera lleva su nombre. La IA planifica, pero cada acción externa requiere la aprobación de Bárbara. | Analiza su memoria, semana y resultados; crea 5 a 8 acciones con fecha y texto listo, y reescribe una acción según la nota de Bárbara. | Bárbara aprueba, pide cambios o rechaza cada acción antes de ejecutarla. El revisor bloquea la aprobación si hay frases prohibidas. |
| Leer sus estadísticas de Instagram y decir qué funciona | No regrets: son sus propios números y leerlos bien tiene bajo riesgo. Si la IA lee mal una cifra, se corrige en la tabla. | Lee las cifras de sus capturas sin inventar las que no se ven, las guarda y explica qué funciona, qué no y qué probar. | Bárbara revisa y corrige los números en 📈 Tu alcance. Ella decide qué recomendación aplicar en su próximo post. |

---

## 2. Solución implementada · 25%

### 2.1 ¿Cómo funciona la solución de principio a fin?

<!-- max:900 -->
Acceso: Bárbara abre https://nexus-dalmeet.streamlit.app en su celular o notebook, sin cuenta. 1) "Tu día" le propone 3 acciones. 2) En los módulos cuenta una idea y recibe guiones, experiencias o propuestas con su voz; la memoria aprende de ella. 3) En el Marketing Executor la IA analiza su situación y crea una campaña de 2 semanas; Bárbara aprueba, pide cambios (la IA reescribe) o rechaza cada acción, y un revisor bloquea promesas de salud. 4) Publica lo aprobado y registra consultas y clientas. 5) Sube capturas de Instagram y "Tu alcance" muestra qué le funciona. 6) El reporte vuelve a la IA, que crea el siguiente plan. Además: calendario, tarjeta digital y afiches QR. IA: Gemini gratis. Limitaciones: la publicación es manual, sin API key usa modo demo y los datos se borran si Streamlit reinicia la app.
<!-- /max -->

---

## 3. Usabilidad y adopción · 20%

### 3.1 Acceptance Test de tres tareas críticas

| Tarea | Resultado esperado | Resultado observado | ¿Sin ayuda? | Evidencia |
|---|---|---|---|---|
| 1. Convertir una idea suya en un post (✍️ Guion para redes) | Guion y texto que publicaría con pocos cambios, sin alertas rojas | Guion de referencia con la explicación del porqué; el revisor marcó 2 palabras no permitidas ("sanar", "insomnio") | Sí · 8 min | Video de la sesión, min 5 a 8 |
| 2. Crear su plan y aprobar acciones (⚙️ Marketing Executor) | Campaña creada, al menos una acción aprobada y otra modificada por la IA | Campaña de 7 acciones creada con IA y 1 acción aprobada; no se probó "Modificar con IA" | Sí · 2 min | Video de la sesión, min 9 a 10 |
| 3. Subir una captura real de Instagram y revisar 📈 Tu alcance | Sus números leídos correctamente y qué formato le funciona | Números leídos correctamente (reel de 88 cuentas) y un análisis tipo FODA de qué funciona | Sí · 3 min | Video de la sesión, min 11 a 13 |

### 3.2 Lectura del Acceptance Test

| Pregunta | Registro del equipo |
|---|---|
| ¿Opera la función principal? | Sí: completó las 3 tareas en su celular Android con la app pública (video de la sesión del 27/09). |
| ¿La PYME entiende cómo usarla? | Sí: navegó sola entre Inicio, Marketing y Alcance y usó los ejemplos para empezar. |
| ¿El resultado es útil? | Sí: el guion le sirvió de referencia, la campaña quedó planificada y el análisis de estadísticas le mostró qué mejorar. |
| ¿Necesitó ayuda? | No: las 3 tareas se hicieron sin ayuda (8, 2 y 3 minutos). |
| ¿Qué falló? (máx. 180) | El guion usó "sanar" e "insomnio" al contar un caso de crisis de pánico; el revisor lo marcó en rojo. No alcanzamos a probar "Modificar con IA" en la sesión. |
| ¿Qué corregimos? (máx. 180) | Reforzamos las instrucciones: la IA ya no nombra condiciones de salud ni dice "sanar". Con el mismo mensaje: 0 alertas rojas en 3 intentos. |

---

## 4. Impacto en la PYME · 15%

### 4.1 Indicadores antes y después

| Indicador | Antes | Después | Fuente o forma de cálculo |
|---|---|---|---|
| Tiempo para tener una publicación lista | De 3 horas a 2 días | 8 minutos, de la idea al guion listo | Antes: estimación de Bárbara. Después: cronómetro en la Tarea 1 (medido) |
| Publicaciones planificadas para 2 semanas | 1 por semana, decidida en el momento | 7 acciones planificadas por el Marketing Executor (1 aprobada en la sesión) | Antes: entrevista. Después: campaña creada en la Tarea 2 (medido) |

### 4.2 ¿Qué valor genera este resultado para la operación de la PYME?

<!-- max:500 -->
Comprobado en la sesión: Bárbara pasó de tardar entre 3 horas y 2 días en tener un post a tener un guion listo en 8 minutos, y de publicar 1 vez por semana sin plan a tener 7 acciones planificadas para 2 semanas. Beneficio principal: publicar con constancia deja de depender del tiempo y el ánimo del momento. Proyección, aún no comprobada: más constancia y difusión cercana deberían subir su alcance (hoy 88 cuentas por reel) y sus consultas (3 por semana). Se medirá al cierre de la campaña.
<!-- /max -->

---

## 5. Confiabilidad y seguridad · 10%

### 5.1 ¿Cómo comprobaron la estabilidad y qué medidas tomaron para proteger datos y accesos?

<!-- max:650 -->
Estabilidad: Bárbara usó la app pública en su celular sin errores; probamos reabrir la página (la memoria se mantiene), el ciclo completo del Marketing Executor y la saturación de la IA (pasa a un modelo de respaldo y avisa). Accesos: la clave de Gemini está en los Secrets de Streamlit, nunca en el código. Datos: no se guardan datos de salud ni nombres de clientas; Bárbara puede corregir u olvidar su memoria. Controles: nada se publica solo y un revisor bloquea promesas de salud; en la sesión detectó 2 palabras. Riesgos: el plan gratis de Gemini puede usar lo enviado, y los datos se borran si la app se reinicia.
<!-- /max -->

---

## 6. Evidencia y handover · 10%

### 6.1 Entregables y evidencia

| Elemento | Qué entrega el equipo |
|---|---|
| Solución o prototipo | App publicada: https://nexus-dalmeet.streamlit.app (se abre sin cuenta, en celular o notebook). Código: https://github.com/pawvilion/Nexus-Solution |
| Guía de uso | Guia_de_uso_BarbaraIA.docx — https://github.com/pawvilion/Nexus-Solution/blob/main/docs/Guia_de_uso_BarbaraIA.docx |
| Registro de pruebas | Registro_de_pruebas_BarbaraIA.xlsx — https://github.com/pawvilion/Nexus-Solution/blob/main/docs/Registro_de_pruebas_BarbaraIA.xlsx |
| Capturas o video | Video de la sesión con Bárbara (Video descubrimiento y uso de 3 funciones por Bárbara Terapias Dalmeet.mp4) y resumen de 1 a 2 minutos — [COMPLETAR link de Drive o YouTube] |

### 6.2 Costos de operación

| Herramienta o servicio | Costo CLP | Frecuencia | Observación |
|---|---|---|---|
| API de Google Gemini (IA de la app): gemini-3.5-flash-lite, con gemini-3.1-flash-lite de respaldo | $0 (plan gratuito) | Por uso, hoy sin cobro | Hasta 15 consultas por minuto y 500 al día por modelo; cada mensaje usa 2, alcanza para su uso diario. Si necesitara más, pago por uso según la tarifa vigente de Google. En el plan gratis Google puede usar lo enviado, por eso no se ingresan datos de clientas. |
| Streamlit Community Cloud (publicación de la app) y GitHub (código) | $0 (planes gratuitos) | Mensual, sin cobro | La app está en nexus-dalmeet.streamlit.app, sin cuenta para Bárbara. Se "duerme" tras horas sin uso y al reiniciarse borra los datos; se resuelve sin costo con una base de datos PostgreSQL gratuita. |

### 6.3 Próximos pasos de adopción

| Acción | Responsable | Plazo | Resultado esperado |
|---|---|---|---|
| Crear su plan en el Marketing Executor, aprobar las acciones y publicar las de la semana sin ayuda | Bárbara (dueña) | 04/10/2026 | 3 de 3 publicaciones aprobadas y publicadas sin ayuda |
| Subir capturas de estadísticas, anotar consultas y nuevas clientas en Resultados, y crear el siguiente plan con el reporte | Bárbara (dueña), con apoyo del equipo Nexus | 11/10/2026 | Alcance y consultas comparados con la línea base (88 cuentas por reel, 3 consultas por semana) y segundo plan creado |
| Agregar inicio de sesión y base de datos permanente, y pasar la clave de Gemini a una cuenta de Bárbara | Equipo Nexus, con Bárbara | 27/10/2026 | Solo Bárbara accede a sus datos, no se borran al reiniciar y se retiran los accesos del equipo |

### 6.4 ¿Qué debe saber la PYME para continuar usando la solución?

<!-- max:450 -->
Se abre en https://nexus-dalmeet.streamlit.app y queda a cargo de Bárbara. Antes de publicar, lee el texto completo y cambia lo que el revisor marque en rojo: Bárbara.IA propone y tú decides; nunca prometas curar. En el Marketing Executor aprueba solo lo que te represente. No escribas datos privados de clientas. Si algo falla o quieres una mejora, escribe al equipo Nexus por WhatsApp con una captura.
<!-- /max -->

---

## Responsable de la entrega

| Estudiante responsable | Correo | Fecha de envío |
|---|---|---|
| [COMPLETAR] | [COMPLETAR] | 27/09/2026 |
