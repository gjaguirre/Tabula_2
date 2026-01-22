from __future__ import annotations

import os
import sys
from typing import Optional

from core import GestorTareas

from rich.console import Console
from rich.theme import Theme
from rich.panel import Panel
from rich.align import Align
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.text import Text


class InterfazConsola:
    """Interfaz de usuario basada en Rich para el CLI.

    Encapsula la Console, estilos y helpers para entradas y salidas.
    """

    def __init__(self) -> None:
        theme = Theme(
            {
                "success": "green",
                "error": "red",
                "warning": "yellow",
                "title": "bold blue",
            }
        )
        self.console = Console(theme=theme)

    def limpiar_pantalla(self) -> None:
        """Limpia la pantalla según el sistema operativo."""
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

    def pedir_texto(self, mensaje: str, default: Optional[str] = None) -> str:
        """Pide una entrada de texto usando Prompt.ask."""
        return Prompt.ask(f"[title]{mensaje}[/title]", default=default)

    def pedir_password(self, mensaje: str = "Password") -> str:
        """Pide una contraseña enmascarada usando Prompt.ask(password=True)."""
        return Prompt.ask(f"[title]{mensaje}[/title]", password=True)

    def confirmar(self, mensaje: str) -> bool:
        """Pregunta sí/no al usuario."""
        return Confirm.ask(f"[warning]{mensaje}[/warning]")

    def mostrar_titulo(self, texto: str) -> None:
        self.console.print(Align.center(Panel(Text(texto, style="title"), expand=False)))

    def mostrar_info(self, texto: str) -> None:
        self.console.print(f"[success]✅ {texto}[/success]")

    def mostrar_error(self, texto: str) -> None:
        self.console.print(f"[error]❌ {texto}[/error]")

    def mostrar_warning(self, texto: str) -> None:
        self.console.print(f"[warning]⚠️ {texto}[/warning]")

    def mostrar_panel_bienvenida(self, usuario) -> None:
        body = Text()
        body.append(f"Usuario: {usuario.nombre_visible}\n", style="title")
        body.append(f"Rol: {usuario.rol}\n")
        self.console.print(Panel(Align.center(body), title="Bienvenido"))

    def mostrar_usuarios(self, usuarios: list[dict]) -> None:
        table = Table(title="Usuarios")
        table.add_column("Nombre visible", style="cyan")
        table.add_column("Username")
        table.add_column("Rol")
        table.add_column("Creado")
        for u in usuarios:
            table.add_row(u.get("nombre_visible", ""), u.get("nombre", ""), u.get("rol", ""), u.get("fecha_creacion", ""))
        self.console.print(table)

    def mostrar_tareas(self, tareas: list) -> None:
        table = Table(title="Tareas")
        table.add_column("Nombre", style="magenta")
        table.add_column("Estado")
        table.add_column("Creada")
        table.add_column("Usuarios asignados")
        for t in tareas:
            usuarios = ", ".join([u["nombre_visible"] for u in t.get("usuarios_asignados", [])])
            table.add_row(t.get("nombre", ""), t.get("estado", ""), t.get("fecha_creacion", ""), usuarios)
        self.console.print(table)


def flujo_crear_admin(gestor: GestorTareas, ui: InterfazConsola) -> None:
    ui.console.print(Panel("No existe un administrador. Crea la cuenta de admin inicial.", title="Atención"))
    while True:
        nombre = ui.pedir_texto("Username admin")
        nombre_visible = ui.pedir_texto("Nombre visible")
        pwd = ui.pedir_password("Password")
        pwd2 = ui.pedir_password("Confirmar password")
        if pwd != pwd2:
            ui.mostrar_error("Las contraseñas no coinciden. Intenta otra vez.")
            continue
        try:
            gestor.crear_usuario(nombre, nombre_visible, "admin", pwd)
            ui.mostrar_info("Administrador creado correctamente.")
            break
        except Exception as e:
            ui.mostrar_error(str(e))


def login(gestor: GestorTareas, ui: InterfazConsola) -> Optional[object]:
    """Flujo de login con 3 intentos. Maneja usuarios sin contraseña inicial."""
    intentos = 0
    while intentos < 3:
        nombre = ui.pedir_texto("Username")
        usuario = gestor.usuarios.get(nombre)
        if not usuario:
            ui.mostrar_error("Usuario inexistente.")
            intentos += 1
            continue

        # Si el usuario no tiene contraseña, forzamos configuración
        if getattr(usuario, "password_hash", None) is None:
            ui.console.print(Panel("Se requiere configurar contraseña inicial.", title="Configurar contraseña"))
            pwd = ui.pedir_password("Nueva password")
            pwd2 = ui.pedir_password("Confirmar password")
            if pwd != pwd2:
                ui.mostrar_error("Las contraseñas no coinciden.")
                intentos += 1
                continue
            try:
                usuario.cambiar_password(pwd)
                gestor._guardar_todo()
                ui.mostrar_info("Contraseña establecida. Ahora puedes iniciar sesión.")
                continue
            except Exception as e:
                ui.mostrar_error(str(e))
                intentos += 1
                continue

        pwd = ui.pedir_password("Password")
        try:
            usuario = gestor.autenticar_usuario(nombre, pwd)
            ui.mostrar_info(f"Bienvenido {usuario.nombre_visible}!")
            return usuario
        except Exception as e:
            ui.mostrar_error(str(e))
            intentos += 1

    ui.mostrar_error("Demasiados intentos fallidos. Saliendo.")
    return None


def menu_admin(gestor: GestorTareas, usuario_actual, ui: InterfazConsola) -> None:
    while True:
        opciones = "\n".join([
            "1. Ver usuarios",
            "2. Crear usuario",
            "3. Resetear password de usuario",
            "4. Crear tarea",
            "5. Asignar tarea",
            "6. Ver tareas",
            "7. Ver estadísticas",
            "0. Logout",
        ])
        ui.console.print(Panel(Align.center(Text(opciones)), title="MENU ADMIN"))
        opcion = ui.pedir_texto("Opción")
        try:
            if opcion == "1":
                usuarios = gestor.listar_usuarios()
                ui.mostrar_usuarios(usuarios)

            elif opcion == "2":
                nombre = ui.pedir_texto("Username")
                visible = ui.pedir_texto("Nombre visible")
                rol = ui.pedir_texto("Rol (user/admin)", default="user")
                pwd = ui.pedir_password("Password (opcional)") or None
                gestor.crear_usuario(nombre, visible, rol, pwd)
                ui.mostrar_info("Usuario creado.")

            elif opcion == "3":
                objetivo = ui.pedir_texto("Username a resetear")
                gestor.resetear_password_usuario(usuario_actual, objetivo)
                ui.mostrar_info("Password reseteada (ahora debe definir una nueva al iniciar sesión).")

            elif opcion == "4":
                nombre = ui.pedir_texto("Nombre tarea")
                desc = ui.pedir_texto("Descripción")
                gestor.crear_tarea(nombre, desc)
                ui.mostrar_info("Tarea creada.")

            elif opcion == "5":
                u = ui.pedir_texto("Usuario")
                t = ui.pedir_texto("Tarea")
                gestor.asignar_usuario_tarea(u, t)
                ui.mostrar_info("Usuario asignado.")

            elif opcion == "6":
                tareas = [t.obtener_detalle() for t in gestor.tareas.values()]
                ui.mostrar_tareas(tareas)

            elif opcion == "7":
                stats = gestor.ver_estadisticas()
                ui.console.print(Panel(Text(str(stats)), title="Estadísticas"))

            elif opcion == "0":
                ui.mostrar_info("Logout...")
                break

            else:
                ui.mostrar_warning("Opción inválida.")
        except (ValueError, PermissionError) as e:
            ui.mostrar_error(str(e))
        except Exception as e:
            ui.mostrar_error(f"Error inesperado: {e}")


def menu_usuario(gestor: GestorTareas, usuario_actual, ui: InterfazConsola) -> None:
    while True:
        opciones = "\n".join([
            "1. Ver mis tareas",
            "2. Agregar comentario a tarea",
            "3. Finalizar tarea",
            "4. Ver perfil",
            "0. Logout",
        ])
        ui.console.print(Panel(Align.center(Text(opciones)), title="MENU USUARIO"))
        opcion = ui.pedir_texto("Opción")
        try:
            if opcion == "1":
                tareas = [t.obtener_detalle() for t in gestor.obtener_tareas_usuario(usuario_actual.nombre)]
                if not tareas:
                    ui.mostrar_info("No tienes tareas asignadas.")
                else:
                    ui.mostrar_tareas(tareas)

            elif opcion == "2":
                t = ui.pedir_texto("Nombre tarea")
                texto = ui.pedir_texto("Comentario")
                gestor.agregar_comentario_tarea(t, texto, usuario_actual.nombre)
                ui.mostrar_info("Comentario agregado.")

            elif opcion == "3":
                t = ui.pedir_texto("Nombre tarea a finalizar")
                gestor.finalizar_tarea(t)
                ui.mostrar_info("Tarea finalizada.")

            elif opcion == "4":
                ui.console.print(Panel(Text(usuario_actual.to_json()), title="Perfil"))

            elif opcion == "0":
                ui.mostrar_info("Logout...")
                break

            else:
                ui.mostrar_warning("Opción inválida.")
        except (ValueError, PermissionError) as e:
            ui.mostrar_error(str(e))
        except Exception as e:
            ui.mostrar_error(f"Error inesperado: {e}")


def main() -> None:
    ui = InterfazConsola()
    gestor = GestorTareas()

    ui.limpiar_pantalla()
    ui.mostrar_titulo("Bienvenido al sistema Tabula_2")

    if not gestor.existe_admin():
        flujo_crear_admin(gestor, ui)

    usuario_actual = login(gestor, ui)
    if usuario_actual is None:
        sys.exit(1)

    ui.mostrar_panel_bienvenida(usuario_actual)

    try:
        if usuario_actual.es_admin():
            menu_admin(gestor, usuario_actual, ui)
        else:
            menu_usuario(gestor, usuario_actual, ui)
    except KeyboardInterrupt:
        ui.mostrar_info("Saliendo...")


if __name__ == "__main__":
    main()
