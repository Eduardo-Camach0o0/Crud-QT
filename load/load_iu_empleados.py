#1.- Importar librerias
import sys
from PyQt5 import QtCore
from PyQt5.QtCore import QPropertyAnimation
from PyQt5 import QtCore, QtGui, QtWidgets, uic  


from modelo.empleadoActions import EmpleadosAct


class Load_ui_empleados(QtWidgets.QMainWindow):

    #2.- Cargar archivo .ui
    def __init__(self):
        super().__init__()
        # Cargar archivo .ui
        uic.loadUi("ui/ui_empleados.ui", self)
        self.show()

        #3.5 Fijar ancho columnas
        #eliminar barra y de titulo - opacidad
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        

        #3.- Configurar contenedores
        #Cerrar ventana
        self.boton_salir.clicked.connect(self.menu)
        # mover ventana
        self.frame_superior.mouseMoveEvent = self.mover_ventana
        #menu lateral
        self.boton_menu.clicked.connect(self.mover_menu)
        
        #Fijar ancho columnas
        self.tabla_productos.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        

        
        #4.- Conectar botones a funciones
        
        #acceder a las paginas
        self.boton_agregar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_agregar))
        self.boton_buscar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_buscar))
        self.boton_actualizar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_actualizar))
        self.boton_eliminar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_eliminar))
        self.boton_consultar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_consultar))

        self.accion_guardar.clicked.connect(self.guardar_empleado) #
        self.buscar_guardar.clicked.connect(self.buscar_guardar_empleado)#

        self.accion_actualizar.clicked.connect(self.actualizar_empleado) #
        self.buscar_actualizar.clicked.connect(self.buscar_actualizar_empleado) #

        self.accion_eliminar.clicked.connect(self.eliminar_empleado)#
        self.buscar_eliminar.clicked.connect(self.buscar_eliminar_empleado) #

        self.accion_limpiar.clicked.connect(self.limpiar_general) #
        self.buscar_buscar.clicked.connect(self.buscar_general)#

        self.boton_refresh.clicked.connect(self.actualizar_tabla) #

        self.boton_actualizar.clicked.connect(self.limpiar)#
        self.boton_agregar.clicked.connect(self.limpiar)#
        self.boton_consultar.clicked.connect(self.limpiar)#
        self.boton_eliminar.clicked.connect(self.limpiar)#
        self.boton_buscar.clicked.connect(self.limpiar)#



        # Instancias
        self.empleadoI = EmpleadosAct()
        

    
    def limpiar(self):
        self.empleadoI.empleado.idEmpleado = 0
        self.empleadoI.empleado.Nombre = ""
        self.empleadoI.empleado.CuentaClabe = ""
        self.empleadoI.empleado.Turno = 0
        self.empleadoI.empleado.Ingreso = ""

    def menu(self):
        from load.load_iu_menu import VentanaMenu

        self.ventana_menu = VentanaMenu()
        self.ventana_menu.show()
        self.close()
        pass
 

    #Operaciones con el modelo de datos            
    def guardar_empleado(self):

        if self.sku_agregar.text() == "" or self.descripcion_agregar.text() == "" or self.existencia_agregar.text() == "":
            self.label.setText("Todos los campos son obligatorios")
        else:
            self.empleadoI.empleado.Nombre = str(self.sku_agregar.text()).upper()
            self.empleadoI.empleado.CuentaClabe = str(self.descripcion_agregar.text()).lower()
            self.empleadoI.empleado.Turno = int(self.existencia_agregar.text())
        
            response = self.empleadoI.InsertEmpleado()

            if response == "ok":
                self.label.setText("Empleado añadido Existosamente")
                self.sku_agregar.setText("")
                self.descripcion_agregar.setText("")
                self.existencia_agregar.setText("")
            else:
                self.label.setText("Error al agregar empleado")

     
        pass

    
    def buscar_guardar_empleado(self):
        self.empleadoI.empleado.Nombre = str(self.sku_agregar.text()).upper()

        if self.empleadoI.searchEmpleado() == []:
            self.label.setText("No existe ese empleado")
        else:
            data = self.empleadoI.searchEmpleado()[0]
            self.label.setText("")
            self.empleadoI.empleado.idEmpleado = int(data[0])
            str(self.sku_agregar.setText(data[1])).upper()
            str(self.descripcion_agregar.setText(data[2])).lower()
            str(self.existencia_agregar.setText(str(data[3])))
            # str(self.precio_agregar.setText(str(data[3])))
        pass


    def actualizar_empleado(self):
        self.empleadoI.empleado.Nombre = str(self.sku_actualizar.text()).upper()
        self.empleadoI.empleado.CuentaClabe = str(self.descripcion_actualizar.text()).lower()
        self.empleadoI.empleado.Turno = int(self.existencia_actualizar.text())
        self.empleadoI.empleado.Ingreso = str(self.precio_actualizar.text())
        

        response = self.empleadoI.UpdateEmpleado()

        if  response == "ok":
            self.label.setText("Exito al actualizar empleado")
            str(self.sku_actualizar.setText(""))
            str(self.descripcion_actualizar.setText(""))
            str(self.existencia_actualizar.setText(str("")))
            str(self.precio_actualizar.setText(str("")))
        else:
            self.label.setText("Error al actualizar empleado")


        pass


    def buscar_actualizar_empleado(self):
        
        self.empleadoI.empleado.Nombre = str(self.sku_actualizar.text()).upper()

        if self.empleadoI.searchEmpleado() == []:
            self.label.setText("No existe ese empleado")
        else:
            data = self.empleadoI.searchEmpleado()[0]
            self.label.setText("")
            self.empleadoI.empleado.idEmpleado = int(data[0])
            str(self.sku_actualizar.setText(data[1])).upper()
            str(self.descripcion_actualizar.setText(data[2])).lower()
            str(self.existencia_actualizar.setText(str(data[3])))
            str(self.precio_actualizar.setText(str(data[4])))

        pass



    def eliminar_empleado(self):
        if self.sku_eliminar.text() == "" or self.descripcion_eliminar.text() == "" or self.existencia_eliminar.text() == "" or self.precio_eliminar.text() == "":
            self.label.setText("Todos los campos son obligatorios")
        else:
            response = self.empleadoI.DeleteEmpleado()
            if  response == "ok":
                self.label.setText("Exito al eliminar empleado")
                str(self.sku_eliminar.setText(""))
                str(self.descripcion_eliminar.setText(""))
                str(self.existencia_eliminar.setText(str("")))
                str(self.precio_eliminar.setText(str("")))
            else:
                self.label.setText("Error al eliminar el empleado empleado")

        pass 
    

    def buscar_eliminar_empleado(self):

        self.empleadoI.empleado.Nombre = str(self.sku_eliminar.text()).upper()
        if self.empleadoI.searchEmpleado() == []:
            self.label.setText("No existe ese empleado")
        else:
           
            data = self.empleadoI.searchEmpleado()[0]
            self.label.setText("")
            self.empleadoI.empleado.idEmpleado = int(data[0])
            str(self.sku_eliminar.setText(data[1]))
            str(self.descripcion_eliminar.setText(data[2]))
            str(self.existencia_eliminar.setText(str(data[3])))
            str(self.precio_eliminar.setText(str(data[4])))

        pass


    def buscar_general(self):
        self.empleadoI.empleado.Nombre = str(self.sku_buscar.text()).upper()
        if self.empleadoI.searchEmpleado() == []:
            self.label.setText("No existe ese empleado")
        else:
           
            data = self.empleadoI.searchEmpleado()[0]
            self.label.setText("")
            self.empleadoI.empleado.id_product = int(data[0])
            str(self.sku_buscar.setText(data[1]))
            str(self.descripcion_buscar.setText(data[2]))
            str(self.existencia_buscar.setText(str(data[3])))
            str(self.precio_buscar.setText(str(data[4])))

            pass


    def limpiar_general(self):
        str(self.sku_buscar.setText(""))
        str(self.descripcion_buscar.setText(""))
        str(self.existencia_buscar.setText(str("")))
        str(self.precio_buscar.setText(str("")))



    def actualizar_tabla(self):
        data = self.empleadoI.selectEmpleado()
        self.tabla_productos.setRowCount(len(data))
        fila = 0

        for item in data:
            self.tabla_productos.setItem(fila, 0, QtWidgets.QTableWidgetItem(str(item[1]))) 
            self.tabla_productos.setItem(fila, 1, QtWidgets.QTableWidgetItem(str(item[2]))) 
            self.tabla_productos.setItem(fila, 2, QtWidgets.QTableWidgetItem(str(item[3]))) 
            self.tabla_productos.setItem(fila, 3, QtWidgets.QTableWidgetItem(str(item[4]))) 
            fila += 1

        # print(response)
    
        
   


    ## mover ventana
    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()
    def mover_ventana(self, event):
        if self.isMaximized() == False:			
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.clickPosition)
                self.clickPosition = event.globalPos()
                event.accept()

        if event.globalPos().y() <=20:
            self.showMaximized()
        else:
            self.showNormal()

    
    #7.- Mover menú
            
    def mover_menu(self):
        if True:			
            width = self.frame_lateral.width()
            widthb = self.boton_menu.width()
            normal = 0
            if width==0:
                extender = 200
                self.boton_menu.setText("Menú")
            else:
                extender = normal
                self.boton_menu.setText("")
                
            self.animacion = QPropertyAnimation(self.frame_lateral, b'minimumWidth')
            self.animacion.setDuration(300)
            self.animacion.setStartValue(width)
            self.animacion.setEndValue(extender)
            self.animacion.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animacion.start()
            
            self.animacionb = QPropertyAnimation(self.boton_menu, b'minimumWidth')
            self.animacionb.setStartValue(width)
            self.animacionb.setEndValue(extender)
            self.animacionb.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animacionb.start()