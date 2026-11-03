import sqlite3
import os

class ConexionDB:
    def __init__(self):
        ruta_actual = os.path.dirname(os.path.abspath(__file__))
        self.ruta_db = os.path.join(ruta_actual, "Base-de-datos-Proyect-GestorLab.db")
        self.conexion = None
        self.cursor = None

    def conectar(self):
        try:
            self.conexion = sqlite3.connect(self.ruta_db)
            self.conexion.row_factory = sqlite3.Row
            self.cursor = self.conexion.cursor()
        except sqlite3.Error as e:
            print(f"Error al conectar a SQLite: {e}")

    def desconectar(self):
        if self.conexion:
            self.cursor.close()
            self.conexion.close()

    def ejecutar_consulta(self, sql, parametros=()):
        try:
            self.conectar()
            self.cursor.execute(sql, parametros)
            resultados = [dict(fila) for fila in self.cursor.fetchall()]
            return resultados
        except sqlite3.Error as e:
            print(f"Error en consulta SELECT: {e}")
            return None
        finally:
            self.desconectar()

    def ejecutar_modificacion(self, sql, parametros=()):
        try:
            self.conectar()
            self.cursor.execute(sql, parametros)
            self.conexion.commit()
            filas_afectadas = self.cursor.rowcount
            return filas_afectadas > 0
        except sqlite3.Error as e:
            print(f"Error al modificar base de datos: {e}")
            return False
        finally:
            self.desconectar()