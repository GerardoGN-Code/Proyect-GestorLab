from Base_de_datos.conexion import ConexionDB

class ControladorDocente:
    def __init__(self):
        self.db = ConexionDB()

    def obtener_horario_docente(self, nombre_docente):
        query = """
            SELECT a.Dia_semana, a.Hora_inicio, a.Hora_final, a.Grupo,
                   r.Materia as Nombre_materia, l.Nombre_lab
            FROM asignaciones a
            LEFT JOIN reticula_isc r ON a.Clave_materia = r.Clave_Materia
            LEFT JOIN Usuarios u ON a.Matricula_docente = u.Matricula
            LEFT JOIN laboratorios l ON a.id_lab = l.id_Lab
            WHERE u.Usuario = ?
        """
        return self.db.ejecutar_consulta(query, (nombre_docente,)) or []

    def obtener_lista_grupos(self, nombre_docente):
        horarios = self.obtener_horario_docente(nombre_docente)
        grupos = list(set(c.get('Grupo') for c in horarios if c.get('Grupo')))
        return sorted(grupos)

    def obtener_lista_laboratorios(self, nombre_docente):
        horarios = self.obtener_horario_docente(nombre_docente)
        labs = list(set(c.get('Nombre_lab') for c in horarios if c.get('Nombre_lab')))
        return sorted(labs)