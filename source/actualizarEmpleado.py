from tkinter import ttk,Label, messagebox as ms,Toplevel,END, DISABLED
import source.funciones as fn


class Actualizar:

    def __init__(self, id):
        query = fn.run_query('select * from empleados where usuario = ?',(id,))

        for dato in query:
            pass
        

        self.ventanaActualizar = Toplevel()
        self.ventanaActualizar.title(f'{dato[2]}')
        self.ventanaActualizar.iconbitmap('img/icon.ico')
        self.ventanaActualizar.config(bg='#fff')

        img = fn.crarImage2(dato[5])

        Label(self.ventanaActualizar, image=img).grid(
            row=0, column=0, columnspan=3)

        Label(self.ventanaActualizar, text='Usuario : ',bg='#fff').grid(
            row=1, column=0)
        self.nUsuario = ttk.Entry(self.ventanaActualizar)
        self.nUsuario.grid(row=1, column=1)

        Label(self.ventanaActualizar, text='Contraseña : ',bg='#fff').grid(
            row=2, column=0)
        self.nCont = ttk.Entry(self.ventanaActualizar)
        self.nCont.grid(row=2, column=1)
        ttk.Button(self.ventanaActualizar, text='aleatoria', command= self.contAleatoria).grid(row=2, column=2)

        Label(self.ventanaActualizar, text='Nombre : ',bg='#fff').grid(row=3, column=0)
        self.nNombre = ttk.Entry(self.ventanaActualizar)
        self.nNombre.grid(row=3, column=1)

        Label(self.ventanaActualizar, text='Direccion : ',bg='#fff').grid(
            row=4, column=0)
        self.nDireccion = ttk.Entry(self.ventanaActualizar)
        self.nDireccion.grid(row=4, column=1)

        Label(self.ventanaActualizar, text='Telefono : ',bg='#fff').grid(
            row=5, column=0)
        self.nTelefono = ttk.Entry(self.ventanaActualizar)
        self.nTelefono.grid(row=5, column=1, padx=10)

        ttk.Button(self.ventanaActualizar, text='Guardar Cambios', command=lambda: [
            self.funcionActualizar(dato[0])]).grid(row=6, column=1, pady=5)

        self.inserterDatos(dato)

        self.ventanaActualizar.mainloop()

    def contAleatoria(self):
        cont = fn.contraAleatoria()

        self.nCont.delete(0,END)
        self.nCont.insert(0,cont)

    def inserterDatos(self,datos):

        self.nUsuario.insert(0,datos[0])
        self.nUsuario.config(state= DISABLED)
        self.nCont.insert(0,datos[1])
        self.nNombre.insert(0,datos[2])
        self.nDireccion.insert(0,datos[3])
        self.nTelefono.insert(0,datos[4])       

    def funcionActualizar(self,id):
        
        fn.run_query('update empleados set contraseña = ? , nombre = ? , direccion = ? , telefono = ? where usuario = ?',
        (self.nCont.get(),self.nNombre.get(),self.nDireccion.get(),self.nTelefono.get(),id))
        ms.showinfo('Actualizado',f'{self.nNombre.get()} actualizado.')
        self.ventanaActualizar.destroy()