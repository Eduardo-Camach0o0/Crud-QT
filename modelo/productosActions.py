from modelo.conexion import Conexion
from modelo.producto import Producto

class ProductosAct():

    def __init__(self):
        self.conexion = Conexion()
        self.producto = Producto()

    def selectProductos(self):
        self.conexion.establecerConexio()
        cursor =  self.conexion.conexion.cursor()
        query = "SELECT * FROM producto"
        cursor.execute(query)
        filas = cursor.fetchall()

        # for fila in filas:
        #     print(fila)
        
        self.conexion.cerrarConexion()
        return filas

    def InsertProducto(self):
        self.conexion.establecerConexio()
        sp = "exec [dbo].[sp_insertar_producto] @clave=?, @descripcion=?, @existencia=?, @precio=?"
        param = (self.producto.clave,self.producto.descripcion, self.producto.existencia,self.producto.precio )
        cursor =  self.conexion.conexion.cursor()
        cursor.execute(sp, param)
        cursor.commit()
        self.conexion.cerrarConexion()
        print("ok")
        return "ok"
    
    def UpdateProducto(self):
        self.conexion.establecerConexio()
        sp = "exec [dbo].[sp_actualizar_producto] @id_producto=?,@clave=?, @descripcion=?, @existencia=?, @precio=?"
        param = (self.producto.id_product,self.producto.clave,self.producto.descripcion, self.producto.existencia,self.producto.precio )
        cursor =  self.conexion.conexion.cursor()
        cursor.execute(sp, param)
        cursor.commit()
        self.conexion.cerrarConexion()
        print("ok")
        return "ok"

    def DeleteProducto(self):
        self.conexion.establecerConexio()
        sp = "exec [dbo].[sp_eliminar_producto] @id_producto=?"
        param = (self.producto.id_product, )
        cursor =  self.conexion.conexion.cursor()
        cursor.execute(sp, param)
        cursor.commit()
        self.conexion.cerrarConexion()
        print("ok")
        return "ok"


    def searchProducto(self):
        self.conexion.establecerConexio()
        sp = "exec  [dbo].[sp_buscar_producto] @SKU=?"
        param = (self.producto.clave, )
        cursor =  self.conexion.conexion.cursor()
        cursor.execute(sp, param)
        fila = cursor.fetchall()
        cursor.commit()
        self.conexion.cerrarConexion()
       
        return fila



    def CountProducto(self):
        self.conexion.establecerConexio()
        funcion = "SELECT [dbo].[fn_contar_productos]()"
       
        cursor =  self.conexion.conexion.cursor()
        cursor.execute(funcion)
        cantidad = cursor.fetchone()
        print(cantidad[0])
        # cursor.commit()
        self.conexion.cerrarConexion()
        print("ok")



# a = ProductosAct()
# a.InsertProducto()
# a.selectProductos()
# a.UpdateProducto()
# a.DeleteProducto()
# a.CountProducto()