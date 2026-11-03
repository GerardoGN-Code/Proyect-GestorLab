import unicodedata
from Base_de_datos.conexion import ConexionDB

class ControladorAsignaciones:
    def __init__(self):
        self.db = ConexionDB()

    def _normalizar(self, texto):
        if not texto:
            return ""
        nfkd_form = unicodedata.normalize('NFKD', str(texto))
        return "".join([c for c in nfkd_form if not unicodedata.combining(c)]).upper().strip()

    def procesar_y_guardar_horarios(self, lista_clases_pdf):
        self.db.ejecutar_modificacion("DELETE FROM asignaciones")
        
        total_guardadas = 0
        conteo_horas_lab = {} 

        reticula = self.db.ejecutar_consulta("SELECT * FROM reticula_isc")
        docentes = self.db.ejecutar_consulta("SELECT Matricula, Usuario FROM Usuarios WHERE rol = 'Docente'")
        
        print(f"--- [DEBUG] Total clases leídas del PDF: {len(lista_clases_pdf)}")

        if not reticula or not docentes:
            print("--- [ERROR] La retícula o los docentes están vacíos en la BD.")
            return 0

        for clase in lista_clases_pdf:
            mat_pdf = self._normalizar(clase.get('materia', ''))
            doc_pdf = self._normalizar(clase.get('docente', ''))
            
            materia_encontrada = None
            for mat in reticula:
                nombre_mat_norm = self._normalizar(mat['Materia'])
                if nombre_mat_norm and (nombre_mat_norm in mat_pdf or mat_pdf in nombre_mat_norm):
                    materia_encontrada = mat
                    break
            
            if not materia_encontrada:
                continue
                
            horas_lab_requeridas = int(materia_encontrada['Hora_Lab'] or 0)
            if horas_lab_requeridas == 0:
                continue 

            docente_matricula = None
            for doc in docentes:
                nombre_doc_norm = self._normalizar(doc['Usuario'])
                if doc_pdf and (doc_pdf in nombre_doc_norm or nombre_doc_norm in doc_pdf):
                    docente_matricula = doc['Matricula']
                    break
            
            if not docente_matricula and doc_pdf:
                for doc in docentes:
                    partes = self._normalizar(doc['Usuario']).split()
                    if any(p in doc_pdf for p in partes if len(p) > 3):
                        docente_matricula = doc['Matricula']
                        break

            if not docente_matricula:
                continue

            clave_grupo_materia = f"{clase['grupo']}_{materia_encontrada['Clave_Materia']}"
            if clave_grupo_materia not in conteo_horas_lab:
                conteo_horas_lab[clave_grupo_materia] = 0
                
            if conteo_horas_lab[clave_grupo_materia] >= horas_lab_requeridas:
                continue

            id_lab_asignado = self._buscar_laboratorio_disponible(
                materia_encontrada['software_requerido'],
                clase['dia'],
                clase['hora_inicio'],
                clase['hora_final']
            )

            if id_lab_asignado:
                sql_insert = """
                    INSERT INTO asignaciones 
                    (Matricula_docente, Clave_materia, Grupo, id_lab, Dia_semana, Hora_inicio, Hora_final)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """
                exito = self.db.ejecutar_modificacion(sql_insert, (
                    docente_matricula, 
                    materia_encontrada['Clave_Materia'], 
                    clase['grupo'], 
                    id_lab_asignado, 
                    clase['dia'], 
                    clase['hora_inicio'], 
                    clase['hora_final']
                ))
                
                if exito:
                    total_guardadas += 1
                    conteo_horas_lab[clave_grupo_materia] += 1
                    print(f"--- [ÉXITO] Asignado: {materia_encontrada['Materia']} ({conteo_horas_lab[clave_grupo_materia]}/{horas_lab_requeridas}) | Grupo: {clase['grupo']} | {clase['dia']} {clase['hora_inicio']}-{clase['hora_final']}")

        print(f"--- [FIN] Total de clases guardadas en BD: {total_guardadas}")
        return total_guardadas

    def _buscar_laboratorio_disponible(self, software_req, dia, h_inicio, h_fin):
        query_ideal = """
            SELECT id_Lab FROM laboratorios 
            WHERE Estado = 'Disponible' AND Software_instalado LIKE ?
            AND id_Lab NOT IN (
                SELECT id_lab FROM asignaciones 
                WHERE Dia_semana = ? AND (
                    (Hora_inicio <= ? AND Hora_final > ?) OR
                    (Hora_inicio < ? AND Hora_final >= ?) OR
                    (Hora_inicio >= ? AND Hora_final <= ?)
                )
            )
        """
        param_software = f"%{software_req}%" if software_req else "%%"
        labs_ideales = self.db.ejecutar_consulta(query_ideal, (param_software, dia, h_inicio, h_inicio, h_fin, h_fin, h_inicio, h_fin))
        if labs_ideales:
            return labs_ideales[0]['id_Lab']

        query_secundaria = """
            SELECT id_Lab FROM laboratorios 
            WHERE Estado = 'Disponible'
            AND id_Lab NOT IN (
                SELECT id_lab FROM asignaciones 
                WHERE Dia_semana = ? AND (
                    (Hora_inicio <= ? AND Hora_final > ?) OR
                    (Hora_inicio < ? AND Hora_final >= ?) OR
                    (Hora_inicio >= ? AND Hora_final <= ?)
                )
            )
        """
        labs_secundarios = self.db.ejecutar_consulta(query_secundaria, (dia, h_inicio, h_inicio, h_fin, h_fin, h_inicio, h_fin))
        if labs_secundarios:
            return labs_secundarios[0]['id_Lab']
            
        return None