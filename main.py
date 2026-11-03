import customtkinter as ctk
import os
import sys

ruta_proyecto = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ruta_proyecto)

from Visual.vista_login import VistaLogin
from Visual.vista_admin import VistaAdmin
from Visual.vista_docente import VistaDocente
from Visual.vista_jefe_carrera import VistaJefeCarrera

ctk.set_appearance_mode("System") 
ctk.set_default_color_theme("green")

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("GestorLab - TESCHI")
        self.geometry("1100x700")
        self.minsize(950, 600)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.vista_actual = None
        self.mostrar_login()

    def limpiar_ventana(self):
        if self.vista_actual:
            self.vista_actual.destroy()

    def mostrar_login(self):
        self.limpiar_ventana()
        self.vista_actual = VistaLogin(self, self.manejar_autenticacion)
        self.vista_actual.grid(row=0, column=0, sticky="nsew")

    def manejar_autenticacion(self, resultado_auth):
        datos_usuario = resultado_auth.get('datos', {})
        rol = str(datos_usuario.get('rol', '')).strip().lower()
        nombre = datos_usuario.get('Usuario', 'Usuario')

        self.limpiar_ventana()

        if 'admin' in rol:
            self.vista_actual = VistaAdmin(self, nombre, self.mostrar_login)
        elif 'jefe' in rol:
            self.vista_actual = VistaJefeCarrera(self, nombre, self.mostrar_login)
        elif 'docente' in rol:
            self.vista_actual = VistaDocente(self, nombre, self.mostrar_login)
        else:
            self.mostrar_login()

        if self.vista_actual:
            self.vista_actual.grid(row=0, column=0, sticky="nsew")

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()