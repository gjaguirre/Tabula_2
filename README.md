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

**CLI (main.py) — Uso y pruebas**

Este proyecto ahora incluye un punto de entrada CLI `main.py` que utiliza el controlador `GestorTareas`.

- Ejecutar el CLI (activar venv primero o usar el python del venv):
```powershell
cd "c:\Users\gusta\Desktop\Taller_jueves_260108\Tabula_2"
.\.venv\Scripts\Activate.ps1
python main.py
```

- Ejecutar sin activar el venv:
```powershell
C:\Users\gusta\Desktop\Taller_jueves_260108\Tabula_2\.venv\Scripts\python.exe main.py
```

- Nota sobre redirecciones en PowerShell: la sintaxis `< file` no siempre funciona; usa `type file | python main.py` o ejecuta desde `cmd.exe` si necesitas `python main.py < inputs.txt`.

**Simulación automatizada de flujo (testing local)**

Para pruebas no interactivas (el CLI usa `getpass` para contraseñas y requiere TTY), hay un runner de simulación disponible:

- `run_cli_sim.py` lee las secuencias de entrada en `cli_inputs_admin.txt` y `cli_inputs_user.txt` y sustituye `input()` y `getpass.getpass()` para permitir pruebas automatizadas.

Ejecutar la simulación:
```powershell
C:\Users\gusta\Desktop\Taller_jueves_260108\Tabula_2\.venv\Scripts\python.exe run_cli_sim.py
```

**Estado persistente y reinicios**

- Los datos se guardan en `usuarios.dat` y `tareas.dat` (pickle) y el histórico en `tareas_finalizadas.json`.
- Para forzar el flujo de creación del administrador inicial borra los ficheros:
```powershell
Remove-Item usuarios.dat,tareas.dat -ErrorAction SilentlyContinue
```

**Dependencias importantes**

- `bcrypt` es requerida para la gestión segura de contraseñas. Si tienes problemas con `ModuleNotFoundError: No module named 'bcrypt'` asegúrate de instalarla en el intérprete que uses:
```powershell
pip install bcrypt
# o, si no usas el venv
py -m pip install bcrypt
```

Si quieres que actualice `requirements.txt` para incluir `bcrypt`, indícamelo y lo añado y commiteo.

**Archivos relevantes**
- `main.py` — Punto de entrada CLI
- `core/` — Paquete que exporta `GestorTareas`
- `run_cli_sim.py` — Runner de simulación (no interactivo)
- `cli_inputs_admin.txt`, `cli_inputs_user.txt` — secuencias de ejemplo para la simulación

---

Si deseas, puedo añadir un workflow de GitHub Actions que ejecute `pytest` en cada push y/o añadir `bcrypt` a `requirements.txt` y hacer commit.
