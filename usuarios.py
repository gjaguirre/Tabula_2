from __future__ import annotations

import bcrypt
import json
from datetime import datetime
from typing import Optional, Dict, Any
from uuid import uuid4


class Usuario:
    """
    Representa un usuario del sistema con autenticación segura.
    """

    def __init__(
        self,
        nombre: str,
        nombre_visible: str,
        rol: str = "user",
        password: Optional[str] = None,
        user_id: Optional[str] = None,
        fecha_creacion: Optional[datetime] = None,
    ) -> None:
        """
        Inicializa un usuario.

        Args:
            nombre (str): Username único (usado para login).
            nombre_visible (str): Nombre mostrado en la interfaz.
            rol (str): Rol del usuario ('user' o 'admin').
            password (Optional[str]): Contraseña inicial (opcional).
            user_id (Optional[str]): ID del usuario (UUID).
            fecha_creacion (Optional[datetime]): Fecha de creación.
        """
        if not nombre:
            raise ValueError("El nombre de usuario no puede estar vacío.")

        if rol not in ("user", "admin"):
            raise ValueError("El rol debe ser 'user' o 'admin'.")

        self.id: str = user_id or str(uuid4())
        self.nombre: str = nombre
        self.nombre_visible: str = nombre_visible
        self.rol: str = rol
        self.fecha_creacion: datetime = fecha_creacion or datetime.now()

        self.password_hash: Optional[bytes] = None
        if password is not None:
            self.cambiar_password(password)

    # -------------------------
    # Seguridad y autenticación
    # -------------------------

    def verificar_password(self, password: str) -> bool:
        """
        Verifica si la contraseña es correcta.

        Args:
            password (str): Contraseña a verificar.

        Returns:
            bool: True si es correcta, False si no.

        Raises:
            ValueError: Si el usuario no tiene contraseña configurada.
        """
        if self.password_hash is None:
            raise ValueError("El usuario no tiene contraseña configurada.")

        return bcrypt.checkpw(password.encode("utf-8"), self.password_hash)

    def cambiar_password(self, nueva_password: str) -> None:
        """
        Cambia la contraseña del usuario.

        Args:
            nueva_password (str): Nueva contraseña.

        Raises:
            ValueError: Si la contraseña es inválida.
        """
        if not nueva_password:
            raise ValueError("La contraseña no puede estar vacía.")

        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(
            nueva_password.encode("utf-8"),
            salt,
        )

    def resetear_password(self) -> None:
        """
        Resetea la contraseña del usuario (la deja en None).
        Usado para recuperación de contraseña.
        """
        self.password_hash = None

    # -------------------------
    # Roles
    # -------------------------

    def es_admin(self) -> bool:
        """
        Indica si el usuario es administrador.

        Returns:
            bool: True si es admin.
        """
        return self.rol == "admin"

    # -------------------------
    # Serialización
    # -------------------------

    def to_dict(self) -> Dict[str, Any]:
        """
        Serializa el usuario a un diccionario.

        Returns:
            Dict[str, Any]: Representación serializable del usuario.
        """
        return {
            "id": self.id,
            "nombre": self.nombre,
            "nombre_visible": self.nombre_visible,
            "rol": self.rol,
            "password_hash": self.password_hash.decode("utf-8")
            if self.password_hash is not None
            else None,
            "fecha_creacion": self.fecha_creacion.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Usuario:
        """
        Crea un usuario a partir de un diccionario.

        Args:
            data (Dict[str, Any]): Datos del usuario.

        Returns:
            Usuario: Instancia reconstruida.
        """
        usuario = cls(
            nombre=data["nombre"],
            nombre_visible=data["nombre_visible"],
            rol=data["rol"],
            password=None,
            user_id=data["id"],
            fecha_creacion=datetime.fromisoformat(data["fecha_creacion"]),
        )

        if data["password_hash"] is not None:
            usuario.password_hash = data["password_hash"].encode("utf-8")

        return usuario

    def to_json(self) -> str:
        """
        Serializa el usuario a JSON.

        Returns:
            str: JSON del usuario.
        """
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

    @classmethod
    def from_json(cls, data: str) -> Usuario:
        """
        Crea un usuario a partir de un JSON.

        Args:
            data (str): JSON del usuario.

        Returns:
            Usuario: Instancia reconstruida.
        """
        return cls.from_dict(json.loads(data))

    # -------------------------
    # Representación
    # -------------------------

    def __str__(self) -> str:
        return f"{self.nombre_visible} ({self.nombre}) - rol: {self.rol}"


# ==========================================================
# Tests y ejemplos de uso
# ==========================================================

if __name__ == "__main__":
    print("=== INICIANDO TESTS DE USUARIO ===\n")

    # Crear usuario sin contraseña
    usuario = Usuario(
        nombre="jdoe",
        nombre_visible="John Doe",
    )

    print("✔ Usuario creado sin contraseña")
    assert usuario.password_hash is None

    # Forzar error al verificar sin password
    try:
        usuario.verificar_password("1234")
        raise AssertionError("Debería haber fallado")
    except ValueError:
        print("✔ Error correcto al verificar sin contraseña")

    # Asignar contraseña
    usuario.cambiar_password("secreta123")
    print("✔ Contraseña asignada")

    assert usuario.verificar_password("secreta123") is True
    assert usuario.verificar_password("otra") is False
    print("✔ Verificación de contraseña correcta")

    # Resetear contraseña
    usuario.resetear_password()
    print("✔ Contraseña reseteada")
    assert usuario.password_hash is None

    # Crear admin
    admin = Usuario(
        nombre="admin",
        nombre_visible="Administrador",
        rol="admin",
        password="admin123",
    )

    assert admin.es_admin() is True
    print("✔ Usuario admin detectado correctamente")

    # Serialización
    json_data = admin.to_json()
    print("\nJSON generado:")
    print(json_data)

    usuario_copiado = Usuario.from_json(json_data)
    assert usuario_copiado.verificar_password("admin123") is True
    print("✔ Serialización y deserialización correctas")

    print("\n=== TODOS LOS TESTS PASARON ✅ ===")
