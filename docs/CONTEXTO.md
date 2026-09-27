# Contexto del cliente: Terapias Dalmeet

Resumen del diagnóstico de la hackatón (zip USACH, entrevistas y reunión 1), con las correcciones y decisiones del equipo. Si algo de aquí contradice los documentos originales, **manda este archivo**.

## Para quién es

**Bárbara Galdames**, dueña de Terapias Dalmeet: terapeuta holística transpersonal, con formación en psicología y 15 años de experiencia en Brasil. Trabaja sola en Puente Alto (Santiago).

- **Servicios:** masajes, reiki, reflexología, aromaterapia y flores de Bach. Sesiones de 45 a 90 minutos, entre $10.000 y $25.000, en su casa o a domicilio.
- **Productos:** guateros terapéuticos de semillas (su producto estrella: para frío o calor, para uso propio o para regalar, de mejor calidad que uno genérico) y sales de baño.
- **Clientas:** 2 o 3 por semana (algunas semanas ninguna). El 70 % son mujeres de 30 a 55 años. Son fieles y vuelven unas 2 veces al mes.
- **Canales:** Instagram, Facebook Marketplace, WhatsApp y ferias.
- **Equipo técnico:** notebook básico y celular, así que la app debe ser liviana.
- **IA:** paga ChatGPT y lo usa como compañía para conversar (le puso "ayam"). Tiene un presupuesto pequeño pero real. Ojo: la suscripción a ChatGPT **no incluye la API**, que se paga aparte.

Su visión, sus creencias y sus sueños están en [nexus/esencia.md](../nexus/esencia.md), que es el texto que usa la IA.

## El problema que elegimos: poco alcance

Bárbara tiene pocas clientas, sobre todo de terapias. Creemos que la causa es el **poco alcance y difusión**.

Tiene una visión clara y una pasión real (por ejemplo, cree que el cariño que pone en cada producto trasciende a quien lo usa), pero **eso no se convierte en contenido, productos ni servicios** que lleguen a más gente. Publica de forma irregular porque tiene que decidir en el momento qué subir mientras atiende y fabrica.

Lo que sí le ha funcionado es lo cercano: el boca a boca y **una feria en su villa** con la junta de vecinos y terapias express, que le dejó clientas constantes.

## Nuestro diferenciador: cercanía

Son 30 equipos. Muchos harán productos muy pulidos técnicamente, y hay otro equipo (de contabilidad) trabajando con Bárbara en costos y finanzas. **No competimos en eso.**

Nuestra apuesta es la **cercanía con la emprendedora**: quien empieza vende poco, pero tiene un sueño, y le falta alguien que la ayude a aterrizarlo. Bárbara.IA es esa compañera: escucha la idea como Bárbara la cuente y la devuelve convertida en algo concreto, con su voz.

Esto se nota en la app:
- Es una **conversación**, no un formulario, porque a Bárbara le gusta conversar con la IA.
- Bárbara.IA **cree en su sueño**: reconoce lo valioso de su idea y la aterriza, sin halagos vacíos.
- Todo lo que genera **suena a Bárbara**, porque parte de su esencia.

## Qué construimos

| Módulo | Qué entra | Qué sale |
|--------|-----------|----------|
| 💭 **Conversemos** | Sus sueños, creencias e historias, contados libremente | Una conversación cercana; lo importante queda en la memoria |
| ✍️ **Guion para redes** | Una idea, anécdota o creencia | Guion de reel o carrusel, texto del post, idea visual, día y hora para publicar |
| 🌱 **Laboratorio de experiencias** | Una inspiración ("quiero que sientan el cariño del guatero") | Una experiencia o servicio concreto: nombre, pasos, formato, por qué es valiosa y post de lanzamiento |
| 🤝 **Difusión fuera de redes** | A quién quiere llegar (junta de vecinos, feria, empresa, municipalidad, otra ciudad) | Qué ofrecer, mensaje listo para enviar y próximos pasos |

| 📊 **Mis estadísticas** | Capturas de pantalla de las estadísticas de Instagram | Qué funciona, qué no y 3 cosas para probar esta semana |

**Memoria:** lo que Bárbara cuenta y lo que muestran sus estadísticas se guarda en 5 **consolidados por tema** (sueños y metas, creencias, historia, trabajo y clientas, redes), escritos hablándole a ella (`nexus/memoria.py`). Con cada mensaje, la IA reescribe solo los temas donde hay algo nuevo, integrándolo sin perder lo anterior. Todos los módulos los usan, así que con el tiempo el contenido se parece cada vez más a ella. En la barra lateral, "Lo que Bárbara.IA sabe de ti" muestra cada tema con su comienzo; al tocarlo se abre una ventana donde puede leerlo entero, corregirlo u olvidarlo (con confirmación). No se guardan datos de salud ni nombres de clientas, y las capturas no se almacenan: solo lo aprendido de ellas.

**📣 Kit de difusión:** para que la difusión salga del chat y circule en el mundo real, donde a Bárbara ya le funciona (ferias, juntas de vecinos, boca a boca). Incluye una **tarjeta digital** (no tiene página web) con su historia, terapias, productos y botón de WhatsApp, y **afiches con QR** listos para imprimir. Cada QR abre WhatsApp con un mensaje que dice de dónde llegó la persona ("te encontré por la feria de…"), así Bárbara sabe qué lugar le trae clientas. El texto del afiche lo puede sugerir la IA según el lugar.

**📈 Tu alcance:** al subir capturas de estadísticas, la IA saca los números de cada publicación (sin inventar los que no se ven) y los guarda. La página muestra el promedio, la mejor publicación, qué formato llega más lejos y un gráfico. Es el indicador de impacto medido dentro de la propia app. Los números se pueden corregir o cargar a mano.

**Inicio proactivo ("Tu día con Bárbara.IA"):** al abrir la app, Bárbara.IA no espera a que Bárbara escriba. La saluda con algo concreto que sabe de ella, le dice cómo va con sus publicaciones (las registra con el botón "📣 Lo publiqué") y le propone 3 acciones para hoy, cada una con un botón que empieza la conversación en el módulo correcto. Es lo que la diferencia de un chat genérico: **toma la iniciativa, como una compañera**.

Se usan capturas porque la API de Instagram exige cuenta de empresa, una app registrada en Meta y una revisión de permisos que tarda días.

La app no publica ni envía nada sola: prepara todo listo y Bárbara decide. **Fuera de alcance:** costos, precios y contabilidad (los trabaja el otro equipo); publicación automática; cuentas de usuario y memoria permanente en una base de datos (quedan como próximo paso: hoy la memoria se guarda en un archivo que Streamlit Cloud borra al reiniciar la app).

## Reglas que no se pueden romper

- **Nada de promesas de cura ni de tratar condiciones** (por ejemplo, TDAH, ansiedad o dolor crónico). Se habla de bienestar, relajación y acompañamiento.
- **No usar la palabra "diagnóstico"** ni presentar su formación en psicología como atención clínica. Para la experiencia del guatero se dice "conversación inicial" o "escucha".
- **Inspirar y educar primero, vender después.**
- No inventar precios, testimonios ni cifras: se marcan como `[a completar por Bárbara]`.
- Nunca subir al repo datos personales, como los PDF de las entrevistas (incluyen su teléfono).

## Pendiente de confirmar con Bárbara

- [ ] Que el tono de [nexus/esencia.md](../nexus/esencia.md) la represente (lo ideal es que lo lea ella).
- [ ] Qué terapias quiere destacar primero.
- [ ] Si le interesa lanzar "Crea tu guatero conmigo" y otra feria como la de su villa.
- [ ] Estadísticas actuales de Instagram (alcance, seguidores, visitas al perfil) para la línea base.
