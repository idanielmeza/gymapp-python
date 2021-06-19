from tkinter import ttk, Label, messagebox as ms, Frame,Toplevel,TOP,END,RIGHT,CENTER,LEFT
import source.funciones as fn
from datetime import *

class Perdidos:

    def __init__(self, usuario='admin'):
        self.ventana = Toplevel()
        self.ventana.title('Articulos Perdidos')
        self.ventana.resizable(0,0)
        self.ventana.iconbitmap('img/icon.ico')
        self.ventana.config(bg='#fff')

###Formulario

        self.frameFormulario = Frame(self.ventana,bg='#fff')
        self.frameFormulario.pack(side=TOP)

        Label(self.frameFormulario, text='Articulo :',bg='#fff').pack(side=LEFT,padx=10,pady=3)
        self.articulo = ttk.Entry(self.frameFormulario, width=40)
        self.articulo.pack(side=LEFT,padx=10,pady=3)

        ttk.Button(self.frameFormulario, text='Agregar', command=self.agregar).pack(side=LEFT,padx=10,pady=3)

###FRAME TABLA
        self.frameUsuarios = Frame(self.ventana,bg='#fff')
        self.frameUsuarios.pack(side=TOP)

        self.tabla = ttk.Treeview(self.frameUsuarios, height=8 ,columns=(1,2,3,4,5,6), show ='headings')
        self.tabla.pack(side=TOP)
        
        self.tabla.heading(1, text="ID", anchor=CENTER)
        self.tabla.heading(2, text="Nombre", anchor=CENTER)
        self.tabla.heading(3, text="Fecha encontrado", anchor=CENTER)
        self.tabla.heading(4, text="Fecha devolcion", anchor=CENTER)
        self.tabla.heading(5, text="Devuelto por", anchor=CENTER)
        self.tabla.heading(6, text="ID Dueño", anchor=CENTER)

##Frame devovolver
        self.frameDevolver = Frame(self.ventana,bg='#fff')
        self.frameDevolver.pack(side=TOP, fill='both')
    	
        Label(self.frameDevolver, text='Los articulos perdidos se guardan por un maximo de 15 dias sin excepciones.', bg='#fff').pack(side=LEFT,padx=10)

        ttk.Button(self.frameDevolver, text = 'Devuelto', command= lambda: [self.devuelto(usuario)]).pack(side=RIGHT)
        self.idU = ttk.Entry(self.frameDevolver)
        self.idU.pack(side=RIGHT, padx=10,pady=5)
        Label(self.frameDevolver, text='ID Dueño : ',bg='#fff').pack(side=RIGHT)


        self.obtener()
        self.ventana.mainloop()  

###Funciones

    def agregar(self):
        if(self.articulo.get() == ''):
            ms.showwarning('Incompleto', 'Ponle un nombre al articulo')
            return;

        fn.run_query('insert into productos_perdidos(nombre,fecha_encuentro,estado) values(?,?,?)',
        (self.articulo.get(),date.today(),0))
        ms.showinfo('Correcto',f'El articulo {self.articulo.get()} se agrego correctamente.')
        self.articulo.delete(0,END)
        self.obtener()

    def obtener(self):
        self.limpiarTabla()
        datos = fn.run_query("select * from productos_perdidos where fecha_encuentro >= Date('now', '-15 days') order by id asc")
        for (id,nombre,fecha_1, devuelto,fecha_2,dueño,estado) in datos:
            if(devuelto == None):
                devuelto,fecha_2,dueño = '', '', ''

            self.tabla.insert('',0, values = (id,nombre,fecha_1,fecha_2,devuelto,dueño))
        
    def limpiarTabla(self):
        productos = self.tabla.get_children()
        for producto in productos:
            self.tabla.delete(producto)

    def devuelto(self,usuario):
        dueno = self.idU.get()
        try:
            id = self.tabla.item(self.tabla.selection())['values'][0]

            datos = fn.run_query(f'select * from productos_perdidos where id = {id}')

            for (num,nombre,fecha_1, devuelto,fecha_2,dueño,estado) in datos:
                
                if estado == 1:
                    ms.showerror('Error', f'Este articulo se devolvio {fecha_2} por {devuelto}')
                    return

            fn.run_query('update productos_perdidos set devuelto_por = ? , feha_devuelto = ? , dueno = ?, estado = 1 where id = ?',
            (usuario,date.today(),dueno, id))
            ms.showinfo('Correcto','El articulo de ha marcado como devuelto')
            self.idU.delete(0,END)
            self.obtener()

        except :
            pass


# if __name__ == '__main__':
#     app= Perdidos()


