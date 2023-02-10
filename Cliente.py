class Cliente:
    def __init__(self, nombre_completo, dni, fecha_nacimiento, telefono):
        self.nombre_completo = nombre_completo
        self.dni = dni
        self.fecha_nacimiento = fecha_nacimiento
        self.telefono = telefono

        def datos(self):
            return (
                    "Nombre: " + self.nombre + "\n" +
                    "DNI: " + self.dni + "\n" +
                    "Fecha de nacimiento: " + self.fecha_nacimiento + "\n" +
                    "Teléfono: " + self.telefono
            )

        def deportes(self):
            deportes_str = ""
            for deporte in self.deportes:
                deportes_str += deporte.mostrar_nombre() + " - Precio por hora: " + str(deporte.precio_hora) + "€\n"
            return deportes_str

        def matricular_en_deporte(self, deporte, horario):
            self.deportes.append((deporte, horario))

