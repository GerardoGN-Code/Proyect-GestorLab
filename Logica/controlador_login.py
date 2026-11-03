from Base_de_datos.conexion import ConexionDB

class ControladorLogin:
    def __init__(self):
        self.db = ConexionDB()

    def autenticar_usuario(self, usuario_o_matricula, contrasena):
        query = """
            SELECT id_usuario, Usuario, rol, Estado 
            FROM Usuarios 
            WHERE (Matricula = ? OR Usuario = ?) AND Contrasena = ?
        """
        resultados = self.db.ejecutar_consulta(query, (usuario_o_matricula, usuario_o_matricula, contrasena))
        
        if resultados:
            usuario = resultados[0] 
            if usuario['Estado'].lower() != 'activo':
                return {'exito': False, 'mensaje': 'Usuario inactivo. Contacte al administrador.'}
            
            return {
                'exito': True, 
                'mensaje': 'Autenticación exitosa',
                'datos': usuario
            }
        elif resultados is None:
            return {'exito': False, 'mensaje': 'Error de conexión a la base de datos.'}
        else:
            return {'exito': False, 'mensaje': 'Credenciales incorrectas.'}