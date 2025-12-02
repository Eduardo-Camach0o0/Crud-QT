#1.- Importar librerias
import sys
from PyQt5 import QtCore
from PyQt5.QtCore import QPropertyAnimation
from PyQt5 import QtCore, QtGui, QtWidgets, uic  


from modelo.productosActions import ProductosAct


class Load_ui_productos(QtWidgets.QMainWindow):

    #2.- Cargar archivo .ui
    def __init__(self):
        super().__init__()
        # Cargar archivo .ui
        uic.loadUi("ui/ui_productos.ui", self)
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

        self.accion_guardar.clicked.connect(self.guardar_producto)
        self.buscar_guardar.clicked.connect(self.buscar_guardar_producto)

        self.accion_actualizar.clicked.connect(self.actualizar_producto)
        self.buscar_actualizar.clicked.connect(self.buscar_actualizar_producto)

        self.accion_eliminar.clicked.connect(self.eliminar_producto)
        self.buscar_eliminar.clicked.connect(self.buscar_eliminar_producto)

        self.accion_limpiar.clicked.connect(self.limpiar_general)
        self.buscar_buscar.clicked.connect(self.buscar_general)

        self.boton_refresh.clicked.connect(self.actualizar_tabla)

        self.boton_actualizar.clicked.connect(self.limpiar)
        self.boton_agregar.clicked.connect(self.limpiar)
        self.boton_consultar.clicked.connect(self.limpiar)
        self.boton_eliminar.clicked.connect(self.limpiar)
        self.boton_buscar.clicked.connect(self.limpiar)



        # Instancias
        self.productoI = ProductosAct()
        


    def limpiar(self):
        self.productoI.producto.id_product = 0
        self.productoI.producto.descripcion = ""
        self.productoI.producto.cantidad = 0
        self.productoI.producto.precio = 0.0

    def menu(self):
        from load.load_iu_menu import VentanaMenu

        self.ventana_menu = VentanaMenu()
        self.ventana_menu.show()
        self.close()
        pass
 

    #Operaciones con el modelo de datos            
    def guardar_producto(self):

        if self.cantidad_agregar.text() == "" or self.descripcion_agregar.text() == "" or self.precio_agregar.text() == "":
            self.label.setText("Todos los campos son obligatorios")
        else:
            self.productoI.producto.descripcion = str(self.descripcion_agregar.text())
            self.productoI.producto.cantidad = int(self.cantidad_agregar.text())
            self.productoI.producto.precio = float(self.precio_agregar.text())
        
            response = self.productoI.InsertProducto()

            if response == "ok":
                self.label.setText("Producto añadido Existosamente")
                self.cantidad_agregar.setText("")
                self.descripcion_agregar.setText("")
                self.precio_agregar.setText("")
            else:
                self.label.setText("Error al agregar producto")

     
        pass

    
    def buscar_guardar_producto(self):
        self.label.setText("Función no disponible en Agregar")
        pass


    def actualizar_producto(self):

        if self.id_producto_actualizar.text() == "" or self.descripcion_actualizar.text() == "" or self.cantidad_actualizar.text() == "" or self.precio_actualizar.text() == "" :
            self.label.setText("Todos los campos son obligatorios")
        else:
            try:
                self.productoI.producto.id_product = int(self.id_producto_actualizar.text())
                self.productoI.producto.descripcion = str(self.descripcion_actualizar.text())
                self.productoI.producto.cantidad = int(self.cantidad_actualizar.text())
                self.productoI.producto.precio = float(self.precio_actualizar.text())
                

                response = self.productoI.UpdateProducto()

                if  response == "ok":
                    self.label.setText("Exito al actualizar producto")
                    self.id_producto_actualizar.setText("")
                    self.descripcion_actualizar.setText("")
                    self.cantidad_actualizar.setText("")
                    self.precio_actualizar.setText("")
                else:
                    self.label.setText("Error al actualizar producto")
            except ValueError:
                self.label.setText("Error: ID, Cantidad o Precio inválidos")


        pass


    def buscar_actualizar_producto(self):
        
        if self.id_producto_actualizar.text() == "":
             self.label.setText("Ingrese ID para buscar")
             return

        try:
            self.productoI.producto.id_product = int(self.id_producto_actualizar.text())

            if self.productoI.searchProducto() == []:
                self.label.setText("No existe ese producto")
            else:
                data = self.productoI.searchProducto()[0]
                self.label.setText("")
            
                if isinstance(data, dict):
                    self.id_producto_actualizar.setText(str(data['id_producto']))
                    self.descripcion_actualizar.setText(str(data['descripcion']))
                    self.cantidad_actualizar.setText(str(data['cantidad']))
                    self.precio_actualizar.setText(str(data['precio']))
                else:
                    # Fallback si no es dict
                    self.id_producto_actualizar.setText(str(data[0]))
                    self.descripcion_actualizar.setText(str(data[1]))
                    self.precio_actualizar.setText(str(data[2]))
                    self.cantidad_actualizar.setText(str(data[3]))
        except ValueError:
            self.label.setText("ID inválido")

        pass



    def eliminar_producto(self):
        if self.id_producto_eliminar.text() == "":
            self.label.setText("Ingrese ID para eliminar")
        else:
            try:
                self.productoI.producto.id_product = int(self.id_producto_eliminar.text())
                response = self.productoI.DeleteProducto()
                if  response == "ok":
                    self.label.setText("Exito al eliminar producto")
                    self.id_producto_eliminar.setText("")
                    self.descripcion_eliminar.setText("")
                    self.cantidad_eliminar.setText("")
                    self.precio_eliminar.setText("")
                else:
                    self.label.setText("Error al eliminar el producto")
            except ValueError:
                self.label.setText("ID inválido")

        pass 
    

    def buscar_eliminar_producto(self):

        if self.id_producto_eliminar.text() == "":
             self.label.setText("Ingrese ID para buscar")
             return

        try:
            self.productoI.producto.id_product = int(self.id_producto_eliminar.text())
            if self.productoI.searchProducto() == []:
                self.label.setText("No existe ese producto")
            else:
                data = self.productoI.searchProducto()[0]
                self.label.setText("")
                if isinstance(data, dict):
                    self.id_producto_eliminar.setText(str(data['id_producto']))
                    self.descripcion_eliminar.setText(str(data['descripcion']))
                    self.cantidad_eliminar.setText(str(data['cantidad']))
                    self.precio_eliminar.setText(str(data['precio']))
                else:
                    self.id_producto_eliminar.setText(str(data[0]))
                    self.descripcion_eliminar.setText(str(data[1]))
                    self.precio_eliminar.setText(str(data[2]))
                    self.cantidad_eliminar.setText(str(data[3]))
        except ValueError:
            self.label.setText("ID inválido")

        pass


    def buscar_general(self):
        if self.id_producto_buscar.text() == "":
             self.label.setText("Ingrese ID para buscar")
             return

        try:
            self.productoI.producto.id_product = int(self.id_producto_buscar.text())
            if self.productoI.searchProducto() == []:
                self.label.setText("No existe ese producto")
            else:
                data = self.productoI.searchProducto()[0]
                self.label.setText("")
                if isinstance(data, dict):
                    self.id_producto_buscar.setText(str(data['id_producto']))
                    self.descripcion_buscar.setText(str(data['descripcion']))
                    self.cantidad_buscar.setText(str(data['cantidad']))
                    self.precio_buscar.setText(str(data['precio']))
                else:
                    self.id_producto_buscar.setText(str(data[0]))
                    self.descripcion_buscar.setText(str(data[1]))
                    self.precio_buscar.setText(str(data[2]))
                    self.cantidad_buscar.setText(str(data[3]))
        except ValueError:
            self.label.setText("ID inválido")
            
        pass


    def limpiar_general(self):
        self.id_producto_buscar.setText("")
        self.descripcion_buscar.setText("")
        self.cantidad_buscar.setText("")
        self.precio_buscar.setText("")



    def actualizar_tabla(self):
        data = self.productoI.selectProductos()
        self.tabla_productos.setRowCount(len(data))
        fila = 0

        for item in data:
            if isinstance(item, dict):
                self.tabla_productos.setItem(fila, 0, QtWidgets.QTableWidgetItem(str(item.get('id_producto', ''))))
                self.tabla_productos.setItem(fila, 1, QtWidgets.QTableWidgetItem(str(item.get('descripcion', ''))))
                self.tabla_productos.setItem(fila, 2, QtWidgets.QTableWidgetItem(str(item.get('precio', ''))))
                self.tabla_productos.setItem(fila, 3, QtWidgets.QTableWidgetItem(str(item.get('cantidad', ''))))
                self.tabla_productos.setItem(fila, 4, QtWidgets.QTableWidgetItem(str(item.get('estado', ''))))
            else:
                self.tabla_productos.setItem(fila, 0, QtWidgets.QTableWidgetItem(str(item[0])))
                self.tabla_productos.setItem(fila, 1, QtWidgets.QTableWidgetItem(str(item[1])))
                self.tabla_productos.setItem(fila, 2, QtWidgets.QTableWidgetItem(str(item[2])))
                self.tabla_productos.setItem(fila, 3, QtWidgets.QTableWidgetItem(str(item[3])))
                self.tabla_productos.setItem(fila, 4, QtWidgets.QTableWidgetItem(str(item[4])))
            fila += 1

    
        
    
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