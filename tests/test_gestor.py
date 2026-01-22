from gestor_tareas import GestorTareas


def test_gestor_crud(tmp_path):
    gestor = GestorTareas()

    # Redirigir rutas a tmp_path para no contaminar el proyecto
    gestor._usuarios_path = str(tmp_path / "usuarios.dat")
    gestor._tareas_path = str(tmp_path / "tareas.dat")
    gestor._historico_path = str(tmp_path / "historico.json")

    gestor.usuarios.clear()
    gestor.tareas.clear()

    admin = gestor.crear_usuario("admin", "Admin", "admin", "adm123")
    user = gestor.crear_usuario("u1", "User One", "user", "u123")

    tarea = gestor.crear_tarea("t1", "Descripción")
    gestor.asignar_usuario_tarea("u1", "t1")
    gestor.finalizar_tarea("t1")

    # ahora se puede eliminar
    gestor.eliminar_tarea("t1")
    assert "t1" not in gestor.tareas
