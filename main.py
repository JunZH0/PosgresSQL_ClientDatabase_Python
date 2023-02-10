import psycopg2

from Cliente import Cliente
from Deporte import Deporte


def __init__(self):
    self.db = psycopg2.connect("dbname=centro_deportivo user=postgres password=secret")
    self.tennis = Deporte("Tennis", 20)
    self.swimming = Deporte("Natación", 25)
    self.athletics = Deporte("Atletismo", 15)
    self.basketball = Deporte("Baloncesto", 22)
    self.football = Deporte("Fútbol", 18)


def delete_client(self):
    dni = input("Ingrese el DNI del cliente que desea dar de baja: ")

    # Validate the input
    if not dni.isdigit() or len(dni) != 8:
        print("El DNI ingresado no es válido.")
        return

    try:
        db = self.connect_to_db()
        cliente = self.db.get_client(dni)
        if cliente:
            self.db.delete_client(cliente)
            print("Cliente dado de baja exitosamente.")
        else:
            print("No se encontró al cliente con ese DNI.")
    except Exception as e:
        print("Se ha producido un error: {}".format(e))



def show_client_data(self):
    opcion = input("¿Desea ver los datos de un cliente específico (1) o de todos los clientes (2)? ")
    if opcion == '1':
        dni = input("Ingrese el DNI del cliente: ")
        client = self.db.get_client(dni)
        if client:
            print(client)
        else:
            print("No se encontró al cliente con ese DNI.")
    else:
        clients = self.db.get_all_clients()
        for client in clients:
            print(client)


def enroll_in_sport(self):
    dni = input("Introduce el DNI del cliente: ")
    print("Los deportes disponibles son:")
    for i, sport in enumerate(self.sports):
        print(f"{i + 1}. {sport.name}")
    sport_index = int(input("Introduce el número del deporte elegido: "))
    if sport_index < 1 or sport_index > len(self.sports):
        print("Opción inválida.")
        return

    sport_price = self.sports[sport_index - 1].price
    schedule = input("Introduce el horario elegido: ")

    conn = self.connect_to_db()
    cur = conn.cursor()
    cur.execute(
        "UPDATE client SET enrolled_sports = array_append(enrolled_sports, %s) WHERE dni = %s",
        (self.sports[sport_index - 1].name + "-" + schedule, dni)
    )
    conn.commit()
    print("Matrícula realizada con éxito.")


def unenroll_from_sport(self):
    dni = input("Introduce el DNI del cliente: ")
    sport_name = input("Introduce el nombre del deporte: ")
    schedule = input("Introduce el horario elegido: ")

    conn = self.connect_to_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT enrolled_sports FROM client WHERE dni = %s",
        (dni,)
    )
    enrolled_sports = cur.fetchone()[0]

    if enrolled_sports is None or (sport_name + "-" + schedule) not in enrolled_sports:
        print("El cliente no está matriculado en este deporte con este horario.")
        return

    enrolled_sports.remove(sport_name + "-" + schedule)

    cur.execute(
        "UPDATE client SET enrolled_sports = %s WHERE dni = %s",
        (enrolled_sports, dni)
    )
    conn.commit()
    print("Desmatrícula realizada con éxito.")


def show_client_sports(self):
    dni = input("Introduce el DNI del cliente: ")

    conn = self.connect_to_db()
    cur = conn.cursor()
    cur.execute("SELECT enrolled_sports FROM client WHERE dni = %s", (dni,))
    enrolled_sports = cur.fetchone()[0]

    if not enrolled_sports:
        print("El cliente no está matriculado en ningún deporte.")
        return

    print("El cliente está matriculado en los siguientes deportes:")
    for sport in enrolled_sports:
        sport_name, schedule = sport.split("-")
        print("- Deporte:", sport_name)
        print("  Horario:", schedule)


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
