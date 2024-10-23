from wtforms.validators import ValidationError

def validar_nombre(nombre):
    if len(nombre) < 5 or len(nombre) > 100:
        return 'El nombre debe tener entre 5 y 100 caracteres.'
    return None

def validar_categoria(genero):
    if len(genero) < 5 or len(genero) > 30:
        return 'La categoría debe tener entre 5 y 30 caracteres.'
    return None

class LibroCQRS:
    def __init__(self, dao):
        self.dao = dao

    def insertar_libro(self, nombre, autor, genero, estatus, archivo):
        error = validar_nombre(nombre)
        if error:
            raise ValidationError(error)

        error = validar_categoria(genero)
        if error:
            raise ValidationError(error)

        self.dao.insertar_libro(nombre, autor, genero, estatus, archivo)

    def obtener_todos_los_libros(self):
        return self.dao.obtener_todos_los_libros()

    def obtener_libro_por_id(self, id_libro):
        return self.dao.obtener_libro_por_id(id_libro)

    def eliminar_libro(self, id_libro):
        self.dao.eliminar_libro(id_libro)

    def actualizar_libro(self, id_libro, nombre, autor, genero, estatus, archivo):
        error = validar_nombre(nombre)
        if error:
            raise ValidationError(error)

        error = validar_categoria(genero)
        if error:
            raise ValidationError(error)

        self.dao.actualizar_libro(id_libro, nombre, autor, genero, estatus, archivo)
