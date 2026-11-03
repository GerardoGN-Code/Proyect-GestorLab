import customtkinter as ctk
import os
import sys

ruta_proyecto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ruta_proyecto)

from Logica.controlador_admin import ControladorAdmin

COLOR_VERDE_OSCURO = "#045b4a"
COLOR_VERDE_CLARO = "#036f56"
COLOR_GRIS_FONDO = "#e5e5e5"
COLOR_TEXTO_GRIS = "#7f7f7f"

class VistaAdmin(ctk.CTkFrame):
    def __init__(self, master, nombre_usuario, al_cerrar_sesion):
        super().__init__(master, fg_color=COLOR_GRIS_FONDO, corner_radius=0)
        
        self.nombre_usuario = nombre_usuario
        self.al_cerrar_sesion = al_cerrar_sesion
        self.controlador = ControladorAdmin()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=8)

        self._crear_sidebar()
        
        self.contenido_principal = ctk.CTkFrame(self, fg_color="transparent")
        self.contenido_principal.grid(row=0, column=1, sticky="nsew")
        self.contenido_principal.grid_rowconfigure(1, weight=1)
        self.contenido_principal.grid_columnconfigure(0, weight=1)

        self.mostrar_panel_horarios()

    def _crear_sidebar(self):
        sidebar = ctk.CTkFrame(self, fg_color=COLOR_VERDE_OSCURO, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")

        logo_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        logo_frame.pack(pady=(40, 60), padx=20, fill="x")
        ctk.CTkLabel(logo_frame, text="GestorLab", font=ctk.CTkFont("Arial", 22, "bold"), text_color="white").pack(anchor="w")
        ctk.CTkLabel(logo_frame, text="TESCHI", font=ctk.CTkFont("Arial", 12), text_color="#a0c4b9").pack(anchor="w")

        self.btn_horarios = ctk.CTkButton(sidebar, text="Horarios", font=ctk.CTkFont("Arial", 16, "bold"), fg_color="transparent", hover_color=COLOR_VERDE_CLARO, anchor="w", command=self.mostrar_panel_horarios)
        self.btn_horarios.pack(fill="x", padx=20, pady=10)

        self.btn_docentes = ctk.CTkButton(sidebar, text="Docentes", font=ctk.CTkFont("Arial", 16, "bold"), fg_color="transparent", hover_color=COLOR_VERDE_CLARO, anchor="w", command=self.mostrar_panel_docentes)
        self.btn_docentes.pack(fill="x", padx=20, pady=10)

        self.btn_laboratorios = ctk.CTkButton(sidebar, text="Laboratorios", font=ctk.CTkFont("Arial", 16, "bold"), fg_color="transparent", hover_color=COLOR_VERDE_CLARO, anchor="w", command=self.mostrar_panel_laboratorios)
        self.btn_laboratorios.pack(fill="x", padx=20, pady=10)

        btn_cerrar = ctk.CTkButton(sidebar, text="cerrar sesión ➔", fg_color="#e63946", hover_color="#c1121f", font=ctk.CTkFont("Arial", 12, "bold"), command=self.al_cerrar_sesion)
        btn_cerrar.pack(side="bottom", pady=40, padx=20, fill="x")

    def _actualizar_botones_sidebar(self, boton_activo):
        for btn in [self.btn_horarios, self.btn_docentes, self.btn_laboratorios]:
            btn.configure(fg_color="transparent", text_color="white")
        boton_activo.configure(fg_color="white", text_color="black")

    def _crear_header_contenido(self, titulo_seccion):
        for widget in self.contenido_principal.winfo_children():
            widget.destroy()

        header = ctk.CTkFrame(self.contenido_principal, fg_color="white", height=100, corner_radius=0)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)
        header.grid_columnconfigure(0, weight=1)
        header.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(header, text=titulo_seccion, font=ctk.CTkFont("Arial", 24, "bold"), text_color="black").grid(row=0, column=0, sticky="w", padx=40)

        perfil_frame = ctk.CTkFrame(header, fg_color="transparent")
        perfil_frame.grid(row=0, column=1, sticky="e", padx=40)
        ctk.CTkLabel(perfil_frame, text=self.nombre_usuario, font=ctk.CTkFont("Arial", 14, "bold"), text_color="black").pack(anchor="e")
        ctk.CTkLabel(perfil_frame, text="Administrador", font=ctk.CTkFont("Arial", 12), text_color=COLOR_TEXTO_GRIS).pack(anchor="e")

        self.vista_dinamica = ctk.CTkFrame(self.contenido_principal, fg_color="transparent")
        self.vista_dinamica.grid(row=1, column=0, sticky="nsew", padx=40, pady=30)
        self.vista_dinamica.grid_columnconfigure(0, weight=1)

    def mostrar_panel_horarios(self):
        self._actualizar_botones_sidebar(self.btn_horarios)
        self._crear_header_contenido("Gestión de horarios")

        for widget in self.vista_dinamica.winfo_children():
            widget.destroy()

        main_container = ctk.CTkFrame(self.vista_dinamica, fg_color="white", corner_radius=15, border_width=1, border_color="#d1d5db")
        main_container.pack(fill="both", expand=True, padx=10, pady=10)

        header_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        header_frame.pack(fill="x", padx=25, pady=(25, 15))
        
        ctk.CTkLabel(header_frame, text="Horarios de laboratorio", font=ctk.CTkFont("Arial", 22, "bold"), text_color="black").pack(side="left")
        
        btn_exportar = ctk.CTkButton(header_frame, text="⭳ Exportar PDF", fg_color="white", text_color="black", border_color="#d1d5db", border_width=1, hover_color="#f3f4f6", font=ctk.CTkFont("Arial", 12, "bold"), command=self.exportar_pdf_horario)
        btn_exportar.pack(side="right")

        filtros_frame = ctk.CTkFrame(main_container, fg_color="#e5e5e5", corner_radius=0, height=75)
        filtros_frame.pack(fill="x")
        filtros_frame.pack_propagate(False)

        inner_filtros = ctk.CTkFrame(filtros_frame, fg_color="transparent")
        inner_filtros.pack(fill="both", expand=True, padx=25, pady=10)

        busqueda_frame = ctk.CTkFrame(inner_filtros, fg_color="transparent")
        busqueda_frame.pack(side="left", padx=(0, 15))
        ctk.CTkLabel(busqueda_frame, text="Búsqueda por materia o docente", font=ctk.CTkFont("Arial", 10), text_color="#7f7f7f").pack(anchor="w")
        self.entrada_busqueda_horario = ctk.CTkEntry(busqueda_frame, placeholder_text="🔍 Escribe aquí...", width=220, fg_color="white", text_color="black")
        self.entrada_busqueda_horario.pack()
        self.entrada_busqueda_horario.bind("<KeyRelease>", self.filtrar_horarios)

        g_frame = ctk.CTkFrame(inner_filtros, fg_color="transparent")
        g_frame.pack(side="left", padx=10)
        ctk.CTkLabel(g_frame, text="Grupos", font=ctk.CTkFont("Arial", 10), text_color="#7f7f7f").pack(anchor="w")
        grupos = ["Todos"] + self.controlador.obtener_lista_grupos()
        self.cb_grupos = ctk.CTkComboBox(g_frame, values=grupos, width=120, fg_color="white", text_color="black", command=self.filtrar_horarios)
        self.cb_grupos.pack()
        
        t_frame = ctk.CTkFrame(inner_filtros, fg_color="transparent")
        t_frame.pack(side="left", padx=10)
        ctk.CTkLabel(t_frame, text="Turno", font=ctk.CTkFont("Arial", 10), text_color="#7f7f7f").pack(anchor="w")
        self.cb_turno = ctk.CTkComboBox(t_frame, values=["Todos", "Matutino", "Vespertino"], width=120, fg_color="white", text_color="black", command=self.filtrar_horarios)
        self.cb_turno.pack()
        
        l_frame = ctk.CTkFrame(inner_filtros, fg_color="transparent")
        l_frame.pack(side="left", padx=10)
        ctk.CTkLabel(l_frame, text="Laboratorios", font=ctk.CTkFont("Arial", 10), text_color="#7f7f7f").pack(anchor="w")
        
        labs = self.controlador.obtener_lista_laboratorios()
        if not labs: 
            labs = ["Sin laboratorios"]
            
        self.cb_labs = ctk.CTkComboBox(l_frame, values=labs, width=200, fg_color="white", text_color="black", command=self.filtrar_horarios)
        self.cb_labs.pack()
        self.cb_labs.set(labs[0])

        scroll_grid = ctk.CTkScrollableFrame(main_container, fg_color="transparent")
        scroll_grid.pack(fill="both", expand=True, padx=25, pady=20)
        self.tabla_frame = ctk.CTkFrame(scroll_grid, fg_color="#d1d5db", corner_radius=0)
        self.tabla_frame.pack(fill="both", expand=True)
        self.tabla_frame.grid_columnconfigure(0, weight=0, minsize=100) 
        for i in range(1, 6):
            self.tabla_frame.grid_columnconfigure(i, weight=1)
        self.dias = ["LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES"]
        self.horas_rango = [f"{str(h).zfill(2)}:00" for h in range(7, 22)] 

        self.filtrar_horarios() 

    def filtrar_horarios(self, *args):
        for widget in self.tabla_frame.winfo_children():
            widget.destroy()
        
        self._dibujar_estructura_tabla()
        
        grupo_f = self.cb_grupos.get()
        turno_f = self.cb_turno.get()
        lab_f = self.cb_labs.get()
        busqueda = self.entrada_busqueda_horario.get().lower()

        horarios = self.controlador.obtener_horarios_completos() or []
        horarios_filtrados = []

        for c in horarios:
            match_g = (grupo_f == "Todos" or str(c.get('Grupo')) == grupo_f)
            match_l = (str(c.get('Nombre_lab')) == lab_f)
            
            h_inicio = int(str(c.get('Hora_inicio', '00:00'))[:2]) if c.get('Hora_inicio') else 0
            if turno_f == "Matutino": match_t = h_inicio < 14
            elif turno_f == "Vespertino": match_t = h_inicio >= 14
            else: match_t = True
                
            match_b = (busqueda in str(c.get('Nombre_materia','')).lower() or busqueda in str(c.get('Nombre_docente','')).lower())
            
            if match_g and match_l and match_t and match_b:
                horarios_filtrados.append(c)

        self.horarios_actuales = horarios_filtrados 
        self._poblar_datos_horario(horarios_filtrados)

        self._poblar_datos_horario(horarios_filtrados)

    def _dibujar_estructura_tabla(self):
        reloj_frame = ctk.CTkFrame(self.tabla_frame, fg_color="#045b4a", corner_radius=0, height=35)
        reloj_frame.grid(row=0, column=0, sticky="nsew", padx=(0,1), pady=(0,1))
        reloj_frame.grid_propagate(False)
        ctk.CTkLabel(reloj_frame, text="🕒", font=("Arial", 16), text_color="white").pack(expand=True)

        for i, dia in enumerate(self.dias):
            dia_frame = ctk.CTkFrame(self.tabla_frame, fg_color="#045b4a", corner_radius=0, height=35)
            dia_frame.grid(row=0, column=i+1, sticky="nsew", padx=(0,1) if i<4 else 0, pady=(0,1))
            dia_frame.grid_propagate(False)
            ctk.CTkLabel(dia_frame, text=dia, font=ctk.CTkFont("Arial", 11, "bold"), text_color="white").pack(expand=True)

        for row_idx in range(len(self.horas_rango) - 1):
            hora_inicio = self.horas_rango[row_idx]
            hora_fin = self.horas_rango[row_idx + 1]
            texto_hora = f"{hora_inicio} - {hora_fin}"

            hora_frame = ctk.CTkFrame(self.tabla_frame, fg_color="#e5e7eb", corner_radius=0, height=35)
            hora_frame.grid(row=row_idx+1, column=0, sticky="nsew", padx=(0,1), pady=(0,1))
            hora_frame.grid_propagate(False)
            ctk.CTkLabel(hora_frame, text=texto_hora, font=ctk.CTkFont("Arial", 10, "bold"), text_color="black").pack(expand=True)

            for col_idx in range(1, 6):
                celda = ctk.CTkFrame(self.tabla_frame, fg_color="white", corner_radius=0, height=35)
                celda.grid(row=row_idx+1, column=col_idx, sticky="nsew", padx=(0,1) if col_idx<5 else 0, pady=(0,1))
                celda.grid_propagate(False)

    def _poblar_datos_horario(self, horarios_lista):
        colores_pastel = [
            {"bg": "#fce4d6", "border": "#d98d75"}, {"bg": "#e1f5fe", "border": "#4fc3f7"}, 
            {"bg": "#f3e8ff", "border": "#c084fc"}, {"bg": "#fef9c3", "border": "#facc15"}, 
            {"bg": "#dcfce7", "border": "#4ade80"}
        ]
        color_index = 0
        materias_colores = {}

        for clase in horarios_lista:
            try:
                dia_str = str(clase.get('Dia_semana', '')).upper()
                if dia_str not in self.dias: continue
                col_idx = self.dias.index(dia_str) + 1

                h_inicio = str(clase.get('Hora_inicio', ''))[:5]
                h_fin = str(clase.get('Hora_final', ''))[:5]
                
                if h_inicio not in self.horas_rango or h_fin not in self.horas_rango: continue
                    
                row_start = self.horas_rango.index(h_inicio) + 1
                row_end = self.horas_rango.index(h_fin) + 1
                row_span = row_end - row_start

                if row_span < 1: continue

                materia = clase.get('Nombre_materia') or 'Materia Sin Asignar'
                if materia not in materias_colores:
                    materias_colores[materia] = colores_pastel[color_index % len(colores_pastel)]
                    color_index += 1
                tema = materias_colores[materia]

                grupo = str(clase.get('Grupo') or 'S/G')
                docente = str(clase.get('Nombre_docente') or 'Sin Docente')
                lab = str(clase.get('Nombre_lab') or 'Lab no asignado')

                self._dibujar_bloque_clase(row_start, col_idx, row_span, grupo, materia, docente, lab, tema)
            except Exception as e:
                pass

    def _dibujar_bloque_clase(self, fila, columna, rowspan, grupo, materia, docente, lab, tema):
        import textwrap
        bloque = ctk.CTkFrame(self.tabla_frame, fg_color=tema["bg"], corner_radius=0)
        bloque.grid(row=fila, column=columna, rowspan=rowspan, sticky="nsew", padx=2, pady=2)
        bloque.grid_propagate(False)

        ctk.CTkFrame(bloque, fg_color=tema["border"], width=4, corner_radius=0).pack(side="left", fill="y")

        text_frame = ctk.CTkFrame(bloque, fg_color="transparent")
        text_frame.pack(side="left", fill="both", expand=True, padx=8, pady=5)
        
        mat_wrap = textwrap.fill(materia, width=25)
        doc_wrap = textwrap.fill(docente, width=30)
        lab_wrap = textwrap.fill(lab, width=25)
        
        ctk.CTkLabel(text_frame, text=grupo, font=ctk.CTkFont("Arial", 10, "bold"), text_color="#4b5563").pack(anchor="w")
        ctk.CTkLabel(text_frame, text=mat_wrap, font=ctk.CTkFont("Arial", 12, "bold"), text_color="black", justify="left").pack(anchor="w", pady=(2, 0))
        ctk.CTkLabel(text_frame, text=doc_wrap, font=ctk.CTkFont("Arial", 9, "bold"), text_color="black", justify="left").pack(anchor="w")
        
        ctk.CTkLabel(text_frame, text=lab_wrap, font=ctk.CTkFont("Arial", 9), text_color=COLOR_TEXTO_GRIS, justify="left").pack(anchor="w", pady=(2, 0))

    def exportar_pdf_horario(self):
        try:
            from fpdf import FPDF
        except ImportError:
            from tkinter import messagebox
            messagebox.showerror("Librería faltante", "Falta la librería FPDF.\nAbre tu terminal y ejecuta:\npip install fpdf")
            return

        horarios = getattr(self, 'horarios_actuales', [])
        
        pdf = FPDF(orientation='L', unit='mm', format='A4')
        pdf.set_auto_page_break(auto=False)
        pdf.add_page()
        
        pdf.set_font("Arial", 'B', 15)
        pdf.set_text_color(4, 91, 74)
        lab_seleccionado = self.cb_labs.get()
        pdf.cell(0, 8, f"Horarios de Laboratorio - {lab_seleccionado}", ln=True, align='C')
        pdf.ln(2)
        
        x_start = 13
        y_start = pdf.get_y()
        col_w_hora = 24
        col_w_dia = 49
        row_h = 7.5 
        
        dias = ["LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES"]
        horas = [f"{str(h).zfill(2)}:00" for h in range(7, 22)]
        
        pdf.set_font("Arial", 'B', 9)
        pdf.set_fill_color(4, 91, 74) 
        pdf.set_text_color(255, 255, 255)
        pdf.set_draw_color(210, 210, 210)
        
        pdf.set_xy(x_start, y_start)
        pdf.cell(col_w_hora, 7, "HORARIOS", border=1, align='C', fill=True)
        for i, dia in enumerate(dias):
            pdf.set_xy(x_start + col_w_hora + (i * col_w_dia), y_start)
            pdf.cell(col_w_dia, 7, dia, border=1, align='C', fill=True)
            
        y_start += 7
        
        pdf.set_font("Arial", 'B', 7.5)
        pdf.set_text_color(60, 60, 60)
        pdf.set_fill_color(245, 247, 248)
        
        for row_idx in range(len(horas) - 1):
            y_pos = y_start + (row_idx * row_h)
            pdf.set_xy(x_start, y_pos)
            pdf.cell(col_w_hora, row_h, f"{horas[row_idx]} - {horas[row_idx+1]}", border=1, align='C', fill=True)
            for col_idx in range(5):
                pdf.set_xy(x_start + col_w_hora + (col_idx * col_w_dia), y_pos)
                pdf.cell(col_w_dia, row_h, "", border=1)

        colores = [
            {"bg": (252, 228, 214), "border": (217, 141, 117)}, 
            {"bg": (225, 245, 254), "border": (79, 195, 247)},  
            {"bg": (243, 232, 255), "border": (192, 132, 252)}, 
            {"bg": (254, 249, 195), "border": (250, 204, 21)},  
            {"bg": (220, 252, 231), "border": (74, 222, 128)}
        ]
        materias_colores = {}
        idx_color = 0

        for clase in horarios:
            dia_str = str(clase.get('Dia_semana', '')).upper().replace('É', 'E')
            if dia_str not in dias: continue
            col_idx = dias.index(dia_str)
            
            h_in = str(clase.get('Hora_inicio', ''))[:5]
            h_fin = str(clase.get('Hora_final', ''))[:5]
            if h_in not in horas or h_fin not in horas: continue
            
            row_start = horas.index(h_in)
            span = horas.index(h_fin) - row_start
            if span < 1: continue
            
            mat = str(clase.get('Nombre_materia') or 'S/M')
            if mat not in materias_colores:
                materias_colores[mat] = colores[idx_color % len(colores)]
                idx_color += 1
            tema = materias_colores[mat]
            
            bx = x_start + col_w_hora + (col_idx * col_w_dia)
            by = y_start + (row_start * row_h)
            bw = col_w_dia
            bh = span * row_h
            
            pdf.set_fill_color(*tema["bg"])
            pdf.rect(bx, by, bw, bh, style='F')
            pdf.set_fill_color(*tema["border"])
            pdf.rect(bx, by, 2.5, bh, style='F')
            pdf.set_draw_color(200, 200, 200)
            pdf.rect(bx, by, bw, bh, style='D')
            
            grup = str(clase.get('Grupo', ''))
            docente = str(clase.get('Nombre_docente', ''))
            lab = str(clase.get('Nombre_lab', ''))
            
            mx = bx + 3.5
            w_util = bw - 4.5

            if span == 1:
                pdf.set_font("Arial", 'B', 6)
                pdf.set_text_color(0, 0, 0)
                txt_head = f"{grup} | {mat}"
                pdf.set_xy(mx, by + 0.8)
                pdf.cell(w_util, 2.3, txt_head[:34], align='L')
                
                pdf.set_font("Arial", '', 5.5)
                pdf.set_text_color(70, 70, 70)
                pdf.set_xy(mx, by + 3.0)
                pdf.cell(w_util, 2.0, docente[:34], align='L')
                
                pdf.set_font("Arial", '', 5)
                pdf.set_text_color(120, 120, 120)
                pdf.set_xy(mx, by + 5.0)
                pdf.cell(w_util, 2.0, lab[:36], align='L')
            else:
                pdf.set_font("Arial", 'B', 6)
                pdf.set_text_color(80, 80, 80)
                pdf.set_xy(mx, by + 1.2)
                pdf.cell(w_util, 2.5, grup, align='L')
                
                pdf.set_font("Arial", 'B', 6.5)
                pdf.set_text_color(0, 0, 0)
                pdf.set_xy(mx, by + 3.8)
                pdf.cell(w_util, 2.8, mat[:32], align='L')
                
                pdf.set_font("Arial", '', 5.5)
                pdf.set_text_color(70, 70, 70)
                pdf.set_xy(mx, by + 6.8)
                pdf.cell(w_util, 2.5, docente[:32], align='L')
                
                pdf.set_font("Arial", '', 5)
                pdf.set_text_color(120, 120, 120)
                pdf.set_xy(mx, by + bh - 3.2)
                pdf.cell(w_util, 2.2, lab[:36], align='L')

        from tkinter import filedialog, messagebox
        ruta_guardar = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("Archivos PDF", "*.pdf")], initialfile="Horarios_Filtrados_GestorLab.pdf")
        if ruta_guardar:
            try:
                pdf.output(ruta_guardar)
                messagebox.showinfo("Éxito", f"PDF exportado perfectamente en 1 página:\n{ruta_guardar}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el PDF:\n{e}")

    def mostrar_panel_docentes(self):
        self._actualizar_botones_sidebar(self.btn_docentes)
        self._crear_header_contenido("Gestión de docentes")

        for widget in self.vista_dinamica.winfo_children():
            widget.destroy()

        banner = ctk.CTkFrame(self.vista_dinamica, fg_color="#539b85", corner_radius=10, height=80)
        banner.pack(fill="x", pady=(0, 15))
        banner.pack_propagate(False)
        
        info_banner = ctk.CTkFrame(banner, fg_color="transparent")
        info_banner.pack(side="left", padx=20, fill="y", pady=15)
        
        ctk.CTkLabel(info_banner, text="Gestión de docentes", font=ctk.CTkFont("Arial", 18, "bold"), text_color="white").pack(anchor="w")
        ctk.CTkLabel(info_banner, text="Administra los perfiles y asignaciones del personal docente", font=ctk.CTkFont("Arial", 12), text_color="#d1e5df").pack(anchor="w")

        btn_agregar = ctk.CTkButton(banner, text="Agregar Docente", fg_color="#045b4a", hover_color="#03483a", font=ctk.CTkFont("Arial", 13, "bold"), command=lambda: self.abrir_modal_docente())
        btn_agregar.pack(side="right", padx=20)

        search_frame = ctk.CTkFrame(self.vista_dinamica, fg_color="white", corner_radius=10, height=50)
        search_frame.pack(fill="x", pady=(0, 20))
        search_frame.pack_propagate(False)

        self.entrada_busqueda = ctk.CTkEntry(search_frame, placeholder_text="Buscar por nombre o matrícula...", width=300, fg_color="#f9f9f9", border_width=1, border_color="#e5e5e5", text_color="black")
        self.entrada_busqueda.pack(side="left", padx=20, pady=10)
        self.entrada_busqueda.bind("<KeyRelease>", self.filtrar_docentes)

        self.lbl_contador_docentes = ctk.CTkLabel(search_frame, text="0 docentes", font=ctk.CTkFont("Arial", 12, "bold"), text_color=COLOR_TEXTO_GRIS)
        self.lbl_contador_docentes.pack(side="right", padx=20)

        self.scroll_docentes = ctk.CTkScrollableFrame(self.vista_dinamica, fg_color="transparent")
        self.scroll_docentes.pack(fill="both", expand=True)
        self.scroll_docentes.grid_columnconfigure((0, 1, 2), weight=1)

        self.cargar_tarjetas_docentes()

    def filtrar_docentes(self, event=None):
        termino = self.entrada_busqueda.get()
        self.cargar_tarjetas_docentes(termino)

    def cargar_tarjetas_docentes(self, filtro=""):
        for widget in self.scroll_docentes.winfo_children():
            widget.destroy()

        docentes_db = self.controlador.obtener_todos_los_docentes() or []
        
        if filtro:
            filtro = filtro.lower()
            docentes_db = [d for d in docentes_db if filtro in str(d.get('Usuario', '')).lower() or filtro in str(d.get('Matricula', '')).lower()]

        self.lbl_contador_docentes.configure(text=f"{len(docentes_db)} docentes encontrados")

        if docentes_db:
            for indice, docente in enumerate(docentes_db):
                fila = indice // 3
                columna = indice % 3
                self._dibujar_tarjeta_docente(self.scroll_docentes, fila, columna, docente)
        else:
            ctk.CTkLabel(self.scroll_docentes, text="No se encontraron docentes.", font=ctk.CTkFont("Arial", 16), text_color="black").grid(row=0, column=0, pady=50)

    def _dibujar_tarjeta_docente(self, padre, fila, columna, docente):
        import textwrap 

        tarjeta = ctk.CTkFrame(padre, fg_color="white", corner_radius=10)
        tarjeta.grid(row=fila, column=columna, padx=15, pady=15, sticky="nsew")
        
        raw_estado = docente.get('Estado') or docente.get('estado') or 'Activo'
        estado_actual = str(raw_estado).strip().capitalize()
        
        if estado_actual == 'Activo':
            color_fondo_estado = "#dcfce7"
            color_texto_estado = "#166534"
            texto_etiqueta = "Activo"
            texto_boton_accion = "Desactivar"
            color_hover_boton = "#fee2e2"
        else:
            color_fondo_estado = "#f3f4f6"
            color_texto_estado = "#4b5563"
            texto_etiqueta = "Inactivo"
            texto_boton_accion = "Activar"
            color_hover_boton = "#dcfce7"

        lbl_estado = ctk.CTkLabel(tarjeta, text=texto_etiqueta, font=ctk.CTkFont("Arial", 10, "bold"), fg_color=color_fondo_estado, text_color=color_texto_estado, corner_radius=5)
        lbl_estado.pack(anchor="e", padx=10, pady=10)
        
        nombre_docente = docente.get('Usuario') or docente.get('usuario') or 'Sin Nombre'
        matricula_docente = docente.get('Matricula') or docente.get('matricula') or ''
        
        nombre_formateado = textwrap.fill(nombre_docente, width=22)
        
        ctk.CTkLabel(tarjeta, text=nombre_formateado, font=ctk.CTkFont("Arial", 14, "bold"), text_color="black", justify="left").pack(anchor="w", padx=15)
        ctk.CTkLabel(tarjeta, text=matricula_docente, font=ctk.CTkFont("Arial", 11), text_color=COLOR_TEXTO_GRIS).pack(anchor="w", padx=15, pady=(0, 10))
        
        div = ctk.CTkFrame(tarjeta, fg_color="#e5e5e5", height=2)
        div.pack(fill="x", padx=15, pady=5)
        
        ctk.CTkLabel(tarjeta, text="📋 Docente ISC", font=ctk.CTkFont("Arial", 11), text_color="#4b5563").pack(anchor="w", padx=15, pady=(5,0))
        
        btn_frame = ctk.CTkFrame(tarjeta, fg_color="transparent")
        btn_frame.pack(fill="x", padx=15, pady=15)
        
        btn_editar = ctk.CTkButton(btn_frame, text="✎ Editar", width=70, height=24, fg_color="#f3f4f6", text_color="black", hover_color="#e5e7eb", font=ctk.CTkFont("Arial", 11, "bold"), command=lambda d=docente: self.abrir_modal_docente(d))
        btn_editar.pack(side="left")
        
        id_usuario = docente.get('id_usuario') or docente.get('ID_USUARIO')
        btn_estado = ctk.CTkButton(
            btn_frame, 
            text=texto_boton_accion, 
            width=70, 
            height=24, 
            fg_color="transparent", 
            text_color=COLOR_TEXTO_GRIS, 
            hover_color=color_hover_boton, 
            font=ctk.CTkFont("Arial", 11, "bold"), 
            command=lambda u_id=id_usuario, e=estado_actual: self.cambiar_estado_docente(u_id, e)
        )
        btn_estado.pack(side="right")

    def cambiar_estado_docente(self, id_usuario, estado_actual):
        nuevo_estado = "Inactivo" if estado_actual == "Activo" else "Activo"
        resultado = self.controlador.cambiar_estado_docente(id_usuario, nuevo_estado)
        if resultado['exito']:
            self.cargar_tarjetas_docentes(self.entrada_busqueda.get())
        else:
            from tkinter import messagebox
            messagebox.showerror("Error", resultado['mensaje'])

    def abrir_modal_docente(self, docente=None):
        modal = ctk.CTkToplevel(self)
        titulo_principal = "Editar docente" if docente else "Nuevo docente"
        modal.title(titulo_principal)
        modal.geometry("500x550")
        modal.resizable(False, False)
        modal.configure(fg_color="white")
        modal.transient(self)
        modal.grab_set()

        header_frame = ctk.CTkFrame(modal, fg_color="transparent")
        header_frame.pack(fill="x", padx=30, pady=(30, 15))
        
        ctk.CTkLabel(header_frame, text="A D M I N I S T R A D O R", font=ctk.CTkFont("Arial", 11, "bold"), text_color="#166534").pack(anchor="w")
        
        title_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_container.pack(fill="x", pady=(5, 0))
        
        ctk.CTkLabel(title_container, text=titulo_principal, font=ctk.CTkFont("Arial", 22, "bold"), text_color="black").pack(side="left")
        
        btn_cerrar_modal = ctk.CTkButton(title_container, text="×", width=35, height=35, fg_color="#f3f4f6", text_color="black", hover_color="#e5e7eb", font=ctk.CTkFont("Arial", 18), corner_radius=8, command=modal.destroy)
        btn_cerrar_modal.pack(side="right")

        div = ctk.CTkFrame(modal, fg_color="#e5e5e5", height=1)
        div.pack(fill="x", pady=(0, 25))

        form_frame = ctk.CTkFrame(modal, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=30)

        ctk.CTkLabel(form_frame, text="Nombre completo", font=ctk.CTkFont("Arial", 12, "bold"), text_color="#4b5563").pack(anchor="w")
        ent_nombre = ctk.CTkEntry(form_frame, placeholder_text="Nombre del docente", height=45, fg_color="white", border_color="#d1d5db", border_width=1, text_color="black")
        ent_nombre.pack(fill="x", pady=(5, 20))

        ctk.CTkLabel(form_frame, text="Correo institucional", font=ctk.CTkFont("Arial", 12, "bold"), text_color="#4b5563").pack(anchor="w")
        ent_correo = ctk.CTkEntry(form_frame, placeholder_text="nombre@teschi.edu.mx", height=45, fg_color="white", border_color="#d1d5db", border_width=1, text_color="black")
        ent_correo.pack(fill="x", pady=(5, 20))

        ctk.CTkLabel(form_frame, text="Especialidad", font=ctk.CTkFont("Arial", 12, "bold"), text_color="#4b5563").pack(anchor="w")
        ent_especialidad = ctk.CTkEntry(form_frame, placeholder_text="Ej. Desarrollo de software", height=45, fg_color="white", border_color="#d1d5db", border_width=1, text_color="black")
        ent_especialidad.pack(fill="x", pady=(5, 30))

        botones_frame = ctk.CTkFrame(modal, fg_color="transparent")
        botones_frame.pack(fill="x", padx=30, pady=(0, 30))
        
        texto_btn_accion = "Guardar cambios" if docente else "Agregar docente"
        
        btn_accion = ctk.CTkButton(botones_frame, text=texto_btn_accion, width=150, height=45, font=ctk.CTkFont("Arial", 14, "bold"), fg_color="#045b4a", hover_color="#03483a", corner_radius=8, command=lambda: guardar())
        btn_accion.pack(side="right", padx=(10, 0))

        btn_cancelar = ctk.CTkButton(botones_frame, text="Cancelar", width=110, height=45, font=ctk.CTkFont("Arial", 14, "bold"), fg_color="white", text_color="#4b5563", border_color="#d1d5db", border_width=1, hover_color="#f3f4f6", corner_radius=8, command=modal.destroy)
        btn_cancelar.pack(side="right")

        if docente:
            ent_nombre.insert(0, str(docente.get('Usuario', '')))
            ent_correo.insert(0, str(docente.get('Matricula', '')))

        def guardar():
            nom = ent_nombre.get().strip()
            correo = ent_correo.get().strip()
            pwd = "teschi_docente"

            if not nom or not correo:
                from tkinter import messagebox
                messagebox.showwarning("Campos vacíos", "Por favor llena el nombre y el correo.", parent=modal)
                return

            if docente:
                res = self.controlador.actualizar_docente(docente.get('id_usuario'), correo, nom, pwd)
            else:
                res = self.controlador.agregar_docente(correo, nom, pwd)

            if res['exito']:
                modal.destroy()
                self.cargar_tarjetas_docentes(self.entrada_busqueda.get())
            else:
                from tkinter import messagebox
                messagebox.showerror("Error DB", res['mensaje'], parent=modal)

    def mostrar_panel_laboratorios(self):
        self._actualizar_botones_sidebar(self.btn_laboratorios)
        self._crear_header_contenido("Gestión de laboratorios")

        for widget in self.vista_dinamica.winfo_children():
            widget.destroy()

        banner = ctk.CTkFrame(self.vista_dinamica, fg_color="#539b85", corner_radius=10, height=80)
        banner.pack(fill="x", pady=(0, 15))
        banner.pack_propagate(False)
        
        info_banner = ctk.CTkFrame(banner, fg_color="transparent")
        info_banner.pack(side="left", padx=20, fill="y", pady=15)
        
        ctk.CTkLabel(info_banner, text="Gestión de laboratorios", font=ctk.CTkFont("Arial", 18, "bold"), text_color="white").pack(anchor="w")
        ctk.CTkLabel(info_banner, text="Consulta la disponibilidad y administra los espacios de trabajo", font=ctk.CTkFont("Arial", 12), text_color="#d1e5df").pack(anchor="w")

        btn_agregar = ctk.CTkButton(banner, text="Agregar Laboratorio", fg_color="#045b4a", hover_color="#03483a", font=ctk.CTkFont("Arial", 13, "bold"), command=lambda: self.abrir_modal_laboratorio())
        btn_agregar.pack(side="right", padx=20)

        search_frame = ctk.CTkFrame(self.vista_dinamica, fg_color="white", corner_radius=10, height=50)
        search_frame.pack(fill="x", pady=(0, 20))
        search_frame.pack_propagate(False)

        self.entrada_busqueda_labs = ctk.CTkEntry(search_frame, placeholder_text="Buscar laboratorio o ubicación...", width=300, fg_color="#f9f9f9", border_width=1, border_color="#e5e5e5", text_color="black")
        self.entrada_busqueda_labs.pack(side="left", padx=20, pady=10)
        self.entrada_busqueda_labs.bind("<KeyRelease>", self.filtrar_laboratorios)

        self.lbl_contador_labs = ctk.CTkLabel(search_frame, text="0 espacios disponibles", font=ctk.CTkFont("Arial", 12, "bold"), text_color=COLOR_TEXTO_GRIS)
        self.lbl_contador_labs.pack(side="right", padx=20)

        self.scroll_labs = ctk.CTkScrollableFrame(self.vista_dinamica, fg_color="transparent")
        self.scroll_labs.pack(fill="both", expand=True)
        self.scroll_labs.grid_columnconfigure((0, 1, 2), weight=1)

        self.cargar_tarjetas_laboratorios()

    def filtrar_laboratorios(self, event=None):
        termino = self.entrada_busqueda_labs.get()
        self.cargar_tarjetas_laboratorios(termino)

    def cargar_tarjetas_laboratorios(self, filtro=""):
        for widget in self.scroll_labs.winfo_children():
            widget.destroy()

        labs_db = self.controlador.obtener_laboratorios() or []

        if filtro:
            filtro = filtro.lower()
            labs_db = [
                l for l in labs_db 
                if filtro in str(l.get('Nombre_lab', '')).lower() 
                or filtro in str(l.get('Ubicacion', '') or l.get('Edificio', '')).lower()
            ]

        disponibles = [l for l in labs_db if str(l.get('Estado', '')).strip().capitalize() == 'Disponible']
        self.lbl_contador_labs.configure(text=f"{len(disponibles)} espacios disponibles")

        if labs_db:
            for indice, lab in enumerate(labs_db):
                fila = indice // 3
                columna = indice % 3
                self._dibujar_tarjeta_lab(self.scroll_labs, fila, columna, lab)
        else:
            ctk.CTkLabel(self.scroll_labs, text="No se encontraron laboratorios.", font=ctk.CTkFont("Arial", 16), text_color="black").grid(row=0, column=0, pady=50)

    def _dibujar_tarjeta_lab(self, padre, fila, columna, lab):
        import textwrap 

        tarjeta = ctk.CTkFrame(padre, fg_color="white", corner_radius=10)
        tarjeta.grid(row=fila, column=columna, padx=15, pady=15, sticky="nsew")

        raw_estado = lab.get('Estado') or lab.get('estado') or 'Disponible'
        estado_actual = str(raw_estado).strip().capitalize()

        if estado_actual == 'Disponible':
            color_fondo_estado = "#dcfce7"
            color_texto_estado = "#166534"
            texto_etiqueta = "Disponible"
            texto_boton_accion = "Desactivar"
            color_hover_boton = "#fee2e2"
        elif estado_actual in ['En mantenimiento', 'Mantenimiento']:
            color_fondo_estado = "#fef9c3"
            color_texto_estado = "#854d0e"
            texto_etiqueta = "Mantenimiento"
            texto_boton_accion = "Activar"
            color_hover_boton = "#dcfce7"
        else:
            color_fondo_estado = "#f3f4f6"
            color_texto_estado = "#4b5563"
            texto_etiqueta = "Inactivo"
            texto_boton_accion = "Activar"
            color_hover_boton = "#dcfce7"

        top_frame = ctk.CTkFrame(tarjeta, fg_color="transparent")
        top_frame.pack(fill="x", padx=15, pady=(15, 5))

        ctk.CTkLabel(top_frame, text="🧪", font=ctk.CTkFont("Arial", 22), fg_color="#d1e5df", text_color="#045b4a", corner_radius=8, width=38, height=38).pack(side="left")
        ctk.CTkLabel(top_frame, text=texto_etiqueta, font=ctk.CTkFont("Arial", 10, "bold"), fg_color=color_fondo_estado, text_color=color_texto_estado, corner_radius=5).pack(side="right")

        nombre_lab = lab.get('Nombre_lab') or lab.get('nombre') or 'Laboratorio'
        ubicacion_lab = lab.get('Ubicacion') or lab.get('ubicacion') or lab.get('Edificio') or 'Edificio A - Planta baja'
        capacidad = lab.get('Capacidad') or lab.get('capacidad') or 0
        equipos = lab.get('Cantidad_equipos') or lab.get('cantidad_equipos') or capacidad

        nombre_lab_formateado = textwrap.fill(nombre_lab, width=20)

        ctk.CTkLabel(tarjeta, text=nombre_lab_formateado, font=ctk.CTkFont("Arial", 14, "bold"), text_color="black", justify="left").pack(anchor="w", padx=15, pady=(10, 0))
        ctk.CTkLabel(tarjeta, text=ubicacion_lab, font=ctk.CTkFont("Arial", 11), text_color=COLOR_TEXTO_GRIS).pack(anchor="w", padx=15, pady=(0, 10))

        div = ctk.CTkFrame(tarjeta, fg_color="#e5e5e5", height=1)
        div.pack(fill="x", padx=15, pady=5)

        stats_frame = ctk.CTkFrame(tarjeta, fg_color="transparent")
        stats_frame.pack(fill="x", padx=15, pady=10)
        stats_frame.grid_columnconfigure((0, 1), weight=1)

        cap_frame = ctk.CTkFrame(stats_frame, fg_color="transparent")
        cap_frame.grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(cap_frame, text=str(capacidad), font=ctk.CTkFont("Arial", 14, "bold"), text_color="black").pack()
        ctk.CTkLabel(cap_frame, text="Capacidad", font=ctk.CTkFont("Arial", 10), text_color=COLOR_TEXTO_GRIS).pack()

        div_v = ctk.CTkFrame(stats_frame, fg_color="#e5e5e5", width=1, height=30)
        div_v.grid(row=0, column=0, sticky="e")

        eq_frame = ctk.CTkFrame(stats_frame, fg_color="transparent")
        eq_frame.grid(row=0, column=1, sticky="e")
        ctk.CTkLabel(eq_frame, text=f"{equipos} equipos", font=ctk.CTkFont("Arial", 14, "bold"), text_color="black").pack()
        ctk.CTkLabel(eq_frame, text="Equipamiento", font=ctk.CTkFont("Arial", 10), text_color=COLOR_TEXTO_GRIS).pack()

        btn_frame = ctk.CTkFrame(tarjeta, fg_color="transparent")
        btn_frame.pack(fill="x", padx=15, pady=(10, 15))

        btn_editar = ctk.CTkButton(btn_frame, text="✎ Editar", width=70, height=24, fg_color="#f3f4f6", text_color="black", hover_color="#e5e7eb", font=ctk.CTkFont("Arial", 11, "bold"), command=lambda l=lab: self.abrir_modal_laboratorio(l))
        btn_editar.pack(side="left")

        id_lab = lab.get('id_Lab') or lab.get('id_lab') or lab.get('id_laboratorio')
        btn_estado = ctk.CTkButton(
            btn_frame, 
            text=texto_boton_accion, 
            width=70, 
            height=24, 
            fg_color="transparent", 
            text_color=COLOR_TEXTO_GRIS, 
            hover_color=color_hover_boton, 
            font=ctk.CTkFont("Arial", 11, "bold"), 
            command=lambda l_id=id_lab, e=estado_actual: self.cambiar_estado_laboratorio(l_id, e)
        )
        btn_estado.pack(side="right")

    def cambiar_estado_laboratorio(self, id_lab, estado_actual):
        nuevo_estado = "Inactivo" if estado_actual == "Disponible" else "Disponible"
        resultado = self.controlador.cambiar_estado_laboratorio(id_lab, nuevo_estado)
        if resultado['exito']:
            self.cargar_tarjetas_laboratorios(self.entrada_busqueda_labs.get())
        else:
            from tkinter import messagebox
            messagebox.showerror("Error", resultado['mensaje'])

    def abrir_modal_laboratorio(self, lab=None):
        modal = ctk.CTkToplevel(self)
        titulo_principal = "Editar laboratorio" if lab else "Nuevo laboratorio"
        modal.title(titulo_principal)
        modal.geometry("500x580")
        modal.resizable(False, False)
        modal.configure(fg_color="white")
        modal.transient(self)
        modal.grab_set()

        header_frame = ctk.CTkFrame(modal, fg_color="transparent")
        header_frame.pack(fill="x", padx=30, pady=(30, 15))
        
        ctk.CTkLabel(header_frame, text="A D M I N I S T R A D O R", font=ctk.CTkFont("Arial", 11, "bold"), text_color="#166534").pack(anchor="w")
        
        title_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_container.pack(fill="x", pady=(5, 0))
        
        ctk.CTkLabel(title_container, text=titulo_principal, font=ctk.CTkFont("Arial", 22, "bold"), text_color="black").pack(side="left")
        
        btn_cerrar_modal = ctk.CTkButton(title_container, text="×", width=35, height=35, fg_color="#f3f4f6", text_color="black", hover_color="#e5e7eb", font=ctk.CTkFont("Arial", 18), corner_radius=8, command=modal.destroy)
        btn_cerrar_modal.pack(side="right")

        div = ctk.CTkFrame(modal, fg_color="#e5e5e5", height=1)
        div.pack(fill="x", pady=(0, 25))

        form_frame = ctk.CTkFrame(modal, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=30)

        ctk.CTkLabel(form_frame, text="Nombre del laboratorio", font=ctk.CTkFont("Arial", 12, "bold"), text_color="#4b5563").pack(anchor="w")
        ent_nombre = ctk.CTkEntry(form_frame, placeholder_text="Ej. Laboratorio de Desarrollo", height=45, fg_color="white", border_color="#d1d5db", border_width=1, text_color="black")
        ent_nombre.pack(fill="x", pady=(5, 15))

        ctk.CTkLabel(form_frame, text="Ubicación / Edificio", font=ctk.CTkFont("Arial", 12, "bold"), text_color="#4b5563").pack(anchor="w")
        ent_ubicacion = ctk.CTkEntry(form_frame, placeholder_text="Ej. Edificio A - Planta baja", height=45, fg_color="white", border_color="#d1d5db", border_width=1, text_color="black")
        ent_ubicacion.pack(fill="x", pady=(5, 15))

        caps_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        caps_frame.pack(fill="x", pady=(5, 20))
        caps_frame.grid_columnconfigure((0, 1), weight=1)

        f1 = ctk.CTkFrame(caps_frame, fg_color="transparent")
        f1.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        ctk.CTkLabel(f1, text="Capacidad", font=ctk.CTkFont("Arial", 12, "bold"), text_color="#4b5563").pack(anchor="w")
        ent_capacidad = ctk.CTkEntry(f1, placeholder_text="32", height=45, fg_color="white", border_color="#d1d5db", border_width=1, text_color="black")
        ent_capacidad.pack(fill="x", pady=(5, 0))

        f2 = ctk.CTkFrame(caps_frame, fg_color="transparent")
        f2.grid(row=0, column=1, sticky="ew", padx=(10, 0))
        ctk.CTkLabel(f2, text="Equipamiento", font=ctk.CTkFont("Arial", 12, "bold"), text_color="#4b5563").pack(anchor="w")
        ent_equipos = ctk.CTkEntry(f2, placeholder_text="30", height=45, fg_color="white", border_color="#d1d5db", border_width=1, text_color="black")
        ent_equipos.pack(fill="x", pady=(5, 0))

        botones_frame = ctk.CTkFrame(modal, fg_color="transparent")
        botones_frame.pack(fill="x", padx=30, pady=(0, 30))
        
        texto_btn_accion = "Guardar cambios" if lab else "Agregar laboratorio"
        
        btn_accion = ctk.CTkButton(botones_frame, text=texto_btn_accion, width=170, height=45, font=ctk.CTkFont("Arial", 14, "bold"), fg_color="#045b4a", hover_color="#03483a", corner_radius=8, command=lambda: guardar())
        btn_accion.pack(side="right", padx=(10, 0))

        btn_cancelar = ctk.CTkButton(botones_frame, text="Cancelar", width=110, height=45, font=ctk.CTkFont("Arial", 14, "bold"), fg_color="white", text_color="#4b5563", border_color="#d1d5db", border_width=1, hover_color="#f3f4f6", corner_radius=8, command=modal.destroy)
        btn_cancelar.pack(side="right")

        if lab:
            ent_nombre.insert(0, str(lab.get('Nombre_lab') or ''))
            ent_ubicacion.insert(0, str(lab.get('Ubicacion') or ''))
            ent_capacidad.insert(0, str(lab.get('Capacidad') or ''))
            ent_equipos.insert(0, str(lab.get('Cantidad_equipos') or lab.get('cantidad_equipos') or ''))

        def guardar():
            nom = ent_nombre.get().strip()
            ubi = ent_ubicacion.get().strip() or "Edificio A - Planta baja"
            cap = ent_capacidad.get().strip()
            eq = ent_equipos.get().strip()

            if not nom or not cap:
                from tkinter import messagebox
                messagebox.showwarning("Campos vacíos", "Ingresa al menos el nombre y la capacidad.", parent=modal)
                return

            try:
                cap_int = int(cap)
                eq_int = int(eq) if eq.isdigit() else cap_int
            except ValueError:
                from tkinter import messagebox
                messagebox.showerror("Error de formato", "Capacidad y equipamiento deben ser números.", parent=modal)
                return

            if lab:
                id_lab = lab.get('id_Lab') or lab.get('id_lab') or lab.get('id_laboratorio')
                estado = lab.get('Estado') or lab.get('estado') or 'Disponible'
                res = self.controlador.actualizar_laboratorio(id_lab, nom, cap_int, eq_int, ubi, estado)
            else:
                res = self.controlador.agregar_laboratorio(nom, cap_int, eq_int, ubi)

            if res['exito']:
                modal.destroy()
                self.cargar_tarjetas_laboratorios(self.entrada_busqueda_labs.get())
            else:
                from tkinter import messagebox
                messagebox.showerror("Error DB", res['mensaje'], parent=modal)