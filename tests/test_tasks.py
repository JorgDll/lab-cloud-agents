import unittest

from tasks import agregar_tarea, completar_tarea, pendientes


class TestTasks(unittest.TestCase):
    def test_agregar_tarea(self):
        tareas = []
        tarea = agregar_tarea(tareas, "Leer documentación", "Estudio")
        self.assertEqual(tarea["titulo"], "Leer documentación")
        self.assertFalse(tarea["completada"])

    def test_completar_tarea(self):
        tareas = []
        agregar_tarea(tareas, "Practicar", "Estudio")
        completar_tarea(tareas, 1)
        self.assertEqual(pendientes(tareas), [])

    def test_agregar_tarea_con_categoria(self):
        tareas = []
        tarea = agregar_tarea(tareas, "Preparar informe", "  Trabajo  ")
        self.assertEqual(tarea["categoria"], "Trabajo")
        self.assertEqual(tareas, [tarea])

    def test_agregar_tarea_categoria_vacia(self):
        tareas = []
        for categoria in ("", "   "):
            with self.subTest(categoria=repr(categoria)):
                with self.assertRaises(ValueError):
                    agregar_tarea(tareas, "Tarea", categoria)
        self.assertEqual(tareas, [])

    def test_agregar_tarea_sin_categoria(self):
        with self.assertRaises(TypeError):
            agregar_tarea([], "Tarea")

    def test_pendientes_filtra_por_categoria(self):
        tareas = []
        agregar_tarea(tareas, "A", "Trabajo")
        agregar_tarea(tareas, "B", "Estudio")
        agregar_tarea(tareas, "C", "Trabajo")
        titulos = [t["titulo"] for t in pendientes(tareas, "Trabajo")]
        self.assertEqual(titulos, ["A", "C"])

    def test_filtrado_sin_distinguir_mayusculas(self):
        tareas = []
        agregar_tarea(tareas, "A", "Trabajo")
        agregar_tarea(tareas, "B", "Estudio")
        for categoria in ("trabajo", "TRABAJO", "Trabajo", " tRaBaJo "):
            with self.subTest(categoria=categoria):
                titulos = [t["titulo"] for t in pendientes(tareas, categoria)]
                self.assertEqual(titulos, ["A"])

    def test_filtrado_excluye_completadas(self):
        tareas = []
        agregar_tarea(tareas, "A", "Trabajo")
        agregar_tarea(tareas, "B", "Trabajo")
        completar_tarea(tareas, 1)
        titulos = [t["titulo"] for t in pendientes(tareas, "trabajo")]
        self.assertEqual(titulos, ["B"])

    def test_filtrado_categoria_inexistente(self):
        tareas = []
        agregar_tarea(tareas, "A", "Trabajo")
        self.assertEqual(pendientes(tareas, "Hogar"), [])

    def test_pendientes_sin_categoria(self):
        tareas = []
        agregar_tarea(tareas, "A", "Trabajo")
        agregar_tarea(tareas, "B", "Estudio")
        self.assertEqual(len(pendientes(tareas)), 2)

    def test_categoria_con_numeros(self):
        tareas = []
        for categoria in ("TrBbaj0", "Trabajo2", "123"):
            with self.subTest(categoria=categoria):
                with self.assertRaises(ValueError):
                    agregar_tarea(tareas, "Tarea", categoria)
        self.assertEqual(tareas, [])

    def test_titulo_vacio(self):
        for titulo in ("", "   "):
            with self.subTest(titulo=repr(titulo)):
                with self.assertRaises(ValueError):
                    agregar_tarea([], titulo, "Trabajo")

    def test_textos_no_str(self):
        with self.assertRaises(TypeError):
            agregar_tarea([], None, "Trabajo")
        with self.assertRaises(TypeError):
            agregar_tarea([], "Tarea", 123)

    def test_formato_primera_letra_mayuscula(self):
        tareas = []
        casos = [
            ("trabajo", "Trabajo"),
            ("TRABAJO", "Trabajo"),
            ("tRaBaJo", "Trabajo"),
            ("vida PERSONAL", "Vida personal"),
        ]
        for entrada, esperado in casos:
            with self.subTest(entrada=entrada):
                tarea = agregar_tarea(tareas, "Tarea", entrada)
                self.assertEqual(tarea["categoria"], esperado)

    def test_formato_titulo(self):
        tarea = agregar_tarea([], "  PREPARAR   el INFORME  ", "Trabajo")
        self.assertEqual(tarea["titulo"], "Preparar el informe")

    def test_limpieza_espacios_internos(self):
        tarea = agregar_tarea([], "Tarea", "  vida    personal ")
        self.assertEqual(tarea["categoria"], "Vida personal")

    def test_filtrado_tras_formateo(self):
        tareas = []
        agregar_tarea(tareas, "A", "TRABAJO")
        agregar_tarea(tareas, "B", "vida   personal")
        self.assertEqual([t["titulo"] for t in pendientes(tareas, "trabajo")], ["A"])
        self.assertEqual([t["titulo"] for t in pendientes(tareas, "VIDA PERSONAL")], ["B"])


if __name__ == "__main__":
    unittest.main()
