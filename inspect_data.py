from utils import cargar_datos, leer_json

print('usuarios.dat:')
usuarios = cargar_datos('usuarios.dat')
print(len(usuarios))
for u in usuarios:
    print(u.to_dict())

print('\ntareas.dat:')
tareas = cargar_datos('tareas.dat')
print(len(tareas))
for t in tareas:
    print(t.obtener_detalle())

print('\ntareas_finalizadas.json:')
print(leer_json('tareas_finalizadas.json', default=[]))
