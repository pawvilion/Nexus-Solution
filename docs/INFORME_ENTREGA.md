# Informe de entrega final · Hackatón FAE USACH 2026

Borrador para copiar en `USACH-Submission-Template.pdf`. Cada respuesta larga está entre marcas `<!-- max:N -->` y respeta el máximo de caracteres con espacios de la plantilla.

**Todo lo marcado [COMPLETAR] depende de la prueba con Bárbara. No lo inventen:** llénenlo con lo que observen (la plantilla pide datos verificables).

## Identificación de la entrega

| Campo | Respuesta |
|---|---|
| Nombre del equipo | Nexus |
| Integrantes | Pablo Cayo, Pavel Andrade, Benjamín Pérez, [COMPLETAR resto con nombre y apellido] |
| PYME asignada | Terapias Dalmeet |
| Contraparte consultada | Bárbara Galdames, fundadora y terapeuta holística transpersonal |
| Nombre de la solución | Bárbara.IA: la compañera de Bárbara para ganar alcance |
| Enlace o ruta de acceso | https://nexus-dalmeet.streamlit.app · código: https://github.com/pawvilion/Nexus-Solution |

---

## 1. Diagnóstico AX · 20%

### 1.1 ¿Qué proceso, usuario y problema real aborda la solución?

<!-- max:700 -->
Proceso: convertir la visión de Bárbara en contenido y difusión que le traigan clientas. Empieza cuando tiene una idea, una anécdota o un sueño y termina cuando publica un post, ofrece una experiencia o envía una propuesta a una organización. Lo hace sola: Bárbara es terapeuta holística transpersonal, atiende, fabrica guateros a mano y lleva sus redes. Problema: su pasión no se transforma en contenido ni servicios concretos; decide en el momento qué publicar y muchas semanas no publica. Consecuencia: poco alcance y pocas clientas (2 o 3 por semana, algunas semanas ninguna), aunque lo cercano, como la feria de su villa, sí le ha funcionado.
<!-- /max -->

### 1.2 Reconstruyan un caso reciente y expliquen la causa raíz.

<!-- max:900 -->
Caso relatado en la entrevista: Bárbara cree que el cariño con que hace cada guatero le llega a quien lo usa, y sueña con una experiencia "Crea tu guatero conmigo". En una semana con sesiones y pedidos no tuvo tiempo de pensar cómo contarlo. Al abrir Instagram tuvo que decidir en el momento tema, foto y texto; lo postergó y esa semana publicó poco o nada. La idea de la experiencia siguió sin nombre, formato ni forma de ofrecerse. Lo que sí le trajo clientas constantes fue algo cercano: una feria en su villa con la junta de vecinos y terapias express, que no ha repetido. Punto crítico: el paso de la idea a algo publicable u ofrecible. Causa raíz: no tiene quién la ayude a aterrizar sus ideas con su propia voz, en el poco tiempo que le queda. Hipótesis por confirmar: que más constancia en redes y más difusión cercana aumenten las consultas.
<!-- /max -->

### 1.3 ¿Cuál era la situación inicial y con qué evidencia la respaldan?

<!-- max:500 -->
Fuente: entrevistas y reunión 1 con Bárbara (estimaciones de la PYME, resumidas en docs/CONTEXTO.md). Atiende 2 o 3 clientas por semana, algunas semanas ninguna; el 70% son mujeres de 30 a 55 años que vuelven unas 2 veces al mes. Publica de forma irregular, decidiendo en el momento, y no tiene web ni calendario de contenido. Sesiones de $10.000 a $25.000. Ideas de experiencias o servicios nuevos preparados: 0. [COMPLETAR alcance actual desde Estadísticas de Instagram]
<!-- /max -->

### 1.4 ¿Qué quedó dentro y fuera del alcance de esta entrega?

<!-- max:500 -->
Dentro: app Bárbara.IA con 5 módulos de conversación, memoria, calendario "Mi semana" editable, Centro de marketing (plan semanal, pide fotos, las edita y escribe la descripción), kit con tarjeta y afiches QR, "Tu alcance" y revisor de promesas de salud. Fuera: costos y precios (otro equipo), publicación automática en Instagram (requiere la API de Meta; hoy Bárbara aprueba y programa en Meta Business Suite) y memoria permanente en base de datos.
<!-- /max -->

### 1.5 Distribución de tareas entre IA y personas

| Tarea (máx. 120) | Cuadrante AX y motivo (máx. 180) | Qué realiza la IA (máx. 180) | Quién revisa y cuándo (máx. 180) |
|---|---|---|---|
| Convertir una idea de Bárbara en un post para Instagram | Creative catalyst: la IA propone y Bárbara elige. Un borrador con error cuesta poco y se corrige antes de publicar. | Con su esencia y memoria entrega formato, guion, texto de máximo 120 palabras, idea visual, día y hora sugeridos y hashtags. | Bárbara lee y ajusta antes de publicar. El revisor automático marca promesas de salud y datos por completar. Solo ella publica. |
| Aterrizar una inspiración en una experiencia o servicio | Creative catalyst: es una propuesta creativa. Bárbara decide si la ofrece, y un mal nombre o paso se corrige sin costo. | Propone nombres, pasos de la experiencia, formato, por qué es valiosa y un post de lanzamiento. Deja el precio como "a definir por Bárbara". | Bárbara decide si la ofrece y fija el precio. Conviene probarla con una clienta de confianza antes de lanzarla. |
| Preparar una propuesta de difusión fuera de redes | Creative catalyst: la IA redacta, Bárbara envía. Un mensaje mejorable se ajusta antes de enviarlo. | Sugiere a quién contactar, qué ofrecer (terapias express, charla, taller), un mensaje listo para WhatsApp o correo y 3 próximos pasos. | Bárbara revisa el mensaje, lo ajusta y lo envía ella misma. La app no envía nada. |

---

## 2. Solución implementada · 25%

### 2.1 ¿Cómo funciona la solución de principio a fin?

<!-- max:900 -->
Acceso: Bárbara abre https://nexus-dalmeet.streamlit.app en su celular o notebook, sin cuenta. 1) La barra lateral muestra siempre "Mi semana": qué días publica, atiende, fabrica y compra insumos; la edita si algo no le acomoda. 2) "Tu día" le propone 3 acciones. 3) En los módulos cuenta una idea y recibe guiones, experiencias o propuestas con su voz. 4) El Centro de marketing arma el plan de Instagram según sus días de publicar y le pide fotos concretas; la app las recorta al formato, ajusta la luz y agrega texto, y la IA elige las mejores y escribe la descripción. 5) Un revisor impide aprobar si hay promesas de cura o diagnósticos. 6) Aprueba, descarga y programa en Meta Business Suite. IA: Gemini gratis. Limitaciones: la publicación final es manual, los videos no se editan, sin clave usa modo demo y los datos se borran si Streamlit reinicia.
<!-- /max -->

---

## 3. Usabilidad y adopción · 20%

### 3.1 Acceptance Test de tres tareas críticas

| Tarea | Resultado esperado | Resultado observado | ¿Sin ayuda? | Evidencia |
|---|---|---|---|---|
| 1. Convertir una idea suya en un post (✍️ Guion para redes) | Guion y texto que ella publicaría con pocos cambios, sin alertas rojas del revisor | [COMPLETAR] | [Sí / No] | evidencia/tarea1_guion.png + tiempo con cronómetro |
| 2. Aterrizar una inspiración en una experiencia (🌱 Laboratorio) | Una experiencia concreta que ella ofrecería, por ejemplo "Crea tu guatero conmigo" | [COMPLETAR] | [Sí / No] | evidencia/tarea2_experiencia.png |
| 3. Preparar una propuesta de difusión (🤝 Difusión) | Mensaje listo para enviar a una junta de vecinos u otra organización | [COMPLETAR] | [Sí / No] | evidencia/tarea3_difusion.png |

### 3.2 Lectura del Acceptance Test

| Pregunta | Registro del equipo |
|---|---|
| ¿Opera la función principal? | [COMPLETAR Sí / Parcialmente / No + evidencia] |
| ¿La PYME entiende cómo usarla? | [COMPLETAR] |
| ¿El resultado es útil? | [COMPLETAR] |
| ¿Necesitó ayuda? | [COMPLETAR Sí / No + paso] |
| ¿Qué falló? (máx. 180) | [COMPLETAR] |
| ¿Qué corregimos? (máx. 180) | [COMPLETAR] |

---

## 4. Impacto en la PYME · 15%

### 4.1 Indicadores antes y después

| Indicador | Antes | Después | Fuente o forma de cálculo |
|---|---|---|---|
| Tiempo para tener un post listo | [COMPLETAR lo que diga Bárbara; hoy lo improvisa o no publica] | [COMPLETAR] min | Antes: estimación de Bárbara. Después: cronómetro en la Tarea 1 |
| Ideas de contenido o servicios utilizables | 0 preparadas | [COMPLETAR] | Respuestas marcadas con 💚 "Me sirve" en una sesión con la app |
| Alcance en Instagram (opcional) | [COMPLETAR captura actual] | [COMPLETAR si publica] | Estadísticas de Instagram; página 📈 Tu alcance. Proyección / evidencia inicial |

### 4.2 ¿Qué valor genera este resultado para la operación de la PYME?

<!-- max:500 -->
Comprobado en la prueba: [COMPLETAR, ej. "Bárbara tuvo un post listo en X min y 3 ideas que marcó como útiles"]. Beneficio principal: el paso de la idea a algo publicable u ofrecible deja de depender de que tenga tiempo y ánimo en el momento; Bárbara.IA lo aterriza con su voz y revisa que no haya promesas de salud. Proyección, no comprobada aún: más constancia en redes y difusión cercana, como su feria, deberían aumentar las consultas. Se medirá en 📈 Tu alcance durante 4 semanas.
<!-- /max -->

---

## 5. Confiabilidad y seguridad · 10%

### 5.1 ¿Cómo comprobaron la estabilidad y qué medidas tomaron para proteger datos y accesos?

<!-- max:650 -->
Estabilidad: cerramos, reabrimos y repetimos las 3 tareas [CONFIRMAR]. Si la IA falla, Bárbara.IA avisa y sigue; sin clave usa el modo demo. Accesos: la clave de Gemini está en los Secrets de Streamlit, nunca en el código ni en GitHub. Datos: la memoria no guarda datos de salud ni nombres de clientas, Bárbara puede corregirla u olvidarla y no se sube a GitHub; las capturas no se almacenan. Controles: la app no publica ni envía nada, y un revisor automático marca promesas de cura, diagnósticos, precios y datos por completar (nexus/revision.py, con pruebas). Riesgo: el plan gratis de Gemini puede usar lo enviado.
<!-- /max -->

---

## 6. Evidencia y handover · 10%

### 6.1 Entregables y evidencia

| Elemento | Qué entrega el equipo |
|---|---|
| Solución o prototipo | https://nexus-dalmeet.streamlit.app · código en https://github.com/pawvilion/Nexus-Solution |
| Guía de uso | `docs/GUIA_DE_USO.md` → exportar como `Guia_de_uso_BarbaraIA.pdf` |
| Registro de pruebas | `docs/registro_pruebas.csv` → abrir en Excel y guardar como `Registro_de_pruebas.xlsx` |
| Capturas o video | `evidencia/`: capturas de las 3 tareas o video de 1 a 2 minutos [COMPLETAR] |

### 6.2 Costos de operación

| Herramienta o servicio | Costo CLP | Frecuencia | Observación |
|---|---|---|---|
| IA: Gemini de Google (plan gratis) | $0 | Por uso | 500 consultas diarias por modelo; cada mensaje usa 2. Sin costo mientras no se supere |
| Hosting: Streamlit Community Cloud | $0 | Mensual | Plan gratuito; la app puede "dormir" si no se usa y tarda unos segundos en despertar |

### 6.3 Próximos pasos de adopción

| Acción | Responsable | Plazo | Resultado esperado |
|---|---|---|---|
| Ejecutar las 3 tareas sin ayuda | Bárbara, dueña | 04/10/2026 | 3 de 3 tareas completadas |
| Subir capturas de sus publicaciones y revisar 📈 Tu alcance | Bárbara, dueña | 25/10/2026 | Alcance de 4 semanas registrado y comparado con la línea base |
| Guardar la memoria de forma permanente y retirar accesos temporales del equipo | Equipo Nexus | 31/10/2026 | Memoria que no se borra al reiniciar y accesos cerrados |

### 6.4 ¿Qué debe saber la PYME para continuar usando la solución?

<!-- max:450 -->
Se abre en https://nexus-dalmeet.streamlit.app; queda a cargo Bárbara. Antes de publicar o enviar, lee el texto completo y cambia todo lo que el revisor marque en rojo: Bárbara.IA propone, tú decides, y nunca prometas curar ni diagnosticar. No escribas datos privados de clientas. Si algo falla o quieres una mejora, escribe al equipo Nexus por WhatsApp con una captura.
<!-- /max -->

---

## Responsable de la entrega

| Estudiante responsable | Correo | Fecha de envío |
|---|---|---|
| [COMPLETAR] | [COMPLETAR] | 27/09/2026 |
