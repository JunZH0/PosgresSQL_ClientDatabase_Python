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
            dni TEXT PRIMARY KEY,
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
            dni TEXT REFERENCES client (dni),
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


def insertar_deportes():
    conn = psycopg2.connect(
        host="localhost",
        database="polideportivos",
        user="postgres",
        password="652050"
    )
    conn.autocommit = True

    for deporte in deportes:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO sports (nombre, precio) VALUES (%s, %s)",
            (deporte.nombre, deporte.precio_hora)
        )

    conn.commit()

    conn.close()


insertar_deportes()


def validar_dni(dni, conn, cur):
    cur.execute("SELECT dni FROM client WHERE dni = %s", (dni,))

    if cur.rowcount == 0:
        print("No se ha encontrado ningún cliente con ese DNI.")
        return False

    return True


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

    # Crear una instancia de la clase Cliente
    client = Cliente(name, dni.upper(), fnac_formateado, tlf)

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

    if not validar_dni(dni, conn, cur):
        return

    cur.execute(
        "DELETE FROM client WHERE dni = %s",
        (dni.upper(),)
    )

    conn.commit()

    conn.close()

    print("Cliente dado de baja correctamente")


# TODO - Formatear la fecha de nacimiento a dd/mm/yyyy
def mostrar_datos_client():
    opcion = input("¿Desea ver los datos de un cliente específico (1) o de todos los clientes (2)? ")
    if opcion == '1':
        dni = input("Ingrese el DNI del cliente: ")
        conn, cur = conexion_bd()

        if not validar_dni(dni, conn, cur):
            return


        # Ejecutar una consulta para recuperar los datos del cliente específico
        cur.execute(
            "SELECT dni, nombre, fnac, telefono FROM client WHERE dni = %s",
            (dni.upper(),)
        )



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
    else:
        print("Opción no válida.")


def alta_deporte():
    dni = input("Introduce el DNI del cliente: ")
    conn, cur = conexion_bd()

    if not validar_dni(dni, conn, cur):
        return


    print("Los deportes disponibles son:")
    for index, sport in enumerate(deportes):
        print(index + 1, sport.nombre)
        print("  Precio por hora:", sport.precio_hora)

    index_deporte = int(input("Introduce el número del deporte elegido: ")) - 1
    horario = input("Introduce el horario elegido: ")

    deporte_seleccionado = deportes[index_deporte]
    if not deporte_seleccionado:
        print("No existe el deporte elegido.")
        return

    nom_deporte = deporte_seleccionado.nombre

    try:
        conn, cur = conexion_bd()

        cur.execute("INSERT INTO client_sports (dni, nombre, horario) VALUES (%s, %s, %s)",
                    (dni.upper(), nom_deporte, horario))

        conn.commit()
        print("Matrícula realizada con éxito.")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error al realizar la matrícula:", error)

    finally:
        if conn is not None:
            conn.close()


def baja_deporte():
    # validar en la base de datos que el dni existe
    dni = input("Introduce el DNI del cliente: ")
    conn, cur = conexion_bd()

    if validar_dni(dni, conn, cur) is False:
        conn.close()
        print("El cliente con DNI", dni.upper(), "no está matriculado en ningún deporte.")
        return

    sport_name = input("Introduce el nombre del deporte: ")

    conn, cur = conexion_bd()

    cur.execute(
        "DELETE FROM client_sports WHERE nombre = %s AND dni = %s",
        (sport_name, dni.upper())
    )
    conn.commit()
    conn.close()
    print("Se ha eliminado el deporte con éxito.")


def mostrar_deportes_cliente():
    # validar en la base de datos que el dni existe

    dni = input("Introduce el DNI del cliente: ")

    conn, cur = conexion_bd()

    cur.execute(
        "SELECT dni FROM client WHERE dni = %s",
        (dni.upper(),)
    )

    if cur.rowcount == 0:
        print("No se ha encontrado ningún cliente con ese DNI.")
        return

    conn.commit()
    conn.close()

    conn, cur = conexion_bd()
    cur.execute("SELECT nombre, horario FROM client_sports WHERE dni = %s", (dni,))
    enrolled_sports = cur.fetchall()

    # conseguir el nombre del dni del cliente
    cur.execute("SELECT nombre FROM client WHERE dni = %s", (dni.upper(),))
    nombre = cur.fetchone()[0]

    if not enrolled_sports:
        print("El cliente " + nombre + "no está matriculado en ningún deporte.")
        return

    print("El cliente " + nombre + " está matriculado en los siguientes deportes:")
    for sport in enrolled_sports:
        print("\n")
        print("  Deporte:", sport[0])
        print("  Horario:", sport[1])
        print("\n")

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
        6: mostrar_deportes_cliente,
        7: exit
    }

    switcher.get(opcion, lambda: print("Opción no válida."))()


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
