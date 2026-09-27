"""Respuestas de ejemplo para el modo demo (sin API key).

Responsable: Persona 3.
Sirven para desarrollar sin créditos y para que el jurado vea el tipo de resultado
si la app se abre sin clave. Deben respetar las mismas reglas que la IA (sin promesas de salud).
"""

AVISO = "\n\n---\n*Modo demo: esta es una respuesta de ejemplo. Con la API key activa, Nexus responde a lo que escribes.*"

RESPUESTAS = {
    "conversemos": """Qué lindo leerte. Se nota que lo que haces no es solo un trabajo para ti: es una forma de cuidar a la gente, y eso se transmite.

Me quedo con eso para tus próximos guiones. Cuéntame: ¿recuerdas el momento en que sentiste por primera vez que esto era lo tuyo?

Si quieres, esa historia podría ser un lindo reel para que la gente te conozca: pruébala en ✍️ Guion para redes.""",
    "estadisticas": """**Lo que veo**
En tus capturas, las publicaciones donde apareces tú (explicando o trabajando) tienen más alcance y más guardados que las fotos solo de producto.

**Lo que está funcionando**
La gente conecta contigo. Cuando cuentas el porqué de lo que haces, se quedan y guardan la publicación para volver a verla.

**Lo que no está funcionando**
Las fotos de producto con fondo neutro y poco texto llegan a menos personas. No es que el producto no guste: es que no cuentan una historia.

**Qué probar esta semana**
1. Un reel corto mostrando tus manos haciendo un guatero, contando para qué sirve cada semilla.
2. Publicar entre martes y jueves, de 19:00 a 21:00, y comparar.
3. Terminar cada publicación con una pregunta para que la gente comente.

*Con pocas capturas todavía no se pueden sacar conclusiones firmes: sube más a medida que publiques.*""",
    "guion":"""Qué bonito lo que cuentas: eso es justo lo que la gente necesita ver para animarse a cuidarse.

**Formato sugerido:** reel de 20 a 30 segundos. Muestra el proceso y tu cara, que es lo que genera confianza.

**Guion**
1. *(3 s)* Plano de tus manos preparando la camilla. Texto en pantalla: "¿Hace cuánto no duermes de corrido?"
2. *(5 s)* Tú a cámara: "Muchas veces el cuerpo guarda lo que la cabeza no alcanza a soltar."
3. *(6 s)* Detalle de aceites, piedras y un guatero calentándose.
4. *(6 s)* Tú: "Por eso en mis sesiones no solo trabajo la espalda: conversamos de lo que estás viviendo."
5. *(4 s)* Cierre: "Si sientes que te hace falta una pausa, escríbeme 💛"

**Texto de la publicación**
A veces el cansancio no es solo físico. En cada sesión busco que tu cuerpo y tu cabeza tengan un momento para soltar. Cada persona es única, y por eso cada sesión también lo es. Si sientes que necesitas una pausa, escríbeme por WhatsApp y conversamos qué es lo que más te acomoda 🌿

**Idea visual:** graba con luz de ventana y el celular apoyado en un vaso; no necesitas trípode.

**Cuándo publicar:** martes o jueves entre 19:00 y 21:00.
**Hashtags:** #PuenteAlto #Autocuidado #TerapiasHolísticas #Reiki #BienestarNatural

**Siguiente paso:** grábalo después de tu próxima sesión, mientras la sensación está fresca.""",
    "experiencia": """Esa idea tiene mucha fuerza: la gente no solo se lleva un guatero, se lleva un momento contigo.

**Nombre**
- *Crea tu guatero conmigo*
- *Guatero con alma*
- *Hecho a tu medida*

**Qué vive la persona**
1. **Escucha (10 min):** conversan con un té sobre qué necesita (descanso, frío en los pies, tensión en la espalda).
2. **Medidas:** ven juntas dónde lo usará y definen el tamaño.
3. **Elección del relleno:** huele y elige semillas, hierbas y aromas mientras tú le cuentas para qué sirve cada uno.
4. **Creación conjunta:** rellenan y cierran el guatero entre las dos.
5. **Cierre:** se lo lleva con una tarjeta escrita a mano con su intención.

**Formato:** 60 a 75 minutos, individual o de a dos (amigas, madre e hija). En tu casa o como estación en una feria.

**Por qué es valiosa:** no es un producto de tienda; es un objeto que vio nacer y que lleva su historia. Además, es un regalo con significado.

**Precio:** [a definir por Bárbara]

**Post de lanzamiento:** un carrusel con las 5 etapas en fotos y el texto: "¿Y si tu guatero lo hiciéramos juntas?"

**Siguiente paso:** pruébala primero con una clienta de confianza y pídele permiso para fotografiar el proceso.""",
    "difusion": """Me encanta: lo de tu villa ya demostró que funciona, así que ahora es cosa de repetirlo.

**A quién contactar:** la junta de vecinos de otra villa de Puente Alto. Les conviene porque les das una actividad gratuita y atractiva para sus vecinos, y apoya a emprendedoras locales.

**Qué ofrecer:** una tarde de bienestar con terapias express de 15 minutos y una mesa de productos. Puedes sumar una charla corta de autocuidado.

**Mensaje listo para enviar (WhatsApp)**
> Hola, ¿cómo está? Mi nombre es Bárbara, soy terapeuta holística de Puente Alto (Terapias Dalmeet). Hace poco organizamos con la junta de vecinos de mi villa una tarde de bienestar con terapias express y emprendedoras del barrio, y a los vecinos les encantó. Me encantaría proponerles algo así en su villa, sin costo para la junta. ¿Podríamos conversar 10 minutos esta semana? ¡Muchas gracias! 🌿

**Próximos pasos**
1. Busca en Instagram o Facebook la página de la junta de vecinos o pregunta a una clienta de esa villa.
2. Ten a mano 2 o 3 fotos de la feria de tu villa para mostrarles.
3. Propón una fecha concreta, por ejemplo un sábado en la tarde.

**Siguiente paso:** envía hoy el mensaje a una sola junta; la primera es la que más cuesta.""",
}


def responder(modo: str) -> str:
    return RESPUESTAS[modo] + AVISO
