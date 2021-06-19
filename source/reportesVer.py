from tkinter import ttk, Label, messagebox as ms, Frame, Toplevel,TOP,END,LEFT,CENTER
import source.funciones as fn
from datetime import date


class Reportes:

    def __init__(self,usuario='admin'):
        self.panel = Toplevel()
        # self.panel.wm_title('Reportes')
        self.panel.title('Reportes')
        self.panel.iconbitmap('img/icon.ico')
        self.panel.config(bg='#fff')

        self.frameInferior = Frame(self.panel,bg='#fff')
        self.frameInferior.pack(side=TOP, pady=10)

        Label(self.frameInferior, text='Titulo',font=('Verdana', 10),bg='#fff').pack(side=LEFT,padx=10)
        self.titulo = ttk.Entry(self.frameInferior)
        self.titulo.pack(side=LEFT,padx=10)

        Label(self.frameInferior, text='Descripcion', font=('Verdana', 10),bg='#fff').pack(side=LEFT,padx=10)
        self.description = ttk.Entry(self.frameInferior,width=100)
        self.description.pack(side=LEFT,padx=10)

        ttk.Button(self.frameInferior, text='Reportar',command= lambda: [self.crearReporte(usuario)]).pack(side=LEFT,padx=10,pady=3)

###Frame Reportes
        self.frameUsuarios = Frame(self.panel,bg='#fff')
        self.frameUsuarios.pack(side=TOP)

        self.tabla = ttk.Treeview(self.frameUsuarios, height=4 ,columns=(1,2,3,4,5,6), show ='headings')
        self.tabla.pack(side=TOP)
        
        self.tabla.heading(1, text="ID", anchor=CENTER)
        self.tabla.heading(2, text="Estado", anchor=CENTER)
        self.tabla.heading(3, text="Generado Por", anchor=CENTER)
        self.tabla.heading(4, text="Fecha", anchor=CENTER)
        self.tabla.heading(5, text="Titulo", anchor=CENTER)
        self.tabla.heading(6, text="Contenido", anchor=CENTER)

        self.frameBotones = Frame(self.panel,bg='#fff')
        self.frameBotones.pack(side=TOP)

        ttk.Button(self.frameBotones, text ='Resuelto', command= self.resolver).pack(side=LEFT)
        ttk.Button(self.frameBotones, text ='Ver Todos', command= self.obtenerTodos).pack(side=LEFT)

        self.obtener()

        self.actVentana(usuario)

        self.panel.mainloop()

###Fucniones

    def obtener(self):
        self.limpiarTabla()

        datos = fn.run_query('select * from reportes where estado = 0')
        for (id,por,titulo, contenido,fecha,estado) in datos:
            if(estado == 0):
                estado = 'Sin Resolver'
            else:
                estado = 'Resuelto'
            self.tabla.insert('',0, values = (id,estado,por,fecha,titulo,contenido))

    def obtenerTodos(self):
        self.limpiarTabla()

        datos = fn.run_query('select * from reportes')
        for (id,por,titulo, contenido,fecha,estado) in datos:
            if(estado == 0):
                estado = 'Sin Resolver'
            else:
                estado = 'Resuelto'
            self.tabla.insert('',0, values = (id,estado,por,fecha,titulo,contenido))

    def limpiarTabla(self):
    
        productos = self.tabla.get_children()
        for producto in productos:
            self.tabla.delete(producto)

    def resolver(self):
        try:
            id = self.tabla.item(self.tabla.selection())['values'][0]
            fn.run_query('update reportes set estado = 1 where id = ?',(id,))
            ms.showinfo('Actualizado', f"El reporte {self.tabla.item(self.tabla.selection())['values'][3]} ha sido solucionado.")

            self.obtener()

        except :
            pass

    def crearReporte(self, usuario):
        if(self.titulo.get() == '' or self.description.get() == ''):
            ms.showerror('Error', 'Completa todos los campos')
            return;

        fn.run_query('insert into reportes(creador,titulo,contenido,fecha,estado) values(?,?,?,?,?)',
        (usuario, self.titulo.get(), self.description.get(),date.today(), 0))

        ms.showinfo('Reporte generado', f'El reporte {self.titulo.get()} ha sido generado correctamente.')

        self.titulo.delete(0,END)
        self.description.delete(0,END)

        self.obtener()

    def actVentana(self,usuario):
        if usuario != 'admin':
            self.frameBotones.destroy()
        else:
            self.frameInferior.destroy()
# if __name__ == '__main__':
#     app = Reportes()