from tasks import agregar_tarea, completar_tarea, pendientes

tareas = []
agregar_tarea(tareas, "estudiar agentes cloud", "ESTUDIO")
agregar_tarea(tareas, "  Preparar   LABORATORIO ", "trabajo")
agregar_tarea(tareas, "revisar issue", "TrAbAjO")
agregar_tarea(tareas, "leer documentación", "estudio")
completar_tarea(tareas, 1)

try:
    agregar_tarea(tareas, "Tarea inválida", "TrBbaj0")
except ValueError as error:
    print(f"Error: {error}\n")

print("Pendientes:")
for tarea in pendientes(tareas):
    print(f'- {tarea["id"]}: {tarea["titulo"]} [{tarea["categoria"]}]')

print("\nPendientes de la categoría 'trabajo':")
for tarea in pendientes(tareas, "trabajo"):
    print(f'- {tarea["id"]}: {tarea["titulo"]} [{tarea["categoria"]}]')
