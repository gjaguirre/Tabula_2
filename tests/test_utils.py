import os
from utils import (
    generar_password,
    buscar_usuario_por_nombre,
    calcular_estadisticas_tareas,
    guardar_datos,
    cargar_datos,
    leer_json,
    escribir_json,
)


class FakeUsuario:
    def __init__(self, nombre):
        self.nombre = nombre


class FakeTarea:
    def __init__(self, estado):
        self.estado = estado


def test_generar_password():
    pwd = generar_password(12, usar_simbolos=True)
    assert isinstance(pwd, str)
    assert len(pwd) == 12


def test_busqueda_y_estadisticas(tmp_path):
    usuarios = [FakeUsuario("alice"), FakeUsuario("bob")]
    u = buscar_usuario_por_nombre(usuarios, "alice")
    assert u is not None and u.nombre == "alice"

    tareas = [FakeTarea("pendiente"), FakeTarea("finalizada"), FakeTarea("pendiente")]
    stats = calcular_estadisticas_tareas(tareas)
    assert stats["total"] == 3
    assert stats["finalizadas"] == 1

    # Persistencia pickle (usar objetos picklables definidos a nivel de módulo)
    path = tmp_path / "data.pkl"
    guardar_datos(str(path), usuarios)
    carg = cargar_datos(str(path))
    assert len(carg) == 2

    # JSON
    jpath = tmp_path / "data.json"
    escribir_json(str(jpath), {"a": 1})
    jd = leer_json(str(jpath))
    assert jd["a"] == 1
