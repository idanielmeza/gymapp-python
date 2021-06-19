from tkinter import Tk, Label, ttk, END
from tkinter import messagebox as ms
import source.funciones as fn
import source.panel as panel
import source.panelAdmin as panelAdmin

class Login:

    def __init__(self):
        # backgroud = '#0C333D'
        # color = '#F7F7F7

        # configuraciones = "bg='#0C333D', fg='#F7F7F7'"

        self.ventana = Tk()
        # self.ventana.eval(f'tk::PlaceWindow {self.ventana} center')
        self.ventana.title('Fitness Gym Tepeyac')
        self.ventana.resizable(0,0)
        self.ventana.iconbitmap('img/icon.ico')
        self.ventana.config(bg='#fff')
        w = self.ventana.winfo_reqwidth()
        h = self.ventana.winfo_reqheight()
        ws = self.ventana.winfo_screenwidth()
        hs = self.ventana.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.ventana.geometry('+%d+%d' % (x, y))



        img = fn.crearImage('img/banner.jpg')

        Label(image = img).grid(row=0, column=0, columnspan=2)

        Label(text='Usuario : ', font=('Constantia',12), bg='#fff').grid(row=1 ,column=0)
        self.nombreUsuario = ttk.Entry()
        self.nombreUsuario.grid(row=1, column=1,pady=10)
        self.nombreUsuario.focus()

        Label(text='Contraseña : ', font=('Constantia',12), bg='#fff').grid(row=2 ,column=0,pady=5,padx=5)
        self.contraseñaUsuario = ttk.Entry(show='*')
        self.contraseñaUsuario.grid(row=2, column=1)

        ttk.Button(text='Entrar',command = self.splash).grid(row=3, column=1)

        self.ventana.mainloop()

    def splash(self):
        self.ventana.iconify()
        self.splash = Tk()
        self.splash.overrideredirect(True)
        self.splash.eval(f'tk::PlaceWindow {self.ventana} center')
        self.splash.config(bg='#fff')
        Label(self.splash, text='Conectando...', font=('Century',15), bg='#fff').pack(padx=10)
        self.splash.after(1000,lambda:[self.validacion([self.nombreUsuario.get(),self.contraseñaUsuario.get()])])

        self.splash.mainloop()

    def validacion(self,datos=[]):
        self.splash.destroy()
        datosEmpleado = fn.run_query('select * from empleados where usuario = ? and contraseña = ?',
        (datos[0],datos[1]))

        datosAdmin = fn.run_query('select * from administracion where usuario = ? and contraseña = ?',
        (datos[0],datos[1]))

        if datosEmpleado.fetchall():
            self.ventana.destroy()
            # nuevoPanel =panel.Panel(datos[0])
            
            panel.Panel(datos[0])

        elif datosAdmin.fetchall():
            self.ventana.destroy()
            
            panelAdmin.PanelAdmin()
                 
        else:
            ms.showerror('Error','Verifica los datos')
            self.ventana.deiconify()
            self.nombreUsuario.delete(0,END)
            self.contraseñaUsuario.delete(0,END)
            self.nombreUsuario.focus()
            
if __name__ == '__main__':
    login = Login()