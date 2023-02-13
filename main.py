import psycopg2

from Clases import Cliente
from Clases import Deporte
import datetime

deportes = [Deporte("Fútbol", 10), Deporte("Baloncesto", 15), Deporte("Tenis", 20), Deporte("Atletismo", 25),
            Deporte("Natación", 30)]

""" ********** Ejecutar solo una vez  ********** """


def drop_database():

    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="652050"
    )
    conn.autocommit = True

    # Drop the database
    cur = conn.cursor()
    cur.execute("DROP DATABASE IF EXISTS polideportivos;")

    # Close the cursor and connection
    cur.close()
    conn.close()


drop_database()


def create_database(conn):
    cur = conn.cursor()

    # Create the database

    cur.execute("CREATE DATABASE polideportivos;")

    # Close the cursor and connection
    cur.close()
    conn.close()


def create_tables(conn):
    cur = conn.cursor()

    # Create the client table
    cur.execute("""
        CREATE TABLE client (
            dni SERIAL PRIMARY KEY,
            nombre TEXT NOT NULL,
            fnac DATE NOT NULL,
            telefono TEXT NOT NULL
        );
    """)

    # Create the sports table
    cur.execute("""
        CREATE TABLE sports (
            nombre TEXT NOT NULL,
            precio NUMERIC NOT NULL,
            PRIMARY KEY (nombre)
        );
    """)

    cur.execute("""
        CREATE TABLE client_sports (
            dni INTEGER REFERENCES client (dni),
            nombre TEXT REFERENCES sports (nombre),
            horario TEXT NOT NULL,
            PRIMARY KEY (dni, nombre)
        );
    """)

    conn.commit()
    cur.close()
    conn.close()


conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="652050"
)
conn.autocommit = True

create_database(conn)

conn = psycopg2.connect(
    host="localhost",
    database="polideportivos",
    user="postgres",
    password="652050"
)

create_tables(conn)


def alta_cliente():
    name = input("Introduce el nombre completo: ")
    # validacion de dni
    while True:
        dni = input("Introduce el DNI: ")
        if len(dni) == 9:
            break
        print("El DNI debe tener 9 caracteres.")

    # validacion fecha de nacimiento
    while True:
        fnac = input("Introduce la fecha de nacimiento (dd/mm/yyyy): ")
        try:
            fnac_formateado = datetime.datetime.strptime(fnac, '%d/%m/%Y').date()
            break
        except ValueError:
            print("El formato de la fecha debe ser dd/mm/yyyy")

    # validacion telefono
    while True:
        tlf = input("Introduce el teléfono: ")
        if len(tlf) == 9:
            break
        print("El teléfono debe tener 9 caracteres.")

    # Crear una instancia de la clase Client
    client = Cliente(name, dni, fnac_formateado, tlf)

    conn, cur = conexion_bd()

    cur.execute(
        "INSERT INTO client (nombre, dni, fnac, telefono) VALUES (%s, %s, %s, %s)",
        (client.nombre_completo, client.dni, client.fecha_nacimiento, client.telefono)
    )

    conn.commit()

    conn.close()

    print("Cliente agregado correctamente")


def baja_cliente():
    dni = input("Ingrese el DNI del cliente que desea dar de baja: ")

    conn, cur = conexion_bd()

    cur.execute(
        "DELETE FROM client WHERE dni = %s",
        (dni,)
    )

    if cur.rowcount == 0:
        print("No se ha encontrado ningún cliente con ese DNI.")
        return

    conn.commit()

    conn.close()

    print("Cliente dado de baja correctamente")


def mostrar_datos_client():
    opcion = input("¿Desea ver los datos de un cliente específico (1) o de todos los clientes (2)? ")
    if opcion == '1':
        dni = input("Ingrese el DNI del cliente: ")
        conn, cur = conexion_bd()

        # Ejecutar una consulta para recuperar los datos del cliente específico
        cur.execute(
            "SELECT dni, nombre, fnac, telefono FROM client WHERE dni = %s",
            (dni,)
        )

        if cur.rowcount == 0:
            print("No se ha encontrado ningún cliente con ese DNI.")
            return

        cliente = cur.fetchone()
        print("\n")
        print("Nombre: ", cliente[1])
        print("DNI: ", cliente[0])
        print("Fecha de nacimiento: ", cliente[2])
        print("Teléfono: ", cliente[3])
        print("\n")

        conn.commit()
        conn.close()
    elif opcion == '2':
        conn, cur = conexion_bd()

        # Ejecutar una consulta para recuperar los datos de todos los clientes
        cur.execute(
            "SELECT * FROM client"
        )

        if cur.rowcount == 0:
            print("No se ha encontrado ningún cliente.")
            return

        clientes = cur.fetchall()
        for cliente in clientes:
            print("\n")
            print("Nombre: ", cliente[1])
            print("DNI: ", cliente[0])
            print("Fecha de nacimiento: ", cliente[2])
            print("Teléfono: ", cliente[3])
            print("\n")

        conn.commit()
        conn.close()


def alta_deporte():
    dni = input("Introduce el DNI del cliente: ")
    print("Los deportes disponibles son:")
    for index, sport in enumerate(deportes):
        print(index + 1, sport.nombre)
        print("  Precio por hora:", sport.precio_hora)

    sport_index = int(input("Introduce el número del deporte elegido: ")) - 1
    schedule = input("Introduce el horario elegido: ")

    selected_sport = deportes[sport_index]
    if not selected_sport:
        print("No existe el deporte elegido.")
        return

    selected_sport_name = selected_sport.nombre
    selected_sport_schedule = selected_sport_name + "-" + schedule


def baja_deporte(self):
    dni = input("Introduce el DNI del cliente: ")
    sport_name = input("Introduce el nombre del deporte: ")

    conn, cur = conexion_bd()

    cur.execute(
        "SELECT sports FROM client WHERE dni = %s",
        (dni,)
    )
    enrolled_sports = cur.fetchone()[0]

    if enrolled_sports is None or sport_name not in enrolled_sports:
        print("El cliente no está matriculado en este deporte.")
        return

    enrolled_sports.remove(sport_name)

    cur.execute(
        "UPDATE client SET sports = %s WHERE dni = %s",
        (enrolled_sports, dni)
    )
    conn.commit()
    conn.close()
    print("Se ha eliminado el deporte con éxito.")


# TODO - Falta Arreglar
def mostrar_deport_client(self):
    dni = input("Introduce el DNI del cliente: ")

    conn, cur = conexion_bd()
    cur.execute("SELECT sport FROM client WHERE dni = %s", (dni,))
    enrolled_sports = cur.fetchone()[0]

    if not enrolled_sports:
        print("El cliente no está matriculado en ningún deporte.")
        return

    print("El cliente está matriculado en los siguientes deportes:")
    for sport in enrolled_sports:
        sport_name, schedule = sport.split("-")
        print("- Deporte:", sport_name)

    conn.close()


def menu():
    print("1. Dar de alta un cliente con sus datos personales")
    print("2. Dar de baja un cliente")
    print("3. Mostrar los datos personales de un cliente o de todos")
    print("4. Matricular a un cliente en un deporte")
    print("5. Baja un cliente en un deporte")
    print("6. Mostrar los deportes de un cliente")
    print("7. Salir")

    try:
        opcion = int(input("Elije una opción: "))
    except ValueError:
        print("Error: Por favor, introduce un número.")
        return

    switcher = {
        1: alta_cliente,
        2: baja_cliente,
        3: mostrar_datos_client,
        4: alta_deporte,
        5: baja_deporte,
        6: mostrar_deport_client,
        7: exit
    }

    func = switcher.get(opcion, lambda: "Opción no válida")
    func()


# Función reutilizable para conectar con la base de datos
def conexion_bd():
    # Conectar con la base de datos
    conn = psycopg2.connect(
        host="localhost",
        database="polideportivos",
        user="postgres",
        password="652050"
    )
    # Crear un cursor
    cur = conn.cursor()
    return conn, cur


if __name__ == '__main__':
    while True:
        menu()
