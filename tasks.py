def _limpiar(texto, campo):
    """Valida que el texto sea un str no vacío y colapsa los espacios."""
    if not isinstance(texto, str):
        raise TypeError(f"El campo {campo} debe ser texto")
    texto = " ".join(texto.split())
    if not texto:
        raise ValueError(f"El campo {campo} es obligatorio")
    return texto


def _formatear(texto):
    """Deja solo la primera letra en mayúscula."""
    return texto.capitalize()


def _normalizar(texto):
    return " ".join(texto.split()).casefold()


def agregar_tarea(tareas, titulo, categoria):
    titulo = _formatear(_limpiar(titulo, "título"))
    categoria = _limpiar(categoria, "categoría")
    if any(c.isdigit() for c in categoria):
        raise ValueError("La categoría no puede contener números")
    categoria = _formatear(categoria)
    tarea = {
        "id": len(tareas) + 1,
        "titulo": titulo,
        "categoria": categoria,
        "completada": False,
    }
    tareas.append(tarea)
    return tarea


def completar_tarea(tareas, tarea_id):
    for tarea in tareas:
        if tarea["id"] == tarea_id:
            tarea["completada"] = True
            return tarea
    raise ValueError("Tarea no encontrada")


def pendientes(tareas, categoria=None):
    resultado = [t for t in tareas if not t["completada"]]
    if categoria is None:
        return resultado
    buscada = _normalizar(categoria)
    return [t for t in resultado if _normalizar(t.get("categoria", "")) == buscada]
