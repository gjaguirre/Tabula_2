from __future__ import annotations

import os
import sys
import getpass
from typing import Optional
from core import GestorTareas


def limpiar_pantalla() -> None:
    """Limpia la pantalla según el sistema operativo."""
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def pedir_password(prompt: str = "Password: ") -> str:
    """Usa getpass para leer contraseñas sin mostrarlas."""
    try:
        return getpass.getpass(prompt)
    except Exception:
        # Fallback si getpass falla
        return input(prompt)


def flujo_crear_admin(gestor: GestorTareas) -> None:
    """Forzar creación de un administrador inicial."""
    print("No existe un administrador. Crea la cuenta de admin inicial.")
    while True:
        nombre = input("Username admin: ").strip()
        nombre_visible = input("Nombre visible: ").strip()
        pwd = pedir_password("Password: ")
        pwd2 = pedir_password("Confirmar password: ")
        if pwd != pwd2:
            print("Las contraseñas no coinciden. Intenta otra vez.")
            continue
        try:
            gestor.crear_usuario(nombre, nombre_visible, "admin", pwd)
            print("Administrador creado correctamente.")
            break
        except Exception as e:
            print(f"Error: {e}")


def login(gestor: GestorTareas) -> Optional[object]:
    """Pide credenciales y autentica al usuario; 3 intentos permitidos."""
    intentos = 0
    while intentos < 3:
        nombre = input("Username: ").strip()
        pwd = pedir_password()
        try:
            usuario = gestor.autenticar_usuario(nombre, pwd)
            print(f"Bienvenido {usuario.nombre_visible}!")
            return usuario
        except Exception as e:
            print(f"Error: {e}")
            intentos += 1
    print("Demasiados intentos fallidos. Saliendo.")
    return None


def menu_admin(gestor: GestorTareas, usuario_actual) -> None:
    while True:
        print("\n-- MENU ADMIN --")
        print(
            "1. Ver usuarios\n"
            "2. Crear usuario\n"
            "3. Resetear password de usuario\n"
            "4. Crear tarea\n"
            "5. Asignar tarea\n"
            "6. Ver tareas\n"
            "7. Ver estadísticas\n"
            "0. Logout"
        )
        opcion = input("Opción: ").strip()
        try:
            if opcion == "1":
                usuarios = gestor.listar_usuarios()
                for u in usuarios:
                    print(f"- {u['nombre_visible']} ({u['nombre']}) - rol: {u['rol']}")

            elif opcion == "2":
                nombre = input("Username: ")
                visible = input("Nombre visible: ")
                rol = input("Rol (user/admin): ") or "user"
                pwd = pedir_password("Password (opcional): ") or None
                gestor.crear_usuario(nombre, visible, rol, pwd)
                print("Usuario creado.")

            elif opcion == "3":
                objetivo = input("Username a resetear: ")
                gestor.resetear_password_usuario(usuario_actual, objetivo)
                print("Password reseteada (ahora debe definir una nueva al iniciar sesión).")

            elif opcion == "4":
                nombre = input("Nombre tarea: ")
                desc = input("Descripción: ")
                gestor.crear_tarea(nombre, desc)
                print("Tarea creada.")

            elif opcion == "5":
                u = input("Usuario: ")
                t = input("Tarea: ")
                gestor.asignar_usuario_tarea(u, t)
                print("Usuario asignado.")

            elif opcion == "6":
                gestor.listar_tareas()

            elif opcion == "7":
                stats = gestor.ver_estadisticas()
                print("Estadísticas:", stats)

            elif opcion == "0":
                print("Logout...")
                break

            else:
                print("Opción inválida.")
        except (ValueError, PermissionError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")


def menu_usuario(gestor: GestorTareas, usuario_actual) -> None:
    while True:
        print("\n-- MENU USUARIO --")
        print(
            "1. Ver mis tareas\n"
            "2. Agregar comentario a tarea\n"
            "3. Finalizar tarea\n"
            "4. Ver perfil\n"
            "0. Logout"
        )
        opcion = input("Opción: ").strip()
        try:
            if opcion == "1":
                tareas = gestor.obtener_tareas_usuario(usuario_actual.nombre)
                if not tareas:
                    print("No tienes tareas asignadas.")
                else:
                    for t in tareas:
                        print("-" * 30)
                        print(t.obtener_info_detallada())

            elif opcion == "2":
                t = input("Nombre tarea: ")
                texto = input("Comentario: ")
                gestor.agregar_comentario_tarea(t, texto, usuario_actual.nombre)
                print("Comentario agregado.")

            elif opcion == "3":
                t = input("Nombre tarea a finalizar: ")
                gestor.finalizar_tarea(t)
                print("Tarea finalizada.")

            elif opcion == "4":
                print(usuario_actual.to_json())

            elif opcion == "0":
                print("Logout...")
                break

            else:
                print("Opción inválida.")
        except (ValueError, PermissionError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")


def main() -> None:
    gestor = GestorTareas()

    limpiar_pantalla()
    print("=== Bienvenido al sistema Tabula_2 ===")

    if not gestor.existe_admin():
        flujo_crear_admin(gestor)

    usuario_actual = login(gestor)
    if usuario_actual is None:
        sys.exit(1)

    # Menú según rol
    try:
        if usuario_actual.es_admin():
            menu_admin(gestor, usuario_actual)
        else:
            menu_usuario(gestor, usuario_actual)
    except KeyboardInterrupt:
        print("\nSaliendo...")


if __name__ == "__main__":
    main()
