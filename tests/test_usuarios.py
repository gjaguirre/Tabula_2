import pytest

from usuarios import Usuario


def test_usuario_password_flow():
    u = Usuario("testuser", "Test User")
    with pytest.raises(ValueError):
        u.verificar_password("x")

    u.cambiar_password("secret123")
    assert u.verificar_password("secret123") is True
    assert u.verificar_password("wrong") is False

    u.resetear_password()
    with pytest.raises(ValueError):
        u.verificar_password("secret123")


def test_serialization_and_admin_role():
    u = Usuario("admin", "Administrator", rol="admin", password="adm1n")
    data = u.to_dict()
    u2 = Usuario.from_dict(data)
    assert u2.nombre == u.nombre
    assert u2.es_admin() is True
    assert u2.verificar_password("adm1n") is True
