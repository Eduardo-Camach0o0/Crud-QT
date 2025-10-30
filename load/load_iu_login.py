from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
from load.load_iu_menu import VentanaMenu
from modelo.login import LoginVal

class Login(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/login_o.ui", self)

        self.usuario = self.line_edit_usuario
        self.password = self.line_edit_password
        self.boton_ingresar = self.boton_ingresar
        self.label_status = self.label_status

        self.boton_ingresar.clicked.connect(self.validar_login)

    def validar_login(self):
        user = self.usuario.text().strip()
        pwd = self.password.text().strip()

        if not user or not pwd:
            self.label_status.setText("⚠️ Ingresa usuario y contraseña.")
            return

        val = LoginVal(user, pwd)
        response = val.validar_login()
        print(response)

        if response:
            self.label_status.setStyleSheet("color: green;")
            self.label_status.setText("✔️ Acceso permitido.")
            QMessageBox.information(self, "Bienvenido", f"Hola, {user}")

            self.ventana_menu = VentanaMenu()
            self.ventana_menu.show()
            
            # self.ventana_principal = Load_ui_productos()
            # self.ventana_principal.show()

            # a = LoginVal("Edu","Desarollo","Eduardo Camacho")
            # a.crear_nuevo_usuario()


           
            self.close()


        else:
            self.label_status.setStyleSheet("color: red;")
            self.label_status.setText("❌ Usuario o contraseña incorrectos.")
            self.password.clear()
