from __future__ import annotations

import json
import pickle
import secrets
import string
from typing import Any, List, Optional, TypeVar, Dict

T = TypeVar("T")

# ==========================================================
# Persistencia
# ==========================================================

def cargar_datos(path: str, default: Optional[List[T]] = None) -> List[T]:
    """
    Carga datos desde un archivo binario usando pickle.

    Args:
        path (str): Ruta del archivo.
        default (Optional[List[T]]): Valor por defecto si el archivo no existe.

    Returns:
        List[T]: Lista de objetos cargados o el valor por defecto.
    """
    if default is None:
        default = []

    try:
        with open(path, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return default
    except Exception as e:
        raise RuntimeError(f"Error al cargar datos desde {path}") from e


def guardar_datos(path: str, data: List[Any]) -> None:
    """
    Guarda datos en un archivo binario usando pickle.

    Args:
        path (str): Ruta del archivo.
        data (List[Any]): Lista de objetos a guardar.
    """
    try:
        with open(path, "wb") as f:
            pickle.dump(data, f)
    except Exception as e:
        raise RuntimeError(f"Error al guardar datos en {path}") from e


def leer_json(path: str, default: Optional[Any] = None) -> Any:
    """
    Lee datos desde un archivo JSON.

    Args:
        path (str): Ruta del archivo.
        default (Optional[Any]): Valor por defecto si el archivo no existe.

    Returns:
        Any: Contenido del JSON o el valor por defecto.
    """
    if default is None:
        default = []

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default
    except Exception as e:
        raise RuntimeError(f"Error al leer JSON desde {path}") from e


def escribir_json(path: str, data: Any) -> None:
    """
    Escribe datos en un archivo JSON.

    Args:
        path (str): Ruta del archivo.
        data (Any): Datos serializables a JSON.
    """
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        raise RuntimeError(f"Error al escribir JSON en {path}") from e


# ==========================================================
# Seguridad
# ==========================================================

def generar_password(
    longitud: int = 12,
    usar_simbolos: bool = True,
) -> str:
    """
    Genera una contraseña aleatoria segura.

    Args:
        longitud (int): Longitud de la contraseña.
        usar_simbolos (bool): Si se incluyen símbolos.

    Returns:
        str: Contraseña generada.
    """
    if longitud < 8:
        raise ValueError("La longitud mínima recomendada es 8.")

    caracteres = string.ascii_letters + string.digits
    if usar_simbolos:
        caracteres += string.punctuation

    return "".join(secrets.choice(caracteres) for _ in range(longitud))


# ==========================================================
# Búsqueda
# ==========================================================

def buscar_usuario_por_nombre(usuarios: List[Any], nombre: str) -> Optional[Any]:
    """
    Busca un usuario por nombre (username).

    Args:
        usuarios (List[Any]): Lista de usuarios.
        nombre (str): Nombre a buscar.

    Returns:
        Optional[Any]: Usuario encontrado o None.
    """
    for usuario in usuarios:
        if getattr(usuario, "nombre", None) == nombre:
            return usuario
    return None


def buscar_tarea_por_nombre(tareas: List[Any], nombre: str) -> Optional[Any]:
    """
    Busca una tarea por nombre.

    Args:
        tareas (List[Any]): Lista de tareas.
        nombre (str): Nombre de la tarea.

    Returns:
        Optional[Any]: Tarea encontrada o None.
    """
    for tarea in tareas:
        if getattr(tarea, "nombre", None) == nombre:
            return tarea
    return None


# ==========================================================
# Estadísticas
# ==========================================================

def calcular_estadisticas_tareas(tareas: List[Any]) -> Dict[str, int]:
    """
    Calcula estadísticas básicas de una lista de tareas.

    Args:
        tareas (List[Any]): Lista de tareas.

    Returns:
        Dict[str, int]: Diccionario con totales, pendientes y finalizadas.
    """
    total = len(tareas)
    finalizadas = sum(
        1 for t in tareas if getattr(t, "estado", None) == "finalizada"
    )
    pendientes = total - finalizadas

    return {
        "total": total,
        "finalizadas": finalizadas,
        "pendientes": pendientes,
    }


# ==========================================================
# Tests manuales
# ==========================================================

if __name__ == "__main__":
    print("=== TESTS DE utils.py ===\n")

    # Test password
    pwd = generar_password()
    print("✔ Password generado:", pwd)
    assert len(pwd) >= 8

    # Test estadísticas
    class FakeTarea:
        def __init__(self, estado: str) -> None:
            self.estado = estado

    tareas = [
        FakeTarea("pendiente"),
        FakeTarea("finalizada"),
        FakeTarea("pendiente"),
    ]

    stats = calcular_estadisticas_tareas(tareas)
    print("✔ Estadísticas:", stats)
    assert stats["total"] == 3
    assert stats["finalizadas"] == 1
    assert stats["pendientes"] == 2

    # Test búsqueda
    class FakeUsuario:
        def __init__(self, nombre: str) -> None:
            self.nombre = nombre

    usuarios = [FakeUsuario("alice"), FakeUsuario("bob")]
    u = buscar_usuario_por_nombre(usuarios, "alice")
    assert u is not None
    assert u.nombre == "alice"
    print("✔ Búsqueda de usuario OK")

    # Test persistencia pickle
    path = "test.pkl"
    guardar_datos(path, usuarios)
    usuarios_cargados = cargar_datos(path)
    assert len(usuarios_cargados) == 2
    print("✔ Persistencia pickle OK")

    print("\n=== TODOS LOS TESTS PASARON ✅ ===")
