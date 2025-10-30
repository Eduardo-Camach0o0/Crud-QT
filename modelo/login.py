import bcrypt
from modelo.conexion import Conexion


class LoginVal():

    def __init__(self, username, password, fullname = None):
        self.conexion = Conexion()
        self.user = username
        self.pswd = password 
        self.fullname = fullname
        

    def crear_nuevo_usuario(self):
        cursor = None  
        try:
            password_bytes = self.pswd.encode('utf-8')
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password_bytes, salt)
            hashed_password_str = hashed_password.decode('utf-8') 

            self.conexion.establecerConexio()
            cursor = self.conexion.conexion.cursor()
            
            sp = "EXEC sp_CrearUsuario @Username=?, @FullName=?, @Password=?"
            params = (self.user, self.fullname, hashed_password_str)
            
            cursor.execute(sp, params)
            cursor.commit()
            
            print(f"Usuario '{self.user}' creado exitosamente.")
            return True

        except Exception as e:
            print(f"Error al crear usuario: {e}")
            if cursor:
                cursor.rollback() 
            return False
        finally:
            if cursor:
                cursor.close()
            self.conexion.cerrarConexion()
    

    def validar_login(self):
        cursor = None
        try:
            
            self.conexion.establecerConexio()
            cursor = self.conexion.conexion.cursor()

            sp = "EXEC sp_ObtenerPasswordPorUsuario @Username=?"
            params = (self.user,)
            
            cursor.execute(sp, params)
            resultado = cursor.fetchone()

            if not resultado:
                print(f"Usuario '{self.user}' no encontrado.")
                return False
            
            hashed_password_from_db = resultado[0]

            password_bytes_plana = self.pswd.encode('utf-8')
            hash_bytes_from_db = hashed_password_from_db.encode('utf-8')

        
            if bcrypt.checkpw(password_bytes_plana, hash_bytes_from_db):
                print(f"Login exitoso. ¡Bienvenido {self.user}!")
                return True
            else:
                print("Contraseña incorrecta.")
                return False

        except Exception as e:
            print(f"Error durante el login: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            self.conexion.cerrarConexion()
    


# a = LoginVal("Edu","Desarollo","Eduardo Camacho")
# a.crear_nuevo_usuario()
