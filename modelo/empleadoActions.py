from modelo.conexion import get_connection
from modelo.empleado import Empleado

# from conexion import get_connection
# from empleado import Empleado

class EmpleadosAct():

    def __init__(self):
        self.empleado = Empleado()

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

    def selectEmpleado(self):
        return self.fetch_procedure("sp_empleado_listar")

    def InsertEmpleado(self):
        return self.execute_procedure("sp_empleado_nuevo", [
            self.empleado.Nombre, 
            self.empleado.ApellidoPaterno, 
            self.empleado.ApellidoMaterno
        ])
    
    def UpdateEmpleado(self):
        return self.execute_procedure("sp_empleado_actualizar", [
            self.empleado.idEmpleado, 
            self.empleado.Nombre, 
            self.empleado.ApellidoPaterno, 
            self.empleado.ApellidoMaterno
        ])

    def DeleteEmpleado(self):
        return self.execute_procedure("sp_empleado_eliminar", [self.empleado.idEmpleado])

    def searchEmpleado(self):
        return self.fetch_procedure("sp_empleado_buscar", [self.empleado.idEmpleado])

# a = EmpleadosAct()
# print(a.InsertEmpleado())
# a.selectProductos()
# a.UpdateProducto()
# a.DeleteProducto()
# a.CountProducto()