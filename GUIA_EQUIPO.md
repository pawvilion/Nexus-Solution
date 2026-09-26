# Guía rápida para trabajar juntos en GitHub

## 1. Preparación (una sola vez)

1. **Crea una cuenta** en https://github.com/signup y pásale tu nombre de usuario al dueño del proyecto.
2. **Instala Git**: https://git-scm.com/download/win (deja todas las opciones por defecto).
3. **Instala GitHub Desktop** (opcional, pero mucho más fácil): https://desktop.github.com
   - Ábrelo e inicia sesión con tu cuenta de GitHub.
4. **Acepta la invitación** que te llegará al correo (o en https://github.com/notifications).
5. **Descarga el proyecto**: en GitHub Desktop → `File` → `Clone repository` → elige el proyecto → `Clone`.

## 2. Rutina de trabajo (cada vez que trabajes)

| Paso | GitHub Desktop | Terminal |
|------|----------------|----------|
| 1. Traer lo último de los demás | `Fetch origin` → `Pull origin` | `git pull` |
| 2. Crear tu rama (tu "copia" para trabajar) | `Current branch` → `New branch` → ej. `pablo-menu` | `git switch -c pablo-menu` |
| 3. Trabajar y guardar tus archivos | (edita normalmente) | (edita normalmente) |
| 4. Hacer un *commit* (guardar un punto) | Escribe un resumen abajo a la izquierda → `Commit` | `git add .` y `git commit -m "Añado menú"` |
| 5. Subir tu rama | `Push origin` | `git push -u origin pablo-menu` |
| 6. Pedir que se una al proyecto | `Create Pull Request` | desde la web de GitHub |

Otro compañero revisa el **Pull Request** en la web y pulsa **Merge**. Después, todos vuelven a la rama `main` y hacen `Pull`.

## 3. Reglas del equipo

- **Nunca trabajes directamente en `main`.** Siempre en tu propia rama.
- **Haz `Pull` antes de empezar** a trabajar cada día.
- Commits pequeños y con mensajes claros ("Arreglo botón de salir", no "cambios").
- Avisad por el chat del grupo qué archivo va a tocar cada uno para evitar conflictos.

## 4. ¿Y si sale un "conflicto"?

Pasa cuando dos personas cambian las mismas líneas. Git marca el archivo así:

```
<<<<<<< HEAD
tu versión
=======
la versión del otro
>>>>>>> main
```

Deja el texto correcto, borra las líneas `<<<<<<<`, `=======` y `>>>>>>>`, guarda y haz un commit. Si dudas, pregunta antes de borrar nada.
