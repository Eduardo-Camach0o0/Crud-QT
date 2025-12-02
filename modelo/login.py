import bcrypt
import pymysql 
from modelo.conexion import get_connection

class LoginVal():

    def __init__(self, username, password, fullname = None):
        self.conexion = get_connection()
        # CORRECCIÓN 1: Asignar las variables que entran como parámetro
        self.user = username      
        self.pswd = password      
        self.fullname = fullname  

    def crear_nuevo_usuario(self):
        cursor = None  
        try:
            # Encriptación
            password_bytes = self.pswd.encode('utf-8')
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password_bytes, salt)
            hashed_password_str = hashed_password.decode('utf-8') 

            cursor = self.conexion.cursor()
            
            # Ejecución del SP
            sp = "CALL sp_agregar_usuario(%s, %s, %s)"
            params = (self.user, hashed_password_str, self.fullname)
            
            cursor.execute(sp, params)
            self.conexion.commit()
            
            print(f"✅ Usuario '{self.user}' creado exitosamente.")
            return True

        except Exception as e:
            print(f"❌ Error al crear usuario: {e}")
            self.conexion.rollback() 
            return False
        finally:
            if cursor:
                cursor.close()
        

    def validar_login(self):
        cursor = None
        try:
            cursor = self.conexion.cursor(pymysql.cursors.DictCursor)

            sp = "CALL sp_validar_usuario(%s)"
            params = (self.user,)
            
            cursor.execute(sp, params)
            resultado = cursor.fetchone() 

            if not resultado:
                print(f"⚠️ Usuario '{self.user}' no encontrado.")
                return False
            
            hashed_password_from_db = resultado.get('contraseña') 
            
            # Si no encuentra la clave 'contraseña', intenta tomar el primer valor (por si se llama 'password' o 'pass')
            if not hashed_password_from_db:
                 hashed_password_from_db = list(resultado.values())[0]

            password_bytes_plana = self.pswd.encode('utf-8')
            
            # Convertir a bytes si viene como string de la BD
            if isinstance(hashed_password_from_db, str):
                hash_bytes_from_db = hashed_password_from_db.encode('utf-8')
            else:
                hash_bytes_from_db = hashed_password_from_db

            # Comparar
            if bcrypt.checkpw(password_bytes_plana, hash_bytes_from_db):
                print(f"🚀 Login exitoso. ¡Bienvenido {self.user}!")
                return True
            else:
                print("❌ Contraseña incorrecta.")
                return False

        except Exception as e:
            print(f"❌ Error durante el login: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
                # self.conexion.close()


    def cerrar_conexion(self):
        if self.conexion:
            self.conexion.close()

# # --- PRUEBA ---
# # Ahora sí pasamos los datos reales
# a = LoginVal("Toño", "Desarollo", "Toño Lopez")

# # 1. Intentamos crear el usuario
# if a.crear_nuevo_usuario():
#     # 2. Si se crea, intentamos loguearnos inmediatamente para probar
#     a.validar_login()

# a.cerrar_conexion()