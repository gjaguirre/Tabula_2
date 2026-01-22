import pytest

from tareas import Tarea
from usuarios import Usuario


def test_tarea_basic_and_serialization():
    a = Usuario("alice", "Alice")
    b = Usuario("bob", "Bob")

    t = Tarea("Refactor", "Refactorizar módulo X")
    t.agregar_usuario(a)
    t.agregar_usuario(b)

    # Autor no asignado debe fallar
    with pytest.raises(ValueError):
        t.agregar_comentario("No soy asignado", Usuario("x", "X"))

    t.agregar_comentario("Inicio trabajo", a)
    assert t.estado == "pendiente"

    t.cambiar_estado("finalizada")
    assert t.estado == "finalizada"

    json_data = t.to_json()
    t2 = Tarea.from_json(json_data)
    assert t2.nombre == t.nombre
    assert len(t2.comentarios) == 1
