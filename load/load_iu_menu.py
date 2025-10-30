from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow


class VentanaMenu(QMainWindow):

 def __init__(self):
  super().__init__()
  uic.loadUi("ui/menu.ui", self)


  self.boton_productos.clicked.connect(self.ir_a_productos)
  self.boton_empleados.clicked.connect(self.ir_a_empleados)
  self.boton_logout.clicked.connect(self.ir_a_login)


 def ir_a_productos(self):
  from load.load_ui_productos import Load_ui_productos

  self.ventana_productos = Load_ui_productos()
  self.ventana_productos.show()
  self.close() 

 def ir_a_empleados(self):
    
  from load.load_iu_empleados import Load_ui_empleados
  self.ventana_empleados = Load_ui_empleados()
  self.ventana_empleados.show()
  self.close()
  
  pass

 def ir_a_login(self):

  from load.load_iu_login import Login

  self.ventana_login = Login()
  self.ventana_login.show()
  self.close() 