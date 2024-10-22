class LibroDAO:
    def __init__(self, mysql):
        self.mysql = mysql

    def insertar_libro(self, nombre, autor, genero, estatus, archivo):
        cur = self.mysql.connection.cursor()
        cur.execute(
            "INSERT INTO libros (nombre, autor, genero, estatus, archivo) VALUES (%s, %s, %s, %s, %s)",
            (nombre, autor, genero, estatus, archivo)
        )
        self.mysql.connection.commit()
        cur.close()

    def obtener_todos_los_libros(self):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM libros")
        libros = cur.fetchall()
        cur.close()
        return libros

    def obtener_libro_por_id(self, id_libro):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM libros WHERE id_libro = %s", (id_libro,))
        libro = cur.fetchone()
        cur.close()
        return libro

    def eliminar_libro(self, id_libro):
        cur = self.mysql.connection.cursor()
        cur.execute("DELETE FROM libros WHERE id_libro = %s", (id_libro,))
        self.mysql.connection.commit()
        cur.close()

    def actualizar_libro(self, id_libro, nombre, autor, genero, estatus, archivo):
        cur = self.mysql.connection.cursor()
        cur.execute(
            """UPDATE libros SET nombre = %s, autor = %s, genero = %s, estatus = %s, archivo = %s 
            WHERE id_libro = %s""",
            (nombre, autor, genero, estatus, archivo, id_libro)
        )
        self.mysql.connection.commit()
        cur.close()
