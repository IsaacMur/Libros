class LibroViewModel:
    def __init__(self, libro):
        self.id_libro = libro[0]
        self.nombre = libro[1]
        self.autor = libro[2]
        self.genero = libro[3]
        self.estatus = libro[4]
        self.archivo_url = f"/ver_pdf/{libro[0]}" 

    def to_json(self):
        return {
            "id_libro": self.id_libro,
            "nombre": self.nombre,
            "autor": self.autor,
            "genero": self.genero,
            "estatus": self.estatus,
            "archivo_url": self.archivo_url
        }
