from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QDateTimeEdit, QGroupBox
from PyQt5.QtCore import QDateTime
from base_datos import verificar_disponibilidad, guardar_reserva, cancelar_reserva

class InterfazReservas(QWidget):
    def __init__(self):
        super().__init__()
        self.inicializar_interfaz()
    
    def inicializar_interfaz(self):
        # Configuración de la interfaz
        self.setWindowTitle("Gestor de Reservas - Restaurante")
        self.resize(400, 600)
        self.configurar_estilo()
        
        # Elementos de entrada de datos de cliente
        caja_informacion_cliente = QGroupBox("Información del Cliente")
        self.entrada_nombre = QLineEdit()
        self.entrada_telefono = QLineEdit()
        self.entrada_correo = QLineEdit()
        self.entrada_correo.textChanged.connect(self.habilitar_boton_cancelar)
        
        # Elementos de reserva
        caja_reserva = QGroupBox("Detalles de la Reserva")
        self.entrada_fecha = QDateTimeEdit(QDateTime.currentDateTime())
        self.entrada_fecha.setCalendarPopup(True)
        self.entrada_personas = QComboBox()
        self.entrada_personas.addItems(["2", "4", "6", "8"])
        
        # Botones
        self.boton_reservar = QPushButton("Reservar")
        self.boton_cancelar = QPushButton("Cancelar Reserva")
        self.boton_cancelar.setEnabled(False)

        # Eventos de los botones
        self.boton_reservar.clicked.connect(self.hacer_reserva)
        self.boton_cancelar.clicked.connect(self.cancelar_reserva)
        
        # Layout
        layout_principal = self.crear_layout(caja_informacion_cliente, caja_reserva)
        self.setLayout(layout_principal)

    def hacer_reserva(self):
        # Obtener datos de entrada
        nombre = self.entrada_nombre.text()
        telefono = self.entrada_telefono.text()
        correo = self.entrada_correo.text()
        fecha = self.entrada_fecha.dateTime().toString("yyyy-MM-dd HH:mm")
        personas = int(self.entrada_personas.currentText())
        
        # Verificar campos
        if not nombre or not telefono or not correo:
            QMessageBox.warning(self, "Campos Vacíos", "Por favor, complete todos los campos.")
            return
        
        # Verificar disponibilidad de mesa y guardar reserva
        mesa_disponible = verificar_disponibilidad(fecha, personas)
        if mesa_disponible:
            guardar_reserva(nombre, telefono, correo, fecha, personas, mesa_disponible)
            QMessageBox.information(self, "Reserva Exitosa", f"Reserva realizada para la mesa {mesa_disponible}")
        else:
            QMessageBox.warning(self, "No disponible", "No hay mesas disponibles para este número de personas.")
        
    def cancelar_reserva(self):
        correo = self.entrada_correo.text()
        cancelar_reserva(correo)
        QMessageBox.information(self, "Reserva Cancelada", "Reserva cancelada exitosamente.")
        self.boton_cancelar.setEnabled(False)

    def habilitar_boton_cancelar(self):
        self.boton_cancelar.setEnabled(bool(self.entrada_correo.text()))

    def configurar_estilo(self):
        # Estilo de la interfaz
        self.setStyleSheet("""
            QWidget { background-color: #f0f0f0; font-family: Arial; }
            QLabel { color: #333; font-size: 14px; padding: 5px; }
            QLineEdit, QComboBox, QDateTimeEdit { border: 1px solid #ccc; border-radius: 5px; padding: 5px; font-size: 14px; }
            QPushButton { background-color: #4CAF50; color: white; font-size: 14px; border-radius: 5px; padding: 10px; }
            QPushButton:disabled { background-color: #ccc; }
            QPushButton:hover { background-color: #45a049; }
            QGroupBox { font-size: 16px; font-weight: bold; color: #4CAF50; border: 1px solid #4CAF50; border-radius: 5px; margin-top: 10px; }
            QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 3px; }
        """)

    def crear_layout(self, caja_informacion_cliente, caja_reserva):
        # Configuración del layout principal
        layout_cliente = QVBoxLayout()
        layout_cliente.addWidget(QLabel("Nombre:"))
        layout_cliente.addWidget(self.entrada_nombre)
        layout_cliente.addWidget(QLabel("Teléfono:"))
        layout_cliente.addWidget(self.entrada_telefono)
        layout_cliente.addWidget(QLabel("Correo:"))
        layout_cliente.addWidget(self.entrada_correo)
        caja_informacion_cliente.setLayout(layout_cliente)

        layout_reserva = QVBoxLayout()
        layout_reserva.addWidget(QLabel("Fecha y Hora:"))
        layout_reserva.addWidget(self.entrada_fecha)
        layout_reserva.addWidget(QLabel("Número de personas:"))
        layout_reserva.addWidget(self.entrada_personas)
        caja_reserva.setLayout(layout_reserva)

        layout_botones = QHBoxLayout()
        layout_botones.addWidget(self.boton_reservar)
        layout_botones.addWidget(self.boton_cancelar)

        layout_principal = QVBoxLayout()
        layout_principal.addWidget(caja_informacion_cliente)
        layout_principal.addWidget(caja_reserva)
        layout_principal.addLayout(layout_botones)
        return layout_principal
