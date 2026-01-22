from __future__ import annotations

from datetime import datetime
from typing import List, Tuple, Dict, Any
import json

from usuarios import Usuario


class Tarea:
    """
    Representa una tarea dentro de un sistema de gestión.
    """

    def __init__(
        self,
        nombre: str,
        descripcion: str,
        usuarios_asignados: List[Usuario] | None = None,
    ) -> None:
        """
        Inicializa una nueva tarea.

        Args:
            nombre (str): Nombre o título de la tarea.
            descripcion (str): Descripción detallada.
            usuarios_asignados (List[Usuario] | None): Usuarios asignados.
        """
        if not nombre:
            raise ValueError("El nombre de la tarea no puede estar vacío.")

        self.nombre: str = nombre
        self.descripcion: str = descripcion
        self.estado: str = "pendiente"
        self.fecha_creacion: datetime = datetime.now()
        self.usuarios_asignados: List[Usuario] = usuarios_asignados or []
        self.comentarios: List[Tuple[str, Usuario, datetime]] = []

    # -------------------------
    # Métodos de negocio
    # -------------------------

    def agregar_usuario(self, usuario: Usuario) -> None:
        """
        Agrega un usuario a la tarea.
        """
        if usuario not in self.usuarios_asignados:
            self.usuarios_asignados.append(usuario)

    def quitar_usuario(self, usuario: Usuario) -> None:
        """
        Quita un usuario de la tarea.
        """
        if usuario in self.usuarios_asignados:
            self.usuarios_asignados.remove(usuario)

    def cambiar_estado(self, nuevo_estado: str) -> None:
        """
        Cambia el estado de la tarea.
        """
        if nuevo_estado not in ("pendiente", "finalizada"):
            raise ValueError("El estado debe ser 'pendiente' o 'finalizada'.")
        self.estado = nuevo_estado

    def agregar_comentario(self, texto: str, autor: Usuario) -> None:
        """
        Agrega un comentario a la tarea.

        Raises:
            ValueError: Si el autor no está asignado a la tarea.
        """
        if autor not in self.usuarios_asignados:
            raise ValueError("El autor debe ser un usuario asignado a la tarea.")

        self.comentarios.append((texto, autor, datetime.now()))

    # -------------------------
    # Información
    # -------------------------

    def obtener_detalle(self) -> Dict[str, Any]:
        """
        Obtiene el detalle completo de la tarea.
        """
        return {
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "estado": self.estado,
            "fecha_creacion": self.fecha_creacion.isoformat(),
            "usuarios_asignados": [
                usuario.to_dict() for usuario in self.usuarios_asignados
            ],
            "comentarios": [
                {
                    "texto": texto,
                    "autor": autor.to_dict(),
                    "fecha": fecha.isoformat(),
                }
                for texto, autor, fecha in self.comentarios
            ],
        }

    def obtener_info_detallada(self) -> str:
        """
        Devuelve un reporte formateado de la tarea.
        """
        lineas = [
            f"📌 TAREA: {self.nombre}",
            f"📝 Descripción: {self.descripcion}",
            f"📊 Estado: {self.estado}",
            f"📅 Creada el: {self.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')}",
            "👥 Usuarios asignados:",
        ]

        if not self.usuarios_asignados:
            lineas.append("  - Ninguno")
        else:
            for u in self.usuarios_asignados:
                lineas.append(f"  - {u}")

        lineas.append("\n💬 Comentarios:")

        if not self.comentarios:
            lineas.append("  - No hay comentarios.")
        else:
            for texto, autor, fecha in self.comentarios:
                lineas.append(
                    f"  - [{fecha.strftime('%Y-%m-%d %H:%M')}] "
                    f"{autor.nombre_visible}: {texto}"
                )

        return "\n".join(lineas)

    # -------------------------
    # Serialización
    # -------------------------

    def to_json(self) -> str:
        """
        Serializa la tarea a JSON.
        """
        return json.dumps(self.obtener_detalle(), ensure_ascii=False, indent=2)

    @classmethod
    def from_json(cls, data: str) -> Tarea:
        """
        Reconstruye una tarea desde JSON.
        """
        obj = json.loads(data)

        usuarios = [
            Usuario.from_dict(u) for u in obj["usuarios_asignados"]
        ]

        tarea = cls(
            nombre=obj["nombre"],
            descripcion=obj["descripcion"],
            usuarios_asignados=usuarios,
        )

        tarea.estado = obj["estado"]
        tarea.fecha_creacion = datetime.fromisoformat(obj["fecha_creacion"])

        for c in obj["comentarios"]:
            tarea.comentarios.append(
                (
                    c["texto"],
                    Usuario.from_dict(c["autor"]),
                    datetime.fromisoformat(c["fecha"]),
                )
            )

        return tarea


# ==========================================================
# Tests manuales
# ==========================================================

if __name__ == "__main__":
    print("=== TESTS DE TAREA CON USUARIO ===\n")

    alice = Usuario("alice", "Alice")
    bob = Usuario("bob", "Bob")

    tarea = Tarea(
        nombre="Refactor modelo",
        descripcion="Actualizar Tarea para usar Usuario",
    )

    tarea.agregar_usuario(alice)
    tarea.agregar_usuario(bob)

    tarea.agregar_comentario("Arranco yo", alice)
    tarea.cambiar_estado("finalizada")

    print(tarea.obtener_info_detallada())

    json_data = tarea.to_json()
    print("\nJSON generado:\n", json_data)

    tarea_copia = Tarea.from_json(json_data)
    print("\n=== TAREA RECONSTRUIDA ===")
    print(tarea_copia.obtener_info_detallada())

    print("\n=== TESTS OK ✅ ===")
