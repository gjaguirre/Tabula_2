from __future__ import annotations

import os
from typing import Dict, Optional

from usuarios import Usuario
from tareas import Tarea
import utils


class GestorTareas:
    """
    Controlador principal del sistema de gestión de tareas.

    Coordina usuarios, tareas, persistencia y reglas de negocio.
    """

    def __init__(self) -> None:
        """
        Inicializa el gestor y carga los datos desde disco.
        Las rutas se calculan automáticamente desde el directorio del proyecto.
        """
        base_dir = os.path.dirname(os.path.abspath(__file__))

        self._usuarios_path = os.path.join(base_dir, "usuarios.dat")
        self._tareas_path = os.path.join(base_dir, "tareas.dat")
        self._historico_path = os.path.join(base_dir, "tareas_finalizadas.json")

        self.usuarios: Dict[str, Usuario] = {
            u.nombre: u for u in utils.cargar_datos(self._usuarios_path)
        }
        self.tareas: Dict[str, Tarea] = {
            t.nombre: t for t in utils.cargar_datos(self._tareas_path)
        }

    # ==================================================
    # Persistencia
    # ==================================================

    def _guardar_todo(self) -> None:
        """Guarda usuarios y tareas en disco."""
        utils.guardar_datos(self._usuarios_path, list(self.usuarios.values()))
        utils.guardar_datos(self._tareas_path, list(self.tareas.values()))

    # ==================================================
    # Usuarios
    # ==================================================

    def crear_usuario(
        self,
        nombre: str,
        nombre_visible: str,
        rol: str = "user",
        password: Optional[str] = None,
    ) -> Usuario:
        """
        Crea un nuevo usuario.

        Raises:
            ValueError: Si el nombre ya existe.
        """
        if nombre in self.usuarios:
            raise ValueError("Ya existe un usuario con ese nombre.")

        usuario = Usuario(
            nombre=nombre,
            nombre_visible=nombre_visible,
            rol=rol,
            password=password,
        )

        self.usuarios[nombre] = usuario
        self._guardar_todo()
        return usuario

    def autenticar_usuario(self, nombre: str, password: str) -> Usuario:
        """
        Autentica un usuario por nombre y contraseña.

        Raises:
            ValueError: Si las credenciales son inválidas.
        """
        usuario = self.usuarios.get(nombre)
        if not usuario:
            raise ValueError("Usuario inexistente.")

        if not usuario.verificar_password(password):
            raise ValueError("Contraseña incorrecta.")

        return usuario

    def resetear_password_usuario(
        self,
        admin: Usuario,
        nombre_usuario: str,
    ) -> None:
        """
        Resetea la contraseña de un usuario (solo admin).

        Raises:
            PermissionError: Si el solicitante no es admin.
        """
        if not admin.es_admin():
            raise PermissionError("Solo un admin puede resetear contraseñas.")

        usuario = self.usuarios.get(nombre_usuario)
        if not usuario:
            raise ValueError("Usuario inexistente.")

        usuario.resetear_password()
        self._guardar_todo()

    # ==================================================
    # Tareas
    # ==================================================

    def crear_tarea(self, nombre: str, descripcion: str) -> Tarea:
        """
        Crea una nueva tarea.

        Raises:
            ValueError: Si el nombre ya existe.
        """
        if nombre in self.tareas:
            raise ValueError("Ya existe una tarea con ese nombre.")

        tarea = Tarea(nombre=nombre, descripcion=descripcion)
        self.tareas[nombre] = tarea
        self._guardar_todo()
        return tarea

    def asignar_usuario_tarea(self, nombre_usuario: str, nombre_tarea: str) -> None:
        """
        Asigna un usuario a una tarea existente.
        """
        usuario = self.usuarios.get(nombre_usuario)
        tarea = self.tareas.get(nombre_tarea)

        if not usuario or not tarea:
            raise ValueError("Usuario o tarea inexistente.")

        tarea.agregar_usuario(usuario)
        self._guardar_todo()

    def finalizar_tarea(self, nombre_tarea: str) -> None:
        """
        Finaliza una tarea y la guarda en el histórico JSON.
        """
        tarea = self.tareas.get(nombre_tarea)
        if not tarea:
            raise ValueError("Tarea inexistente.")

        tarea.cambiar_estado("finalizada")

        historico = utils.leer_json(self._historico_path, default=[])
        historico.append(tarea.obtener_detalle())
        utils.escribir_json(self._historico_path, historico)

        self._guardar_todo()

    def eliminar_tarea(self, nombre_tarea: str) -> None:
        """
        Elimina una tarea solo si está finalizada.
        """
        tarea = self.tareas.get(nombre_tarea)
        if not tarea:
            raise ValueError("Tarea inexistente.")

        if tarea.estado != "finalizada":
            raise ValueError("Solo se pueden eliminar tareas finalizadas.")

        del self.tareas[nombre_tarea]
        self._guardar_todo()

    # ==================================================
    # Consulta
    # ==================================================

    def listar_tareas(self) -> None:
        """Imprime todas las tareas."""
        if not self.tareas:
            print("No hay tareas.")
            return

        for tarea in self.tareas.values():
            print("-" * 40)
            print(tarea.obtener_info_detallada())


# ======================================================
# Interfaz simple de consola
# ======================================================

def menu() -> None:
    gestor = GestorTareas()

    print("=== SISTEMA DE GESTIÓN DE TAREAS ===")

    while True:
        print(
            "\n1. Crear usuario\n"
            "2. Crear tarea\n"
            "3. Asignar usuario a tarea\n"
            "4. Finalizar tarea\n"
            "5. Eliminar tarea\n"
            "6. Listar tareas\n"
            "0. Salir"
        )

        opcion = input("Opción: ").strip()

        try:
            if opcion == "1":
                nombre = input("Username: ")
                visible = input("Nombre visible: ")
                rol = input("Rol (user/admin): ") or "user"
                password = input("Password (opcional): ") or None
                gestor.crear_usuario(nombre, visible, rol, password)
                print("Usuario creado.")

            elif opcion == "2":
                nombre = input("Nombre tarea: ")
                desc = input("Descripción: ")
                gestor.crear_tarea(nombre, desc)
                print("Tarea creada.")

            elif opcion == "3":
                u = input("Usuario: ")
                t = input("Tarea: ")
                gestor.asignar_usuario_tarea(u, t)
                print("Usuario asignado.")

            elif opcion == "4":
                t = input("Tarea: ")
                gestor.finalizar_tarea(t)
                print("Tarea finalizada.")

            elif opcion == "5":
                t = input("Tarea: ")
                gestor.eliminar_tarea(t)
                print("Tarea eliminada.")

            elif opcion == "6":
                gestor.listar_tareas()

            elif opcion == "0":
                print("Saliendo...")
                break

            else:
                print("Opción inválida.")

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    menu()
