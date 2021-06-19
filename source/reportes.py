from tkinter import ttk,Label, messagebox as ms,Toplevel,END,BUTTON,LEFT
from datetime import date
import source.funciones as fn


class Reporte:
    def __init__(self, usuario):

        # self.panel = Tk()
        self.panel = Toplevel()
        self.panel.title('Reportes')
        self.panel.iconbitmap('img/icon.ico')
        self.panel.config(bg='#fff')

        Label(self.panel, text='Titulo',font=('Verdana', 10)).pack(side=LEFT)
        self.titulo = ttk.Entry(self.panel)
        self.titulo.pack(side=LEFT)

        Label(self.panel, text='Descripcion', font=('Verdana', 10)).pack(side=LEFT)
        self.description = ttk.Text(self.panel, height=10, width=50)
        self.description.pack(side=LEFT)

        ttk.Button(self.panel, text='Reportar',command= lambda: [self.crearReporte(usuario)]).pack(side=BUTTON)
    
    
        self.panel.mainloop()

    def crearReporte(self, usuario):
        if(self.titulo.get() == '' or self.description.get('1.0','end-1c') == ''):
            ms.showerror('Error', 'Completa todos los campos')
            return;

        fn.run_query('insert into reportes(creador,titulo,contenido,fecha,estado) values(?,?,?,?,?)',
        (usuario, self.titulo.get(), self.description.get('1.0','end-1c'),date.today(), 0))

        ms.showinfo('Reporte generado', f'El reporte {self.titulo.get()} ha sido generado correctamente.')

        self.titulo.delete(0,END)
        self.description.delete('1.0','end-1c')

        self.panel.destroy()

# if __name__ == '__main__':
#     app= Reporte()