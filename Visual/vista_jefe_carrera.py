import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import sys

ruta_proyecto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ruta_proyecto)

from Logica.controlador_pdf import ControladorPDF

COLOR_VERDE_OSCURO = "#045b4a"
COLOR_VERDE_BOTON = "#036f56"
COLOR_GRIS_FONDO = "#e5e5e5"
COLOR_TEXTO_GRIS = "#7f7f7f"

class VistaJefeCarrera(ctk.CTkFrame):
    def __init__(self, master, nombre_usuario, al_cerrar_sesion=None):
        super().__init__(master, fg_color=COLOR_GRIS_FONDO, corner_radius=0)

        self.nombre_usuario = nombre_usuario
        self.al_cerrar_sesion = al_cerrar_sesion
        self.controlador_pdf = ControladorPDF()

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._crear_encabezado()
        self._crear_cuerpo()

    def _crear_encabezado(self):
        header_frame = ctk.CTkFrame(self, fg_color=COLOR_VERDE_OSCURO, corner_radius=0, height=100)
        header_frame.grid(row=0, column=0, sticky="ew")
        header_frame.grid_propagate(False)

        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_columnconfigure(1, weight=2)
        header_frame.grid_columnconfigure(2, weight=1)

        izq_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        izq_frame.grid(row=0, column=0, sticky="w", padx=40, pady=20)
        
        ctk.CTkLabel(izq_frame, text="GestorLab", font=ctk.CTkFont("Arial", 22, "bold"), text_color="white").pack(anchor="w", pady=(0, 2))
        ctk.CTkLabel(izq_frame, text="TESCHI", font=ctk.CTkFont("Arial", 12), text_color="#a0c4b9").pack(anchor="w")

        ctk.CTkLabel(header_frame, text="Carga de horario semestral", font=ctk.CTkFont("Arial", 24, "bold"), text_color="white").grid(row=0, column=1)

        der_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        der_frame.grid(row=0, column=2, sticky="e", padx=40, pady=15)

        ctk.CTkLabel(der_frame, text=self.nombre_usuario, font=ctk.CTkFont("Arial", 14, "bold"), text_color="white").pack(anchor="e")
        ctk.CTkLabel(der_frame, text="Jefe de carrera", font=ctk.CTkFont("Arial", 12), text_color="#a0c4b9").pack(anchor="e", pady=(0, 5))

        btn_cerrar = ctk.CTkButton(
            der_frame, 
            text="cerrar sesión ➔", 
            width=110, 
            height=24, 
            fg_color="#e63946", 
            hover_color="#c1121f", 
            font=ctk.CTkFont(family="Arial", size=11, weight="bold"), 
            corner_radius=6, 
            command=self.cerrar_sesion
        )
        btn_cerrar.pack(anchor="e")

    def _crear_cuerpo(self):
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.grid(row=1, column=0, sticky="nsew", padx=50, pady=30)

        ctk.CTkLabel(main_frame, text="Nuevo horario", font=ctk.CTkFont("Arial", 26, "bold"), text_color="black").pack(anchor="w")
        ctk.CTkLabel(main_frame, text="Sube el documento oficial para iniciar su validación", font=ctk.CTkFont("Arial", 13), text_color=COLOR_TEXTO_GRIS).pack(anchor="w", pady=(0, 25))

        cards_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        cards_frame.pack(fill="both", expand=True)
        
        cards_frame.grid_columnconfigure(0, weight=13)
        cards_frame.grid_columnconfigure(1, weight=10)
        cards_frame.grid_rowconfigure(0, weight=1)

        carga_frame = ctk.CTkFrame(cards_frame, fg_color="white", corner_radius=12, border_width=2, border_color="#3b82f6")
        carga_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 25))
        
        center_carga = ctk.CTkFrame(carga_frame, fg_color="transparent")
        center_carga.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(center_carga, text="[↑]", font=ctk.CTkFont("Arial", 45), text_color=COLOR_VERDE_BOTON).pack(pady=(0,15))
        ctk.CTkLabel(center_carga, text="Carga el horario oficial", font=ctk.CTkFont("Arial", 18, "bold"), text_color="black").pack()
        ctk.CTkLabel(center_carga, text="Arrastra aquí el archivo PDF o selecciónalo desde tu equipo", font=ctk.CTkFont("Arial", 12), text_color=COLOR_TEXTO_GRIS).pack(pady=(8, 25))
        
        btn_seleccionar = ctk.CTkButton(
            center_carga, 
            text="Seleccionar archivo PDF", 
            fg_color=COLOR_VERDE_BOTON, 
            hover_color=COLOR_VERDE_OSCURO, 
            font=ctk.CTkFont(family="Arial", size=14, weight="bold"), 
            height=40, 
            width=200, 
            command=self.seleccionar_pdf
        )
        btn_seleccionar.pack()

        instrucciones_frame = ctk.CTkFrame(cards_frame, fg_color="white", corner_radius=12, border_width=1, border_color="#e5e7eb")
        instrucciones_frame.grid(row=0, column=1, sticky="nsew")

        inner_inst = ctk.CTkFrame(instrucciones_frame, fg_color="transparent")
        inner_inst.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(inner_inst, text="Antes de cargar", font=ctk.CTkFont("Arial", 20, "bold"), text_color="black").pack(anchor="center", pady=(0, 35))

        self._crear_item_instruccion(inner_inst, "Documento legible", "Verifica que el contenido no esté borroso")
        self._crear_item_instruccion(inner_inst, "Semestre correcto", "Debe corresponder al semestre actual")
        self._crear_item_instruccion(inner_inst, "Formato oficial", "Incluye grupos, docentes y laboratorios")

    def _crear_item_instruccion(self, parent, titulo, subtitulo):
        item_frame = ctk.CTkFrame(parent, fg_color="transparent")
        item_frame.pack(fill="x", pady=15)
        
        ctk.CTkLabel(item_frame, text="☑", font=ctk.CTkFont("Arial", 30), text_color="black").pack(side="left", padx=(0, 20))
        
        text_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        text_frame.pack(side="left")
        
        ctk.CTkLabel(text_frame, text=titulo, font=ctk.CTkFont("Arial", 15, "bold"), text_color="black", anchor="w").pack(fill="x")
        ctk.CTkLabel(text_frame, text=subtitulo, font=ctk.CTkFont("Arial", 12), text_color=COLOR_TEXTO_GRIS, anchor="w").pack(fill="x")

    def seleccionar_pdf(self):
        ruta_archivo = filedialog.askopenfilename(
            title="Seleccionar Horario",
            filetypes=[("Archivos PDF", "*.pdf")]
        )

        if ruta_archivo:
            messagebox.showinfo("Procesando", f"Analizando y guardando el archivo:\n{os.path.basename(ruta_archivo)}\n\nEsto puede tardar unos segundos...")
            
            resultado_pdf = self.controlador_pdf.procesar_archivo(ruta_archivo)
            
            if resultado_pdf['exito'] and resultado_pdf['datos']:
                from Logica.controlador_asignaciones import ControladorAsignaciones
                
                ca = ControladorAsignaciones()
                total_guardadas = ca.procesar_y_guardar_horarios(resultado_pdf['datos'])
                
                if total_guardadas > 0:
                    messagebox.showinfo(
                        "Éxito Total", 
                        f"Se extrajeron y guardaron {total_guardadas} clases en la Base de Datos.\nLos horarios ya están disponibles para los docentes."
                    )
                else:
                    messagebox.showwarning(
                        "Aviso", 
                        "El PDF se leyó pero no se pudo guardar ninguna clase en la base de datos. Verifica la terminal."
                    )
            else:
                messagebox.showerror("Error de lectura", resultado_pdf.get('mensaje', 'El PDF no contenía clases válidas.'))

    def cerrar_sesion(self):
        respuesta = messagebox.askyesno("Cerrar Sesión", "¿Estás seguro que deseas salir?")
        if respuesta:
            if self.al_cerrar_sesion:
                self.al_cerrar_sesion()