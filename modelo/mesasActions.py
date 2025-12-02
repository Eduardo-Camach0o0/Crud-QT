from modelo.conexion import get_connection

class MesasAct():

    def __init__(self):
        pass

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

    # =========================================================
    #   C) MESAS
    # =========================================================
    def mesa_listar(self):
        return self.fetch_procedure("sp_mesa_listar")

    def mesa_set_estado(self, id_mesa, estado):
        return self.execute_procedure("sp_mesa_set_estado", [id_mesa, estado])

    def mesa_abrir(self, id_mesa, id_empleado):
        return self.execute_procedure("sp_mesa_abrir", [id_mesa, id_empleado])

    def mesa_cerrar(self, id_mesa):
        return self.execute_procedure("sp_mesa_cerrar", [id_mesa])

    # =========================================================
    #   D) PEDIDOS
    # =========================================================
    def pedido_cambiar_estado(self, id_pedido, estado):
        return self.execute_procedure("sp_pedido_cambiar_estado", [id_pedido, estado])

    def pedido_cancelar(self, id_pedido):
        return self.execute_procedure("sp_pedido_cancelar", [id_pedido])

    def pedido_obtener(self, id_pedido):
        return self.fetch_procedure("sp_pedido_obtener", [id_pedido])

    # =========================================================
    #   E) DETALLE DE PEDIDO
    # =========================================================
    def detalle_agregar(self, id_pedido, id_producto, cantidad):
        return self.execute_procedure("sp_detalle_agregar", [id_pedido, id_producto, cantidad])

    def detalle_eliminar(self, id_detalle):
        return self.execute_procedure("sp_detalle_eliminar", [id_detalle])

    def detalle_listar_por_pedido(self, id_pedido):
        return self.fetch_procedure("sp_detalle_listar_por_pedido", [id_pedido])

    # =========================================================
    #   F) TICKETS
    # =========================================================
    def ticket_generar(self, id_pedido, metodo_pago):
        return self.execute_procedure("sp_ticket_generar", [id_pedido, metodo_pago])

    def ticket_listar(self):
        return self.fetch_procedure("sp_ticket_listar")

    def listar_pedidos_pendientes(self):
        return self.fetch_procedure("sp_listar_pedidos_pendientes")
