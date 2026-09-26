"""Planificador sin IA (modo demo).

Responsable: Persona 3 (Lógica y datos).
Sirve para desarrollar y probar la app sin API key ni créditos, y como
plan B si la IA falla. Reparte las tareas por prioridad en los huecos libres.
"""

from .modelos import Bloque, Preferencias, PRIORIDADES, Tarea


def _formatear_hora(horas: float) -> str:
    minutos = round(horas * 60)
    return f"{minutos // 60:02d}:{minutos % 60:02d}"


def planificar(tareas: list[Tarea], preferencias: Preferencias) -> list[Bloque]:
    """Coloca cada tarea en el primer hueco libre, empezando por las de prioridad alta."""
    ocupado_hasta = {dia: float(preferencias.hora_inicio) for dia in preferencias.dias_disponibles}
    ordenadas = sorted(tareas, key=lambda t: PRIORIDADES.index(t.prioridad))
    bloques = []

    for tarea in ordenadas:
        candidatos = [tarea.dia_fijo] if tarea.dia_fijo else list(preferencias.dias_disponibles)
        for dia in candidatos:
            inicio = ocupado_hasta.get(dia, float(preferencias.hora_inicio))
            fin = inicio + tarea.duracion_horas
            if fin <= preferencias.hora_fin:
                bloques.append(
                    Bloque(
                        dia=dia,
                        inicio=_formatear_hora(inicio),
                        fin=_formatear_hora(fin),
                        tarea=tarea.nombre,
                        motivo=f"Prioridad {tarea.prioridad.lower()} (modo demo, sin IA)",
                    )
                )
                ocupado_hasta[dia] = fin
                break
        # Si no cabe en ningún día, la tarea se queda fuera; la interfaz lo avisa.

    return bloques
