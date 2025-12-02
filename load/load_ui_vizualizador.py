from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QLabel, QFrame, QVBoxLayout

from modelo.mesasActions import MesasAct

class Vizualizador(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/vizualizador_coman.ui", self)
        
        # Conectar botón de regresar
        self.btn_regresar.clicked.connect(self.ir_a_menu)

        # Instancia del modelo
        self.mesasAct = MesasAct()

        # Cargar mesas al iniciar
        self.cargar_mesas()

    def ir_a_menu(self):
        from load.load_iu_menu import VentanaMenu
        self.ventana_menu = VentanaMenu()
        self.ventana_menu.show()
        self.close()

    def cargar_mesas(self):
        # Limpiar grid actual (eliminar widgets de prueba del diseñador)
        for i in reversed(range(self.gridLayout.count())): 
            item = self.gridLayout.itemAt(i)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.gridLayout.removeItem(item)
from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QLabel, QFrame, QVBoxLayout

from modelo.mesasActions import MesasAct

class Vizualizador(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/vizualizador_coman.ui", self)
        
        # Conectar botón de regresar
        self.btn_regresar.clicked.connect(self.ir_a_menu)

        # Instancia del modelo
        self.mesasAct = MesasAct()

        # Cargar mesas al iniciar
        self.cargar_mesas()

    def ir_a_menu(self):
        from load.load_iu_menu import VentanaMenu
        self.ventana_menu = VentanaMenu()
        self.ventana_menu.show()
        self.close()

    def cargar_mesas(self):
        # Limpiar grid actual (eliminar widgets de prueba del diseñador)
        for i in reversed(range(self.gridLayout.count())): 
            item = self.gridLayout.itemAt(i)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.gridLayout.removeItem(item)

        # Obtener mesas de la BD
        mesas = self.mesasAct.mesa_listar()
        
        # Obtener pedidos pendientes
        pedidos = self.mesasAct.listar_pedidos_pendientes()
        self.all_pedidos = pedidos # Guardar para uso en sidebar
        
        # Agrupar pedidos por mesa
        pedidos_por_mesa = {}
        if pedidos:
            for pedido in pedidos:
                # Ajustar clave id_mesa según lo que devuelva el SP
                id_mesa_p = pedido.get('id_mesa') or pedido.get('MesaID')
                if id_mesa_p:
                    if id_mesa_p not in pedidos_por_mesa:
                        pedidos_por_mesa[id_mesa_p] = []
                    pedidos_por_mesa[id_mesa_p].append(pedido)

        # Si no hay mesas o error
        if not mesas:
            print("No se encontraron mesas o hubo un error.")
            return

        # Configuración del Grid
        columnas = 4 
        row = 0
        col = 0

        for mesa in mesas:
            # Asumiendo que 'mesa' es un diccionario: {'id_mesa': 1, 'nombre': 'Mesa 1', 'estado': 'Libre'}
            # Ajustar claves según la respuesta real del SP
            id_mesa = mesa.get('id_mesa') or mesa.get('id') or 0 # Fallback
            nombre = str(mesa.get('nombre') or f"Mesa {id_mesa}")
            estado = str(mesa.get('estado') or 'Desconocido')
            
            # Obtener pedidos para esta mesa
            lista_pedidos = pedidos_por_mesa.get(id_mesa, [])

            # Crear el widget de la mesa
            widget_mesa = self.crear_widget_mesa(id_mesa, nombre, estado, lista_pedidos)
            
            # Añadir al grid
            self.gridLayout.addWidget(widget_mesa, row, col)

            # Calcular siguiente posición
            col += 1
            if col >= columnas:
                col = 0
                row += 1

    def crear_widget_mesa(self, id_mesa, nombre, estado, pedidos=[]):
        frame = QFrame()
        frame.setMinimumSize(160, 220) # Aumentar altura
        frame.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        
        # Definir estilos según estado
        color_bg = "rgba(229, 231, 235, 0.5)" # Gris default
        color_border = "#9ca3af"
        color_text = "#374151"
        icon_text = "?"

        estado_lower = str(estado).lower()
        
        if "1" in estado_lower: # libre
            color_bg = "rgba(34, 197, 94, 0.1)" # Verde
            color_border = "#22c55e"
            color_text = "#166534"
            icon_text = "✓"
        elif "2" in estado_lower: # ocupada
            color_bg = "rgba(59, 130, 246, 0.1)" # Azul
            color_border = "#3b82f6"
            color_text = "#1e40af"
            icon_text = "🍽"
        elif "3" in estado_lower: # esperando
            color_bg = "rgba(234, 179, 8, 0.1)" # Amarillo
            color_border = "#eab308"
            color_text = "#854d0e"
            icon_text = "🕒"
        elif "4" in estado_lower: # pago
            color_bg = "rgba(168, 85, 247, 0.1)" # Morado
            color_border = "#a855f7"
            color_text = "#6b21a8"
            icon_text = "💳"

        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {color_bg};
                border: 2px solid {color_border};
                border-radius: 12px;
                color: {color_text};
            }}
            QFrame:hover {{
                background-color: {color_bg.replace('0.1', '0.2')};
            }}
        """)

        layout = QVBoxLayout(frame)

        # Header (Icono + Nombre)
        header_layout = QtWidgets.QHBoxLayout()
        
        lbl_nombre = QLabel(str(nombre))
        lbl_nombre.setStyleSheet("border: none; font-weight: bold; font-size: 18px;") # Aumentado
        header_layout.addWidget(lbl_nombre)
        
        lbl_icon = QLabel(icon_text)
        lbl_icon.setStyleSheet("border: none; font-size: 24px;")
        lbl_icon.setAlignment(QtCore.Qt.AlignRight)
        header_layout.addWidget(lbl_icon)
        
        layout.addLayout(header_layout)

        # Estado
        lbl_estado = QLabel(str(estado))
        lbl_estado.setStyleSheet("border: none; font-size: 14px; font-style: italic;") # Aumentado
        lbl_estado.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(lbl_estado)
        
        # Separador
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet(f"background-color: {color_border}; border: none; max-height: 1px;")
        layout.addWidget(line)

        # Lista de Pedidos
        if pedidos:
            lbl_pedidos_titulo = QLabel("Pendientes:")
            lbl_pedidos_titulo.setStyleSheet("border: none; font-weight: bold; font-size: 14px; margin-top: 5px;") # Aumentado
            layout.addWidget(lbl_pedidos_titulo)
            
            for p in pedidos:
                # Ajustar claves: nombre_producto, cantidad
                prod = p.get('nombre_producto') or p.get('producto') or 'Item'
                cant = p.get('cantidad') or 1
                lbl_p = QLabel(f"• {prod} x{cant}")
                lbl_p.setStyleSheet("border: none; font-size: 13px; font-weight: 500;") # Aumentado
                layout.addWidget(lbl_p)
        else:
            lbl_no_pedidos = QLabel("Sin pedidos")
            lbl_no_pedidos.setStyleSheet("border: none; color: gray; font-size: 12px;")
            layout.setAlignment(QtCore.Qt.AlignCenter)
            layout.addWidget(lbl_no_pedidos)

        layout.addStretch()

        # Evento Click
        frame.id_mesa = id_mesa
        frame.mousePressEvent = self.crear_evento_click(id_mesa)

        return frame

    def crear_evento_click(self, id_mesa):
        def evento(event):
            self.seleccionar_mesa(id_mesa)
        return evento

    def seleccionar_mesa(self, id_mesa):
        print(f"Mesa seleccionada: {id_mesa}")
        self.lblTableName.setText(f"Mesa {id_mesa}")
        
        # Limpiar sidebar actual
        # Asumiendo que el layout donde van los items es vl_items (según el UI file analizado)
        # Si no existe, hay que verificar el nombre en el .ui o usar findChild
        layout_items = self.findChild(QVBoxLayout, 'vl_items')
        
        if layout_items:
            # Limpiar items anteriores
            while layout_items.count():
                item = layout_items.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
                elif item.layout():
                    # Si es un layout anidado (como el row de cada item), borrar sus widgets
                    sublayout = item.layout()
                    while sublayout.count():
                        subitem = sublayout.takeAt(0)
                        if subitem.widget():
                            subitem.widget().deleteLater()
                    sublayout.deleteLater()

            # Filtrar pedidos de esta mesa
            pedidos_mesa = [p for p in getattr(self, 'all_pedidos', []) if (p.get('id_mesa') or p.get('MesaID')) == id_mesa]
            
            total = 0.0
            
            if pedidos_mesa:
                for p in pedidos_mesa:
                    prod_nombre = p.get('nombre_producto') or p.get('producto') or 'Producto'
                    cantidad = p.get('cantidad') or 1
                    precio_unit = float(p.get('precio') or p.get('precio_unitario') or 0.0)
                    subtotal = precio_unit * cantidad
                    total += subtotal
                    
                    # Crear widget del item (Row)
                    row_widget = QtWidgets.QWidget()
                    row_layout = QtWidgets.QHBoxLayout(row_widget)
                    row_layout.setContentsMargins(0, 0, 0, 0)
                    
                    # Cantidad
                    lbl_qty = QLabel(f"{cantidad}x")
                    lbl_qty.setFixedSize(40, 40)
                    lbl_qty.setStyleSheet("background-color: #f3f4f6; border-radius: 8px; color: #4b5563; font-weight: bold;")
                    lbl_qty.setAlignment(QtCore.Qt.AlignCenter)
                    row_layout.addWidget(lbl_qty)
                    
                    # Info (Nombre)
                    lbl_name = QLabel(str(prod_nombre))
                    lbl_name.setStyleSheet("font-size: 14px; font-weight: 500; color: #1f2937;")
                    row_layout.addWidget(lbl_name)
                    
                    row_layout.addStretch()
                    
                    # Precio
                    lbl_price = QLabel(f"${subtotal:.2f}")
                    lbl_price.setStyleSheet("font-weight: bold; color: #1f2937;")
                    row_layout.addWidget(lbl_price)
                    
                    layout_items.addWidget(row_widget)
                
                layout_items.addStretch()
                
                # Agregar Total al final (o actualizar un label de total si existe)
                # Voy a agregar un separador y el total al final de la lista
                
                line = QFrame()
                line.setFrameShape(QFrame.HLine)
                line.setFrameShadow(QFrame.Sunken)
                line.setStyleSheet("background-color: #e5e7eb; margin-top: 10px;")
                layout_items.addWidget(line)
                
                total_widget = QtWidgets.QWidget()
                total_layout = QtWidgets.QHBoxLayout(total_widget)
                
                lbl_total_txt = QLabel("Total:")
                lbl_total_txt.setStyleSheet("font-size: 18px; font-weight: bold;")
                total_layout.addWidget(lbl_total_txt)
                
                total_layout.addStretch()
                
                lbl_total_val = QLabel(f"${total:.2f}")
                lbl_total_val.setStyleSheet("font-size: 18px; font-weight: bold; color: #4f46e5;")
                total_layout.addWidget(lbl_total_val)
                
                layout_items.addWidget(total_widget)

            else:
                lbl_empty = QLabel("No hay pedidos pendientes")
                lbl_empty.setStyleSheet("color: #6b7280; font-style: italic; margin-top: 20px;")
                lbl_empty.setAlignment(QtCore.Qt.AlignCenter)
                layout_items.addWidget(lbl_empty)
                layout_items.addStretch()
