from modelo.conexion import Conexion
from modelo.empleado import Empleado

class EmpleadosAct():

    def __init__(self):
        self.conexion = Conexion()
        self.empleado = Empleado()

    def selectEmpleado(self):
        self.conexion.establecerConexio()
        cursor =  self.conexion.conexion.cursor()
        query = "SELECT * FROM Empleados"
        cursor.execute(query)
        filas = cursor.fetchall()

        for fila in filas:
            print(fila)
        
        self.conexion.cerrarConexion()

        return filas

    def InsertEmpleado(self):
        self.conexion.establecerConexio()
        sp = "exec [dbo].[sp_insertar_empleado] @Nombre=?, @CuentaClabe=?, @Turno=?"
        param = (self.empleado.Nombre,self.empleado.CuentaClabe, self.empleado.Turno)
        cursor =  self.conexion.conexion.cursor()
        cursor.execute(sp, param)
        cursor.commit()
        self.conexion.cerrarConexion()
        print("ok")
        return "ok"
    
    def UpdateEmpleado(self):
        self.conexion.establecerConexio()
        sp = "exec [dbo].[sp_actualizar_empleado] @IdEmpleado=?,@Nombre=?, @CuentaClabe=?, @Turno=?"
        param = (self.empleado.idEmpleado,self.empleado.Nombre,self.empleado.CuentaClabe, self.empleado.Turno)
        cursor =  self.conexion.conexion.cursor()
        cursor.execute(sp, param)
        cursor.commit()
        self.conexion.cerrarConexion()
        print("ok")
        return "ok"

    def DeleteEmpleado(self):
        self.conexion.establecerConexio()
        sp = "exec [dbo].[sp_eliminar_empleado]@IdEmpleado=?"
        param = (self.empleado.idEmpleado, )
        cursor =  self.conexion.conexion.cursor()
        cursor.execute(sp, param)
        cursor.commit()
        self.conexion.cerrarConexion()
        print("ok")

        return "ok"

    def searchEmpleado(self):
        self.conexion.establecerConexio()
        sp = "exec [dbo].[sp_BuscarEmpleado] @Name_Empleado=?"
        param = (self.empleado.Nombre, )
        cursor =  self.conexion.conexion.cursor()
        cursor.execute(sp, param)
        fila = cursor.fetchall()
        cursor.commit()
        self.conexion.cerrarConexion()
        return fila




# a = EmpleadosAct()
# a.InsertEmpleado()
# a.selectProductos()
# a.UpdateProducto()
# a.DeleteProducto()
# a.CountProducto()