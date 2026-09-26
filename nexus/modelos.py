"""Modelos de datos compartidos por todo el proyecto.

Responsable: Persona 3 (Lógica y datos).
Es el "contrato" entre la interfaz y la IA: si cambias un campo, avisa al equipo.
"""

from dataclasses import dataclass, asdict

DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
PRIORIDADES = ["Alta", "Media", "Baja"]


@dataclass
class Tarea:
    """Algo que el usuario quiere hacer durante la semana."""

    nombre: str
    duracion_horas: float
    prioridad: str = "Media"  # uno de PRIORIDADES
    dia_fijo: str | None = None  # uno de DIAS si la tarea tiene día obligatorio

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Preferencias:
    """Cómo quiere el usuario que se organice su semana."""

    hora_inicio: int = 9  # hora del día (0-23) a la que empieza a trabajar
    hora_fin: int = 18
    dias_disponibles: tuple[str, ...] = tuple(DIAS[:5])
    notas: str = ""  # texto libre para la IA ("prefiero deporte por la mañana"...)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Bloque:
    """Un hueco del horario ya planificado."""

    dia: str
    inicio: str  # "HH:MM"
    fin: str  # "HH:MM"
    tarea: str
    motivo: str = ""  # por qué se colocó aquí (lo rellena la IA)

    def to_dict(self) -> dict:
        return asdict(self)
