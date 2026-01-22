# Tabula_2

Pequeño proyecto de gestión de tareas.

Descripción
- Scripts para gestionar tareas y usuarios.

Archivos principales
- `gestor_tareas.py`
- `tareas.py`
- `usuarios.py`
- `utils.py`
- `requirements.txt`

Requisitos
- Python 3.8+
- Instalar dependencias: `pip install -r requirements.txt`

Uso (Windows PowerShell)
```powershell
cd "c:\Users\gusta\Desktop\Taller_jueves_260108\Tabula_2"
python gestor_tareas.py
```

Entorno virtual (recomendado)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Licencia
- Añade una licencia si lo deseas.

**Tests y entorno**

Sigue estos pasos para crear un entorno reproducible e ejecutar la suite de tests con `pytest` (Windows PowerShell):

```powershell
cd "c:\Users\gusta\Desktop\Taller_jueves_260108\Tabula_2"

# Crear y activar entorno virtual (recomendado)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Actualizar pip e instalar dependencias
python -m pip install --upgrade pip
pip install -r requirements.txt

# Instalar pytest si no está en requirements
pip install pytest

# Ejecutar tests
python -m pytest -q
```

Notas:
- Si usas otra shell (cmd.exe, WSL, bash) adapta el comando de activación.
- Los tests están en la carpeta `tests/`.
- Para integración continua, puedes añadir un workflow de GitHub Actions que ejecute `pytest` en cada push.
