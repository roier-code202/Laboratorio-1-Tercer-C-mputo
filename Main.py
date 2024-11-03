import sys
from PyQt5.QtWidgets import QApplication
from interfaz import InterfazReservas
from base_datos import crear_base_datos

#Este es el achivo principal que inica el programa y mustra la inferzas
def main():
    # Crear la base de datos si no existe
    crear_base_datos()
    
    # Ejecutar la aplicación
    app = QApplication(sys.argv)
    ventana = InterfazReservas()
    ventana.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
