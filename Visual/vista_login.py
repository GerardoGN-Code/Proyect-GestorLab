import customtkinter as ctk
from tkinter import messagebox
import os
import sys

ruta_proyecto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ruta_proyecto)

from Logica.controlador_login import ControladorLogin

COLOR_VERDE_OSCURO = "#045b4a"
COLOR_VERDE_BOTON = "#036f56"
COLOR_TEXTO_GRIS = "#7f7f7f"

class VistaLogin(ctk.CTkFrame):
    def __init__(self, master, al_autenticar):
        super().__init__(master, fg_color="white", corner_radius=0)
        
        self.al_autenticar = al_autenticar
        self.controlador = ControladorLogin()

        self.grid_columnconfigure(0, weight=4)
        self.grid_columnconfigure(1, weight=6)
        self.grid_rowconfigure(0, weight=1)

        self._crear_panel_izquierdo()
        self._crear_panel_derecho()

    def _crear_panel_izquierdo(self):
        frame_izq = ctk.CTkFrame(self, fg_color=COLOR_VERDE_OSCURO, corner_radius=0)
        frame_izq.grid(row=0, column=0, sticky="nsew")

        margen = ctk.CTkFrame(frame_izq, fg_color="transparent")
        margen.pack(padx=40, pady=50, fill="both", expand=True)

        ctk.CTkLabel(margen, text="GestorLab", font=("Arial", 24, "bold"), text_color="white", anchor="w").pack(fill="x")
        ctk.CTkLabel(margen, text="TESCHI", font=("Arial", 14), text_color="#a0c4b9", anchor="w").pack(fill="x", pady=(0, 50))

        ctk.CTkLabel(margen, text="GESTION ACADEMICA INTELIGENTE", font=("Arial", 10, "bold"), text_color="#a0c4b9", anchor="w").pack(fill="x")
        
        texto_grande = "Laboratorios\nmejor\norganizados\nclases sin\ncontratiempos"
        ctk.CTkLabel(margen, text=texto_grande, font=("Arial", 38, "bold"), text_color="white", justify="left", anchor="w").pack(fill="x", pady=(10, 0))

    def _crear_panel_derecho(self):
        frame_der = ctk.CTkFrame(self, fg_color="white", corner_radius=0)
        frame_der.grid(row=0, column=1, sticky="nsew")

        form_frame = ctk.CTkFrame(frame_der, fg_color="transparent")
        form_frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(form_frame, text="Bienvenido de nuevo", font=("Arial", 14, "bold"), text_color=COLOR_VERDE_BOTON, anchor="w").pack(fill="x")
        ctk.CTkLabel(form_frame, text="Inicia sesión", font=("Arial", 32, "bold"), text_color="black", anchor="w").pack(fill="x", pady=(5, 5))
        ctk.CTkLabel(form_frame, text="Ingresa tus credenciales para continuar", font=("Arial", 12), text_color=COLOR_TEXTO_GRIS, anchor="w").pack(fill="x", pady=(0, 30))

        ctk.CTkLabel(form_frame, text="Usuario o matrícula", font=("Arial", 12, "bold"), text_color="black", anchor="w").pack(fill="x")
        self.entrada_usuario = ctk.CTkEntry(form_frame, width=350, height=40, fg_color="white", text_color="black", border_color="#d3d3d3")
        self.entrada_usuario.pack(pady=(5, 15))

        ctk.CTkLabel(form_frame, text="Contraseña", font=("Arial", 12, "bold"), text_color="black", anchor="w").pack(fill="x")
        self.entrada_contrasena = ctk.CTkEntry(form_frame, width=350, height=40, fg_color="white", text_color="black", border_color="#d3d3d3")
        self.entrada_contrasena.pack(pady=(5, 30))

        btn_login = ctk.CTkButton(form_frame, text="iniciar sesión", width=350, height=45, font=("Arial", 16, "bold"), fg_color=COLOR_VERDE_BOTON, hover_color=COLOR_VERDE_OSCURO, command=self.evento_login)
        btn_login.pack()

        texto_soporte = "¿Problemas para acceder? Contacta a soporte"
        ctk.CTkLabel(form_frame, text=texto_soporte, font=("Arial", 11), text_color=COLOR_TEXTO_GRIS).pack(pady=(20, 0))

    def evento_login(self):
        usuario = self.entrada_usuario.get().strip()
        contrasena = self.entrada_contrasena.get().strip()

        if not usuario or not contrasena:
            messagebox.showwarning("Campos vacios", "Por favor ingresa usuario y contraseña")
            return

        resultado = self.controlador.autenticar_usuario(usuario, contrasena)

        if resultado['exito']:
            self.al_autenticar(resultado)
        else:
            messagebox.showerror("Error", resultado['mensaje'])