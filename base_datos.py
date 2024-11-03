import sqlite3

def crear_base_datos():
    # Crear la base de datos y tabla si no existen
    conexion = sqlite3.connect('restaurant.db')
    cursor = conexion.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS reservas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT,
                        telefono TEXT,
                        correo TEXT,
                        fecha TEXT,
                        personas INTEGER,
                        numero_mesa INTEGER)''')
    conexion.commit()
    conexion.close()

def guardar_reserva(nombre, telefono, correo, fecha, personas, numero_mesa):
    # Guardar una nueva reserva
    conexion = sqlite3.connect('restaurant.db')
    cursor = conexion.cursor()
    cursor.execute('''INSERT INTO reservas (nombre, telefono, correo, fecha, personas, numero_mesa)
                      VALUES (?, ?, ?, ?, ?, ?)''', 
                   (nombre, telefono, correo, fecha, personas, numero_mesa))
    conexion.commit()
    conexion.close()

def verificar_disponibilidad(fecha, personas):
    # Verificar si hay una mesa disponible
    conexion = sqlite3.connect('restaurant.db')
    cursor = conexion.cursor()
    cursor.execute("SELECT numero_mesa FROM reservas WHERE personas = ? AND fecha = ?", (personas, fecha))
    mesas_reservadas = cursor.fetchall()
    conexion.close()
    
    todas_mesas = list(range(1, 11))
    mesas_disponibles = [mesa for mesa in todas_mesas if (mesa,) not in mesas_reservadas]
    return mesas_disponibles[0] if mesas_disponibles else None

def cancelar_reserva(correo):
    # Cancelar reserva basada en el correo
    conexion = sqlite3.connect('restaurant.db')
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM reservas WHERE correo = ?", (correo,))
    conexion.commit()
    conexion.close()
