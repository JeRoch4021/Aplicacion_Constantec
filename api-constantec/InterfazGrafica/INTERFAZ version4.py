import tkinter as tk
from tkinter import messagebox, ttk

# Colores
COLOR_PRIMARIO = "#1F4172"
COLOR_SECUNDARIO = "#5F85DB"
COLOR_FONDO = "#EEF1F7"
COLOR_TEXTO = "#1F4172"
COLOR_BOTON = "#1F4172"
COLOR_BLANCO = "#FFFFFF"
COLOR_SOLICITAR = "#FFD700"


class ConstantecApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CONSTANTEC - Campus León 1")
        self.geometry("360x640")
        self.configure(bg=COLOR_FONDO)
        self.resizable(False, False)
        self.frames = {}
        self.datos_estudiante = {}

        for F in (
            PantallaBienvenida,
            LoginFrame,
            RecuperarPassword,
            MenuPrincipal,
            HistorialConstancias,
            TutorialUso,
            DatosGenerales,
            SolicitarConstancia,
            FormularioPersonalizado,
            ResumenSolicitud,
        ):
            frame = F(self)
            self.frames[F] = frame
            frame.place(relwidth=1, relheight=1)

        self.mostrar_frame(PantallaBienvenida)

    def mostrar_frame(self, contenedor):
        frame = self.frames[contenedor]
        frame.tkraise()


class BasePantalla(tk.Frame):
    def __init__(self, master, titulo=""):
        super().__init__(master, bg=COLOR_FONDO)
        tk.Label(self, text="[Logo Aquí]", bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(
            anchor="nw", padx=10, pady=5
        )
        if titulo:
            tk.Label(
                self,
                text=titulo,
                font=("Helvetica", 16, "bold"),
                bg=COLOR_FONDO,
                fg=COLOR_TEXTO,
            ).pack(pady=10)
        tk.Button(
            self,
            text="🏠",
            command=lambda: master.mostrar_frame(MenuPrincipal),
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO,
            borderwidth=0,
        ).place(x=320, y=10)


class PantallaBienvenida(BasePantalla):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(
            self,
            text="BIENVENIDO A\nCONSTANTEC",
            font=("Helvetica", 20, "bold"),
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO,
        ).pack(pady=80)
        tk.Button(
            self,
            text="Ingresar",
            command=lambda: master.mostrar_frame(LoginFrame),
            bg=COLOR_BOTON,
            fg=COLOR_BLANCO,
            height=2,
            width=25,
            font=("Helvetica", 12, "bold"),
        ).pack()


class LoginFrame(BasePantalla):
    def __init__(self, master):
        super().__init__(master, "INICIO DE SESIÓN")
        self.email_entry = self.crear_entry("Correo institucional")
        self.pass_entry = self.crear_entry("Contraseña", show="*")
        tk.Button(
            self,
            text="Ingresar",
            bg=COLOR_BOTON,
            fg=COLOR_BLANCO,
            width=25,
            command=lambda: master.mostrar_frame(MenuPrincipal),
        ).pack(pady=15)
        tk.Button(
            self,
            text="¿Olvidaste tu contraseña?",
            fg=COLOR_SECUNDARIO,
            bg=COLOR_FONDO,
            bd=0,
        ).pack()

    def crear_entry(self, placeholder, show=""):
        frame = tk.Frame(self, bg=COLOR_FONDO)
        frame.pack(pady=5)
        entry = tk.Entry(frame, width=30, font=("Helvetica", 12), show=show)
        entry.insert(0, placeholder)
        entry.pack(ipady=6)
        return entry


class RecuperarPassword(BasePantalla):
    def __init__(self, master):
        super().__init__(master, "RECUPERAR CONTRASEÑA")
        self.correo_entry = tk.Entry(self, width=30, font=("Helvetica", 12))
        self.correo_entry.pack(pady=10, ipady=6)
        self.correo_entry.insert(0, "Ingresa tu correo")
        tk.Button(
            self, text="Enviar código", bg=COLOR_BOTON, fg=COLOR_BLANCO, width=25
        ).pack(pady=15)


class MenuPrincipal(BasePantalla):
    def __init__(self, master):
        super().__init__(master, "CAMPUS LEÓN 1")
        tk.Button(
            self,
            text="Información Constancias",
            bg=COLOR_PRIMARIO,
            fg=COLOR_BLANCO,
            width=30,
        ).pack(pady=10)
        tk.Button(
            self,
            text="Historial de Constancias",
            bg=COLOR_PRIMARIO,
            fg=COLOR_BLANCO,
            width=30,
            command=lambda: master.mostrar_frame(HistorialConstancias),
        ).pack(pady=10)
        tk.Button(
            self,
            text="Tutorial de uso",
            bg=COLOR_PRIMARIO,
            fg=COLOR_BLANCO,
            width=30,
            command=lambda: master.mostrar_frame(TutorialUso),
        ).pack(pady=10)
        tk.Button(
            self,
            text="Solicitar Constancia",
            bg=COLOR_SOLICITAR,
            fg=COLOR_TEXTO,
            width=30,
            font=("Helvetica", 10, "bold"),
            command=lambda: master.mostrar_frame(DatosGenerales),
        ).pack(pady=10)


class DatosGenerales(BasePantalla):
    def __init__(self, master):
        super().__init__(master, "DATOS GENERALES")
        self.entries = {}
        for campo in ["Nombre", "No. Control", "Carrera", "Semestre"]:
            tk.Label(self, text=campo, bg=COLOR_FONDO, fg=COLOR_TEXTO).pack()
            entry = tk.Entry(self, width=30)
            entry.pack(pady=2)
            self.entries[campo] = entry
        tk.Button(
            self,
            text="Continuar",
            bg=COLOR_SOLICITAR,
            fg=COLOR_TEXTO,
            command=self.guardar_datos,
        ).pack(pady=10)

    def guardar_datos(self):
        self.master.datos_estudiante = {
            campo: entry.get() for campo, entry in self.entries.items()
        }
        self.master.mostrar_frame(SolicitarConstancia)


class SolicitarConstancia(BasePantalla):
    def __init__(self, master):
        super().__init__(master, "SELECCIONA LA CONSTANCIA")
        self.opciones = [
            "Constancia de inscritos",
            "Constancia de Kardex",
            "Constancia para el seguro social",
            "Constancia con calificaciones del semestre anterior",
            "Constancia con calificaciones de dos semestres anteriores",
            "Constancia de egreso",
            "Constancia de título en trámite",
            "Constancia de pago",
        ]
        for texto in self.opciones:
            tk.Button(
                self,
                text=texto,
                bg=COLOR_BOTON,
                fg=COLOR_BLANCO,
                width=40,
                command=lambda t=texto: self.mostrar_formulario(t),
            ).pack(pady=3)
        tk.Button(
            self,
            text="Constancia Personalizada",
            bg=COLOR_SOLICITAR,
            fg=COLOR_TEXTO,
            width=40,
            command=lambda: master.mostrar_frame(FormularioPersonalizado),
        ).pack(pady=10)
        tk.Button(
            self,
            text="⬅ Regresar",
            command=lambda: master.mostrar_frame(DatosGenerales),
            bg=COLOR_FONDO,
            fg=COLOR_SECUNDARIO,
            bd=0,
        ).pack(pady=10)

    def mostrar_formulario(self, tipo):
        ventana = tk.Toplevel(self)
        ventana.title("Solicitud de " + tipo)
        ventana.geometry("300x300")
        ventana.configure(bg=COLOR_FONDO)
        tk.Label(
            ventana,
            text="¿Para cuándo necesita la constancia?",
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO,
        ).pack(pady=10)
        fecha_entry = ttk.Entry(ventana)
        fecha_entry.pack(pady=5)
        tk.Button(
            ventana,
            text="Enviar",
            bg=COLOR_SOLICITAR,
            fg=COLOR_TEXTO,
            command=lambda: self.confirmar_envio(ventana),
        ).pack(pady=10)

    def confirmar_envio(self, ventana):
        ventana.destroy()
        messagebox.showinfo(
            "Confirmación",
            "Tu solicitud fue registrada con éxito, sigue en el proceso para concluir tu trámite.",
        )
        self.master.mostrar_frame(ResumenSolicitud)


class FormularioPersonalizado(BasePantalla):
    def __init__(self, master):
        super().__init__(master, "CONSTANCIA PERSONALIZADA")
        opciones = [
            "Inscrito (IMSS, ISSSTE, Pagobús)",
            "Promedio general",
            "Promedio semestre anterior",
            "Promedio dos últimos semestres",
            "Egresado",
            "Bachillerato",
            "Maestría",
            "Título en trámite",
            "Incluir número de Seguro Social",
            "Otros",
        ]
        self.vars = {}
        for texto in opciones:
            var = tk.IntVar()
            chk = tk.Checkbutton(
                self, text=texto, variable=var, bg=COLOR_FONDO, fg=COLOR_TEXTO
            )
            chk.pack(anchor="w")
            self.vars[texto] = var

        tk.Label(
            self,
            text="Describe qué necesitas en la constancia:",
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO,
        ).pack(pady=5)
        self.descripcion = tk.Text(self, width=30, height=4)
        self.descripcion.pack(pady=5)

        tk.Label(
            self,
            text="¿Para cuándo necesitas la constancia?",
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO,
        ).pack(pady=5)
        self.fecha = ttk.Entry(self)
        self.fecha.pack(pady=5)

        tk.Button(
            self,
            text="Enviar Solicitud",
            bg=COLOR_SOLICITAR,
            fg=COLOR_TEXTO,
            command=lambda: self.confirmar_envio(),
        ).pack(pady=10)

    def confirmar_envio(self):
        messagebox.showinfo(
            "Confirmación",
            "Tu solicitud fue registrada con éxito, sigue en el proceso para concluir tu trámite.",
        )
        self.master.mostrar_frame(ResumenSolicitud)


class ResumenSolicitud(BasePantalla):
    def __init__(self, master):
        super().__init__(master, "RESUMEN DE SOLICITUD")
        self.info = tk.Label(self, bg=COLOR_FONDO, fg=COLOR_TEXTO, justify="left")
        self.info.pack(pady=10)
        tk.Button(
            self,
            text="Regresar al Menú",
            command=lambda: master.mostrar_frame(MenuPrincipal),
            bg=COLOR_BOTON,
            fg=COLOR_BLANCO,
        ).pack(pady=10)

    def tkraise(self, *args, **kwargs):
        datos = (
            self.master.datos_estudiante
            if hasattr(self.master, "datos_estudiante")
            else {}
        )
        texto = f"Nombre: {datos.get('Nombre', '')}\nNo. Control: {datos.get('No. Control', '')}\nCarrera: {datos.get('Carrera', '')}\nSemestre: {datos.get('Semestre', '')}\n\nTu solicitud fue registrada correctamente."
        self.info.config(text=texto)
        super().tkraise(*args, **kwargs)


class HistorialConstancias(BasePantalla):
    def __init__(self, master):
        super().__init__(master, "HISTORIAL DE CONSTANCIAS")
        tk.Label(
            self,
            text="Aquí se mostrará el historial del usuario",
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO,
        ).pack(pady=30)


class TutorialUso(BasePantalla):
    def __init__(self, master):
        super().__init__(master, "TUTORIAL DE USO")
        tk.Label(
            self,
            text="Aquí se insertará el video y PDF de ayuda",
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO,
        ).pack(pady=30)


if __name__ == "__main__":
    app = ConstantecApp()
    app.mainloop()
