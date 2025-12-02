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
        self.empleadoI.empleado.ApellidoPaterno = ""
        self.empleadoI.empleado.ApellidoMaterno = ""
        self.empleadoI.empleado.FechaAlta = ""
        self.empleadoI.empleado.FechaBaja = ""
        self.empleadoI.empleado.Activo = 0

    def menu(self):
        from load.load_iu_menu import VentanaMenu

        self.ventana_menu = VentanaMenu()
        self.ventana_menu.show()
        self.close()
        pass
 

    #Operaciones con el modelo de datos            
    def guardar_empleado(self):

        if self.nombre_agregar.text() == "" or self.ap_paterno_agregar.text() == "" or self.ap_materno_agregar.text() == "":
            self.label.setText("Todos los campos son obligatorios")
        else:
            self.empleadoI.empleado.Nombre = str(self.nombre_agregar.text()).upper()
            self.empleadoI.empleado.ApellidoPaterno = str(self.ap_paterno_agregar.text()).upper()
            self.empleadoI.empleado.ApellidoMaterno = str(self.ap_materno_agregar.text()).upper()
        
            response = self.empleadoI.InsertEmpleado()

            if response == "ok":
                self.label.setText("Empleado añadido Existosamente")
                self.nombre_agregar.setText("")
                self.ap_paterno_agregar.setText("")
                self.ap_materno_agregar.setText("")
            else:
                self.label.setText("Error al agregar empleado")

     
        pass

    
    def buscar_guardar_empleado(self):
        # Assuming user enters ID in the Name field for searching
        try:
            self.empleadoI.empleado.idEmpleado = int(self.nombre_agregar.text())
        except ValueError:
            self.label.setText("Ingrese un ID valido en el campo Nombre")
            return

        if self.empleadoI.searchEmpleado() == []:
            self.label.setText("No existe ese empleado")
        else:
            data = self.empleadoI.searchEmpleado()[0]
            self.label.setText("")
            self.empleadoI.empleado.idEmpleado = int(data['id_empleados'])
            self.nombre_agregar.setText(str(data['nombre']))
            self.ap_paterno_agregar.setText(str(data['apellido_paterno']))
            self.ap_materno_agregar.setText(str(data['apellido_materno']))
        pass


    def actualizar_empleado(self):

        if self.nombre_actualizar.text() == "" or self.ap_paterno_actualizar.text() == "" or self.ap_materno_actualizar.text() == "":
            self.label.setText("Todos los campos son obligatorios")
        else:
            # ID should have been set by search
            if self.empleadoI.empleado.idEmpleado == 0:
                 self.label.setText("Primero busque el empleado por ID")
                 return

            self.empleadoI.empleado.Nombre = str(self.nombre_actualizar.text()).upper()
            self.empleadoI.empleado.ApellidoPaterno = str(self.ap_paterno_actualizar.text()).upper()
            self.empleadoI.empleado.ApellidoMaterno = str(self.ap_materno_actualizar.text()).upper()
            

            response = self.empleadoI.UpdateEmpleado()

            if  response == "ok":
                self.label.setText("Exito al actualizar empleado")
                self.nombre_actualizar.setText("")
                self.ap_paterno_actualizar.setText("")
                self.ap_materno_actualizar.setText("")
            else:
                self.label.setText("Error al actualizar empleado")

        pass


    def buscar_actualizar_empleado(self):
        try:
            self.empleadoI.empleado.idEmpleado = int(self.nombre_actualizar.text())
        except ValueError:
            self.label.setText("Ingrese un ID valido en el campo Nombre")
            return

        if self.empleadoI.searchEmpleado() == []:
            self.label.setText("No existe ese empleado")
        else:
            data = self.empleadoI.searchEmpleado()[0]
            self.label.setText("")
            self.empleadoI.empleado.idEmpleado = int(data['id_empleados'])
            self.nombre_actualizar.setText(str(data['nombre']))
            self.ap_paterno_actualizar.setText(str(data['apellido_paterno']))
            self.ap_materno_actualizar.setText(str(data['apellido_materno']))
            self.precio_actualizar.setText(str(data['fecha_alta']))

        pass


    def eliminar_empleado(self):
        # ID should have been set by search
        if self.empleadoI.empleado.idEmpleado == 0:
             # Try to parse from field if user just typed it
             try:
                self.empleadoI.empleado.idEmpleado = int(self.nombre_eliminar.text())
             except ValueError:
                self.label.setText("Busque por ID o ingrese ID valido")
                return

        response = self.empleadoI.DeleteEmpleado()
        if  response == "ok":
            self.label.setText("Exito al eliminar empleado")
            self.nombre_eliminar.setText("")
            self.ap_paterno_eliminar.setText("")
            self.ap_materno_eliminar.setText("")
            self.precio_eliminar.setText("")
        else:
            self.label.setText("Error al eliminar el empleado")

        pass 
    

    def buscar_eliminar_empleado(self):
        try:
            self.empleadoI.empleado.idEmpleado = int(self.nombre_eliminar.text())
        except ValueError:
            self.label.setText("Ingrese un ID valido en el campo Nombre")
            return

        if self.empleadoI.searchEmpleado() == []:
            self.label.setText("No existe ese empleado")
        else:
           
            data = self.empleadoI.searchEmpleado()[0]
            self.label.setText("")
            self.empleadoI.empleado.idEmpleado = int(data['id_empleados'])
            self.nombre_eliminar.setText(str(data['nombre']))
            self.ap_paterno_eliminar.setText(str(data['apellido_paterno']))
            self.ap_materno_eliminar.setText(str(data['apellido_materno']))
            self.precio_eliminar.setText(str(data['fecha_alta']))

        pass


    def buscar_general(self):
        try:
            self.empleadoI.empleado.idEmpleado = int(self.nombre_buscar.text())
        except ValueError:
            self.label.setText("Ingrese un ID valido en el campo Nombre")
            return

        if self.empleadoI.searchEmpleado() == []:
            self.label.setText("No existe ese empleado")
        else:
           
            data = self.empleadoI.searchEmpleado()[0]
            self.label.setText("")
            self.empleadoI.empleado.idEmpleado = int(data['id_empleados'])
            self.nombre_buscar.setText(str(data['nombre']))
            self.ap_paterno_buscar.setText(str(data['apellido_paterno']))
            self.ap_materno_buscar.setText(str(data['apellido_materno']))
            self.precio_buscar.setText(str(data['fecha_alta']))

            pass


    def limpiar_general(self):
        self.nombre_buscar.setText("")
        self.ap_paterno_buscar.setText("")
        self.ap_materno_buscar.setText("")
        self.precio_buscar.setText("")


    def actualizar_tabla(self):
        data = self.empleadoI.selectEmpleado()
        if data:
            self.tabla_productos.setRowCount(len(data))
            fila = 0

            for item in data:
                # Assuming DictCursor, keys are column names
                self.tabla_productos.setItem(fila, 0, QtWidgets.QTableWidgetItem(str(item['id_empleados']))) 
                self.tabla_productos.setItem(fila, 1, QtWidgets.QTableWidgetItem(str(item['nombre']))) 
                self.tabla_productos.setItem(fila, 2, QtWidgets.QTableWidgetItem(str(item['apellido_paterno']))) 
                self.tabla_productos.setItem(fila, 3, QtWidgets.QTableWidgetItem(str(item['apellido_materno']))) 
                self.tabla_productos.setItem(fila, 4, QtWidgets.QTableWidgetItem(str(item['fecha_alta'])))
                self.tabla_productos.setItem(fila, 5, QtWidgets.QTableWidgetItem(str(item['fecha_baja'] if item['fecha_baja'] else "")))
                self.tabla_productos.setItem(fila, 6, QtWidgets.QTableWidgetItem(str(item['activo'])))
                fila += 1
        else:
             self.tabla_productos.setRowCount(0)

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