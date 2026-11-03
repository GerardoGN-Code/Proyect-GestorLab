from Base_de_datos.conexion import ConexionDB

class ControladorAdmin:
    def __init__(self):
        self.db = ConexionDB()

    def obtener_lista_grupos(self):
        resultados = self.db.ejecutar_consulta("SELECT DISTINCT Grupo FROM asignaciones WHERE Grupo IS NOT NULL ORDER BY Grupo")
        return [fila['Grupo'] for fila in (resultados or [])]

    def obtener_lista_laboratorios(self):
        resultados = self.db.ejecutar_consulta("SELECT Nombre_lab FROM laboratorios ORDER BY Nombre_lab")
        return [fila['Nombre_lab'] for fila in (resultados or [])]

    def obtener_horarios_completos(self):
        query = """
            SELECT a.Dia_semana, a.Hora_inicio, a.Hora_final, a.Grupo,
                   r.Materia as Nombre_materia, u.Usuario as Nombre_docente, l.Nombre_lab
            FROM asignaciones a
            LEFT JOIN reticula_isc r ON a.Clave_materia = r.Clave_Materia
            LEFT JOIN Usuarios u ON a.Matricula_docente = u.Matricula
            LEFT JOIN laboratorios l ON a.id_lab = l.id_Lab
        """
        return self.db.ejecutar_consulta(query) or []

    def obtener_todos_los_docentes(self):
        return self.db.ejecutar_consulta("SELECT * FROM Usuarios WHERE rol = 'Docente' ORDER BY Usuario") or []

    def agregar_docente(self, matricula, nombre, contrasena):
        sql = "INSERT INTO Usuarios (Matricula, Usuario, Contrasena, rol, Estado) VALUES (?, ?, ?, 'Docente', 'Activo')"
        if self.db.ejecutar_modificacion(sql, (matricula, nombre, contrasena)):
            return {'exito': True, 'mensaje': 'Docente agregado.'}
        return {'exito': False, 'mensaje': 'Error al agregar docente (posible matrícula duplicada).'}
            
    def actualizar_docente(self, id_usuario, matricula, nombre, contrasena):
        sql = "UPDATE Usuarios SET Matricula = ?, Usuario = ?, Contrasena = ? WHERE id_usuario = ?"
        if self.db.ejecutar_modificacion(sql, (matricula, nombre, contrasena, id_usuario)):
            return {'exito': True, 'mensaje': 'Docente actualizado.'}
        return {'exito': False, 'mensaje': 'Error al actualizar.'}

    def cambiar_estado_docente(self, id_usuario, nuevo_estado):
        sql = "UPDATE Usuarios SET Estado = ? WHERE id_usuario = ?"
        if self.db.ejecutar_modificacion(sql, (nuevo_estado, id_usuario)):
            return {'exito': True}
        return {'exito': False, 'mensaje': 'No se pudo cambiar el estado.'}

    def obtener_laboratorios(self):
        return self.db.ejecutar_consulta("SELECT * FROM laboratorios ORDER BY Nombre_lab") or []

    def agregar_laboratorio(self, nombre, capacidad, equipos, ubicacion):
        sql = "INSERT INTO laboratorios (Nombre_lab, Capacidad, Cantidad_equipos, Ubicacion, Estado) VALUES (?, ?, ?, ?, 'Disponible')"
        if self.db.ejecutar_modificacion(sql, (nombre, capacidad, equipos, ubicacion)):
            return {'exito': True, 'mensaje': 'Laboratorio creado.'}
        return {'exito': False, 'mensaje': 'Error al agregar laboratorio.'}

    def actualizar_laboratorio(self, id_lab, nombre, capacidad, equipos, ubicacion, estado):
        sql = "UPDATE laboratorios SET Nombre_lab=?, Capacidad=?, Cantidad_equipos=?, Ubicacion=?, Estado=? WHERE id_Lab=?"
        if self.db.ejecutar_modificacion(sql, (nombre, capacidad, equipos, ubicacion, estado, id_lab)):
            return {'exito': True, 'mensaje': 'Laboratorio actualizado.'}
        return {'exito': False, 'mensaje': 'Error al actualizar.'}

    def cambiar_estado_laboratorio(self, id_lab, nuevo_estado):
        sql = "UPDATE laboratorios SET Estado = ? WHERE id_Lab = ?"
        if self.db.ejecutar_modificacion(sql, (nuevo_estado, id_lab)):
            return {'exito': True}
        return {'exito': False, 'mensaje': 'No se pudo cambiar el estado.'}