import psycopg2

from Cliente import Cliente
from Deporte import Deporte

def __init__(self):
    self.tennis = Deporte("Tennis", 20)
    self.swimming = Deporte("Natación", 25)
    self.athletics = Deporte("Atletismo", 15)
    self.basketball = Deporte("Baloncesto", 22)
    self.football = Deporte("Fútbol", 18)


def delete_client(self):
    dni = input("Ingrese el DNI del cliente que desea dar de baja: ")
    cliente = self.db.get_client(dni)
    if cliente:
        self.db.delete_client(cliente)
        print("Cliente dado de baja exitosamente.")
    else:
        print("No se encontró al cliente con ese DNI.")


def show_client_data():
    pass


def enroll_in_sport():
    pass


def unenroll_from_sport():
    pass


def show_client_sports():
    pass


def menu():
    print("1. Dar de alta un cliente con sus datos personales")
    print("2. Dar de baja un cliente")
    print("3. Mostrar los datos personales de un cliente o de todos")
    print("4. Matricular a un cliente en un deporte")
    print("5. Desmatricular a un cliente en un deporte")
    print("6. Mostrar los deportes de un cliente")
    print("7. Salir")

    opcion = int(input("Elije una opción: "))

    if opcion == 1:
        add_client()
    elif opcion == 2:
        delete_client()
    elif opcion == 3:
        show_client_data()
    elif opcion == 4:
        enroll_in_sport()
    elif opcion == 5:
        unenroll_from_sport()
    elif opcion == 6:
        show_client_sports()
    elif opcion == 7:
        exit()
    else:
        print("Opción no válida. Elije otra opción.")
        menu()

def add_client():
    # Solicitar los datos personales del cliente
    name = input("Introduce el nombre completo: ")
    dni = input("Introduce el DNI: ")
    birthdate = input("Introduce la fecha de nacimiento (dd/mm/yyyy): ")
    phone = input("Introduce el teléfono: ")

    # Crear una instancia de la clase Client
    client = Cliente(name, dni, birthdate, phone)

    # Conectar con la base de datos
    conn = psycopg2.connect(
        host="localhost",
        database="polideportivo",
        user="postgres",
        password="password"
    )

    # Crear un cursor
    cur = conn.cursor()

    # Ejecutar una consulta para insertar los datos del cliente en la tabla clientes
    cur.execute(
        "INSERT INTO clientes (nombre, dni, fecha_nacimiento, telefono) VALUES (%s, %s, %s, %s)",
        (client.name, client.dni, client.birthdate, client.phone)
    )

    # Guardar los cambios en la base de datos
    conn.commit()

    # Cerrar la conexión con la base de datos
    conn.close()

    print("Cliente agregado correctamente")


menu()
