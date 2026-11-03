import pdfplumber
import re

class ControladorPDF:
    def procesar_archivo(self, ruta_pdf):
        clases_extraidas = []
        dias_semana = ["LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES"]
        
        try:
            with pdfplumber.open(ruta_pdf) as pdf:
                for pagina in pdf.pages:
                    texto_pagina = pagina.extract_text() or ""
                    
                    match_grupo = re.search(r'\b([1-8]ISC\d{2})\b', texto_pagina)
                    if not match_grupo:
                        continue
                    grupo_actual = match_grupo.group(1)

                    docentes_por_materia = {}
                    tablas = pagina.extract_tables()

                    if tablas:
                        for tabla in tablas:
                            for fila in tabla:
                                fila_limpia = [str(cell).strip().replace('\n', ' ') for cell in fila if cell]
                                if len(fila_limpia) >= 2:
                                    mat_candidata = fila_limpia[0].upper()
                                    doc_candidato = fila_limpia[1].upper()
                                    if len(doc_candidato) > 3 and "@" not in doc_candidato and "CORREO" not in doc_candidato:
                                        docentes_por_materia[mat_candidata] = doc_candidato

                    tablas_visuales = pagina.find_tables()
                    if not tablas_visuales:
                        continue
                        
                    tabla_principal = None
                    for tv in tablas_visuales:
                        celdas = tv.extract()
                        for fila in celdas:
                            if fila and fila[0] and re.search(r'\d{2}:\d{2}', str(fila[0])):
                                tabla_principal = tv
                                break
                        if tabla_principal:
                            break

                    if not tabla_principal:
                        continue

                    filas_tabla = tabla_principal.extract()
                    for fila in filas_tabla:
                        if not fila or not fila[0]:
                            continue
                            
                        hora_texto = str(fila[0]).strip().replace('\n', '').replace(' ', '')
                        match_hora = re.search(r'(\d{2}:\d{2})-(\d{2}:\d{2})', hora_texto)
                        
                        if not match_hora:
                            continue
                            
                        hora_inicio = match_hora.group(1)
                        hora_final = match_hora.group(2)
                        
                        for i in range(1, min(6, len(fila))):
                            celda = fila[i]
                            if celda:
                                texto_celda = str(celda).replace('\n', ' ').strip().upper()
                                
                                if texto_celda and "LUNES" not in texto_celda and "CAMBIO" not in texto_celda:
                                    
                                    materia_encontrada = ""
                                    docente_encontrado = ""
                                    
                                    for mat, doc in docentes_por_materia.items():
                                        if mat in texto_celda or texto_celda in mat:
                                            materia_encontrada = mat
                                            docente_encontrado = doc
                                            break
                                            
                                    if not materia_encontrada:
                                        materia_encontrada = texto_celda
                                        partes = texto_celda.split('  ')
                                        if len(partes) > 1:
                                            materia_encontrada = partes[0].strip()
                                            docente_encontrado = partes[1].strip()
                                            
                                    clases_extraidas.append({
                                        'grupo': grupo_actual,
                                        'dia': dias_semana[i-1],
                                        'hora_inicio': hora_inicio,
                                        'hora_final': hora_final,
                                        'materia': materia_encontrada,
                                        'docente': docente_encontrado,
                                        'texto_celda': texto_celda
                                    })
                                    
            if len(clases_extraidas) > 0:
                return {'exito': True, 'datos': clases_extraidas}
            else:
                return {'exito': False, 'mensaje': 'No se encontraron horarios válidos en la estructura del PDF.'}
                
        except Exception as e:
            return {'exito': False, 'mensaje': f'Error al leer PDF: {str(e)}'}