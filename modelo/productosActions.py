
from modelo.conexion import get_connection
from modelo.producto import Producto

# from conexion import get_connection
# from producto import Producto

class ProductosAct():

    def __init__(self):
        self.producto = Producto()

    def execute_procedure(self, procedure_name, args=None):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.callproc(procedure_name, args or [])
            conn.commit()
            return "ok"
        except Exception as e:
            print(f"Error executing {procedure_name}: {e}")
            return None
        finally:
            conn.close()

    def fetch_procedure(self, procedure_name, args=None):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.callproc(procedure_name, args or [])
                return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching {procedure_name}: {e}")
            return []
        finally:
            conn.close()

    def selectProductos(self):
        return self.fetch_procedure("sp_producto_listar")

    def InsertProducto(self):
        return self.execute_procedure("sp_producto_nuevo", [
            self.producto.descripcion, 
            self.producto.precio, 
            self.producto.cantidad
        ])
    
    def UpdateProducto(self):
        return self.execute_procedure("sp_producto_actualizar", [
            self.producto.id_product, 
            self.producto.descripcion, 
            self.producto.precio
        ])

    def DeleteProducto(self):
        return self.execute_procedure("sp_producto_eliminar", [self.producto.id_product])

    def searchProducto(self):
        return self.fetch_procedure("sp_producto_buscar", [self.producto.id_product])

    def setEstadoProducto(self):
        return self.execute_procedure("sp_producto_set_estado", [
            self.producto.id_product, 
            self.producto.estado
        ])



# a = ProductosAct()
# a.InsertProducto()
# a.selectProductos()
# a.UpdateProducto()
# a.DeleteProducto()
# a.CountProducto()