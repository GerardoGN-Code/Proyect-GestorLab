import customtkinter as ctk
import os
import sys
import textwrap

ruta_proyecto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ruta_proyecto)

from Logica.controlador_docente import ControladorDocente

COLOR_VERDE_OSCURO = "#045b4a"
COLOR_GRIS_FONDO = "#e5e5e5"
COLOR_TEXTO_GRIS = "#7f7f7f"

class VistaDocente(ctk.CTkFrame):
    def __init__(self, master, nombre_usuario, al_cerrar_sesion):
        super().__init__(master, fg_color=COLOR_GRIS_FONDO, corner_radius=0)
        
        self.nombre_usuario = nombre_usuario or "Docente"
        self.al_cerrar_sesion = al_cerrar_sesion
        self.controlador = ControladorDocente()
        
        self.horarios_completos = self.controlador.obtener_horario_docente(self.nombre_usuario) or []

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._crear_header()
        self._crear_cuerpo()

    def _crear_header(self):
        header_frame = ctk.CTkFrame(self, fg_color=COLOR_VERDE_OSCURO, corner_radius=0)
        header_frame.grid(row=0, column=0, sticky="ew")
        header_frame.grid_columnconfigure(1, weight=1)

        logo_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        logo_frame.grid(row=0, column=0, sticky="w", padx=30, pady=15)
        ctk.CTkLabel(logo_frame, text="GestorLab", font=ctk.CTkFont("Arial", 20, "bold"), text_color="white").pack(anchor="w")
        ctk.CTkLabel(logo_frame, text="TESCHI", font=ctk.CTkFont("Arial", 11), text_color="#a0c4b9").pack(anchor="w")

        ctk.CTkLabel(header_frame, text="Mis horarios", font=ctk.CTkFont("Arial", 22, "bold"), text_color="white").grid(row=0, column=1)

        perfil_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        perfil_frame.grid(row=0, column=2, sticky="e", padx=30, pady=15)
        
        ctk.CTkLabel(perfil_frame, text=self.nombre_usuario, font=ctk.CTkFont("Arial", 14, "bold"), text_color="white").pack(anchor="e")
        ctk.CTkLabel(perfil_frame, text="Docente", font=ctk.CTkFont("Arial", 11), text_color="#a0c4b9").pack(anchor="e")
        
        btn_cerrar = ctk.CTkButton(perfil_frame, text="cerrar sesión ➔", fg_color="#e63946", hover_color="#c1121f", font=ctk.CTkFont("Arial", 11, "bold"), height=24, width=110, command=self.al_cerrar_sesion)
        btn_cerrar.pack(anchor="e", pady=(5,0))

    def _crear_cuerpo(self):
        self.scroll_body = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_body.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

        ctk.CTkLabel(self.scroll_body, text=f"Hola, {self.nombre_usuario}", font=ctk.CTkFont("Arial", 26, "bold"), text_color="black").pack(anchor="w", padx=15, pady=(10, 0))
        ctk.CTkLabel(self.scroll_body, text="Estos son tus grupos asignados para el periodo actual", font=ctk.CTkFont("Arial", 14), text_color=COLOR_TEXTO_GRIS).pack(anchor="w", padx=15, pady=(0, 20))

        self._crear_tarjetas_resumen()
        self._crear_modulo_horario()

    def _crear_tarjetas_resumen(self):
        num_grupos = len(set(c.get('Grupo') for c in self.horarios_completos if c.get('Grupo')))
        num_clases = len(self.horarios_completos)
        
        horas_totales = 0
        for c in self.horarios_completos:
            try:
                h_in = int(str(c.get('Hora_inicio', '00:00'))[:2])
                h_out = int(str(c.get('Hora_final', '00:00'))[:2])
                horas_totales += (h_out - h_in)
            except: pass
            
        labs_unicos = list(set(c.get('Nombre_lab') for c in self.horarios_completos if c.get('Nombre_lab')))
        num_labs = len(labs_unicos)
        nombres_labs = ", ".join(labs_unicos[:2]) + ("..." if num_labs > 2 else "")

        texto_horas = "horas totales" if horas_totales > 0 else ""
        texto_grupos = "En el periodo actual" if num_grupos > 0 else ""

        cards_frame = ctk.CTkFrame(self.scroll_body, fg_color="transparent")
        cards_frame.pack(fill="x", padx=10, pady=(0, 20))

        def crear_tarjeta(padre, titulo, valor, subtitulo, icono):
            t = ctk.CTkFrame(padre, fg_color="white", corner_radius=10)
            t.pack(side="left", padx=10, fill="x", expand=True)
            
            icon_lbl = ctk.CTkLabel(t, text=icono, font=("Arial", 24), fg_color="#dcfce7", text_color=COLOR_VERDE_OSCURO, corner_radius=8, width=40, height=40)
            icon_lbl.pack(side="left", padx=15, pady=15)
            
            txt_frame = ctk.CTkFrame(t, fg_color="transparent")
            txt_frame.pack(side="left", fill="both", expand=True, pady=10)
            ctk.CTkLabel(txt_frame, text=titulo, font=ctk.CTkFont("Arial", 11), text_color=COLOR_TEXTO_GRIS).pack(anchor="w")
            
            val_frame = ctk.CTkFrame(txt_frame, fg_color="transparent")
            val_frame.pack(fill="x")
            ctk.CTkLabel(val_frame, text=str(valor), font=ctk.CTkFont("Arial", 18, "bold"), text_color="black").pack(side="left")
            ctk.CTkLabel(val_frame, text=subtitulo, font=ctk.CTkFont("Arial", 10), text_color=COLOR_TEXTO_GRIS).pack(side="left", padx=5, pady=(5,0))

        crear_tarjeta(cards_frame, "Grupos asignados", num_grupos, texto_grupos, "💬")
        crear_tarjeta(cards_frame, "Clases esta semana", num_clases, texto_horas, "📅")
        crear_tarjeta(cards_frame, "Laboratorios", num_labs, nombres_labs, "🧪")

    def _crear_modulo_horario(self):
        main_container = ctk.CTkFrame(self.scroll_body, fg_color="white", corner_radius=15, border_width=1, border_color="#d1d5db")
        main_container.pack(fill="both", expand=True, padx=15, pady=10)

        header_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        header_frame.pack(fill="x", padx=25, pady=(25, 15))
        ctk.CTkLabel(header_frame, text="Mis grupos asignados", font=ctk.CTkFont("Arial", 22, "bold"), text_color="black").pack(side="left")
        
        btn_exportar = ctk.CTkButton(header_frame, text="⭳ Exportar PDF", fg_color="white", text_color="black", border_color="#d1d5db", border_width=1, hover_color="#f3f4f6", font=ctk.CTkFont("Arial", 12, "bold"), command=self.exportar_pdf_horario)
        btn_exportar.pack(side="right")

        filtros_frame = ctk.CTkFrame(main_container, fg_color="#e5e5e5", corner_radius=0, height=75)
        filtros_frame.pack(fill="x")
        filtros_frame.pack_propagate(False)
        inner_filtros = ctk.CTkFrame(filtros_frame, fg_color="transparent")
        inner_filtros.pack(fill="both", expand=True, padx=25, pady=10)

        busqueda_frame = ctk.CTkFrame(inner_filtros, fg_color="transparent")
        busqueda_frame.pack(side="left", padx=(0, 15))
        ctk.CTkLabel(busqueda_frame, text="Búsqueda por materia...", font=ctk.CTkFont("Arial", 10), text_color="#7f7f7f").pack(anchor="w")
        self.entrada_busqueda = ctk.CTkEntry(busqueda_frame, placeholder_text="🔍 Escribe aquí...", width=200, fg_color="white", text_color="black")
        self.entrada_busqueda.pack()
        self.entrada_busqueda.bind("<KeyRelease>", self.filtrar_horarios)

        g_frame = ctk.CTkFrame(inner_filtros, fg_color="transparent")
        g_frame.pack(side="left", padx=10)
        ctk.CTkLabel(g_frame, text="Grupos", font=ctk.CTkFont("Arial", 10), text_color="#7f7f7f").pack(anchor="w")
        grupos = ["Todos"] + self.controlador.obtener_lista_grupos(self.nombre_usuario)
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
        labs = ["Todos"] + self.controlador.obtener_lista_laboratorios(self.nombre_usuario)
        self.cb_labs = ctk.CTkComboBox(l_frame, values=labs, width=200, fg_color="white", text_color="black", command=self.filtrar_horarios)
        self.cb_labs.pack()

        self.tabla_frame = ctk.CTkFrame(main_container, fg_color="#d1d5db", corner_radius=0)
        self.tabla_frame.pack(fill="both", expand=True, padx=25, pady=20)

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
        busqueda = self.entrada_busqueda.get().lower()

        horarios_filtrados = []

        for c in self.horarios_completos:
            match_g = (grupo_f == "Todos" or str(c.get('Grupo')) == grupo_f)
            match_l = (lab_f == "Todos" or str(c.get('Nombre_lab')) == lab_f)
            
            h_inicio = int(str(c.get('Hora_inicio', '00:00'))[:2]) if c.get('Hora_inicio') else 0
            if turno_f == "Matutino": match_t = h_inicio < 14
            elif turno_f == "Vespertino": match_t = h_inicio >= 14
            else: match_t = True
                
            match_b = (busqueda in str(c.get('Nombre_materia','')).lower())
            
            if match_g and match_l and match_t and match_b:
                horarios_filtrados.append(c)

        self._poblar_datos_horario(horarios_filtrados)

    def _dibujar_estructura_tabla(self):
        reloj_frame = ctk.CTkFrame(self.tabla_frame, fg_color=COLOR_VERDE_OSCURO, corner_radius=0, height=35)
        reloj_frame.grid(row=0, column=0, sticky="nsew", padx=(0,1), pady=(0,1))
        reloj_frame.grid_propagate(False)
        ctk.CTkLabel(reloj_frame, text="🕒", font=("Arial", 16), text_color="white").pack(expand=True)

        for i, dia in enumerate(self.dias):
            dia_frame = ctk.CTkFrame(self.tabla_frame, fg_color=COLOR_VERDE_OSCURO, corner_radius=0, height=35)
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
                lab = str(clase.get('Nombre_lab') or 'Lab no asignado')

                self._dibujar_bloque_clase(row_start, col_idx, row_span, grupo, materia, lab, tema)
            except: pass

    def _dibujar_bloque_clase(self, fila, columna, rowspan, grupo, materia, lab, tema):
        bloque = ctk.CTkFrame(self.tabla_frame, fg_color=tema["bg"], corner_radius=0)
        bloque.grid(row=fila, column=columna, rowspan=rowspan, sticky="nsew", padx=2, pady=2)
        bloque.grid_propagate(False)

        ctk.CTkFrame(bloque, fg_color=tema["border"], width=4, corner_radius=0).pack(side="left", fill="y")

        text_frame = ctk.CTkFrame(bloque, fg_color="transparent")
        text_frame.pack(side="left", fill="both", expand=True, padx=8, pady=5)
        
        mat_wrap = textwrap.fill(materia, width=25)
        lab_wrap = textwrap.fill(lab, width=25)
        
        ctk.CTkLabel(text_frame, text=grupo, font=ctk.CTkFont("Arial", 10, "bold"), text_color="#4b5563").pack(anchor="w")
        ctk.CTkLabel(text_frame, text=mat_wrap, font=ctk.CTkFont("Arial", 12, "bold"), text_color="black", justify="left").pack(anchor="w", pady=(2, 0))
        ctk.CTkLabel(text_frame, text=self.nombre_usuario, font=ctk.CTkFont("Arial", 9, "bold"), text_color="black", justify="left").pack(anchor="w")
        
        ctk.CTkLabel(text_frame, text=lab_wrap, font=ctk.CTkFont("Arial", 9), text_color=COLOR_TEXTO_GRIS, justify="left").pack(anchor="w", pady=(2, 0))

    def exportar_pdf_horario(self):
        try:
            from fpdf import FPDF
        except ImportError:
            from tkinter import messagebox
            messagebox.showerror("Librería faltante", "Falta la librería FPDF.\nAbre tu terminal y ejecuta:\npip install fpdf")
            return

        pdf = FPDF(orientation='L', unit='mm', format='A4')
        pdf.set_auto_page_break(auto=False)
        pdf.add_page()
        
        pdf.set_font("Arial", 'B', 15)
        pdf.set_text_color(4, 91, 74)
        pdf.cell(0, 8, f"Horario Personal - {self.nombre_usuario}", ln=True, align='C')
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

        for clase in self.horarios_completos: 
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
            lab = str(clase.get('Nombre_lab', ''))
            
            mx = bx + 3.5
            w_util = bw - 4.5

            if span == 1:
                pdf.set_font("Arial", 'B', 6)
                pdf.set_text_color(0, 0, 0)
                txt_head = f"{grup} | {mat}"
                pdf.set_xy(mx, by + 1.2)
                pdf.cell(w_util, 2.5, txt_head[:34], align='L')
                
                pdf.set_font("Arial", '', 5)
                pdf.set_text_color(120, 120, 120)
                pdf.set_xy(mx, by + 4.2)
                pdf.cell(w_util, 2.0, lab[:36], align='L')
            else:
                pdf.set_font("Arial", 'B', 6)
                pdf.set_text_color(80, 80, 80)
                pdf.set_xy(mx, by + 1.2)
                pdf.cell(w_util, 2.5, grup, align='L')
                
                pdf.set_font("Arial", 'B', 6.5)
                pdf.set_text_color(0, 0, 0)
                pdf.set_xy(mx, by + 4.0)
                pdf.cell(w_util, 2.8, mat[:34], align='L')
                
                pdf.set_font("Arial", '', 5)
                pdf.set_text_color(120, 120, 120)
                pdf.set_xy(mx, by + bh - 3.2)
                pdf.cell(w_util, 2.2, lab[:36], align='L')

        from tkinter import filedialog, messagebox
        primer_nombre = self.nombre_usuario.split()[0]
        ruta_guardar = filedialog.asksaveasfilename(
            defaultextension=".pdf", 
            filetypes=[("Archivos PDF", "*.pdf")], 
            initialfile=f"Horario_{primer_nombre}.pdf"
        )
        if ruta_guardar:
            try:
                pdf.output(ruta_guardar)
                messagebox.showinfo("Éxito", f"PDF exportado correctamente en:\n{ruta_guardar}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el PDF:\n{e}")