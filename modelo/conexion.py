import pyodbc

class Conexion():
    def __init__(self):
        self.conexion = ""
    
    def establecerConexio(self):
        try:
            self.conexion = pyodbc.connect('DRIVER={SQL SERVER}; SERVER=ROGEDU\SQLEXPRESS;DATABASE=bdsistema; UID:ROGEDU\eduar; PWD:""')
            print("SIUUUUUUUUUUU")
        except Exception as ex:
            print("No peloo")

    def cerrarConexion(self):
        self.conexion.close()



        

# a = Conexion()
# a.establecerConexio()
