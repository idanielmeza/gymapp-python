from tkinter import ttk, filedialog, Label, messagebox as ms, Frame,LabelFrame, Tk, Toplevel,Menu,TOP,END,CENTER, YES,E
from datetime import date
import source.funciones as fn
import source.actualizarEmpleado as act
import main as principal
import source.reporteVentas as rp
import source.reportesVer as rpVer
import source.ventas as Ventas
import source.nuevoProducto as nP



class PanelAdmin:
    def __init__(self):
        self.panel = Tk()
        self.panel.title('Panel de Administracion')
        self.panel.iconbitmap('img/icon.ico')
        self.panel.resizable(0,0)
        self.panel.config(bg='#fff')

        ### CERRAR SESION MENUBAR

        menubar = Menu(self.panel)
        self.panel.config(menu=menubar)

        opciones = Menu(menubar, tearoff=0)

        opciones.add_command(label="Actualizar contraseña", command= self.actualizarCont)
        opciones.add_command(label="Cerrar Sesion", command= lambda:[self.panel.destroy(),principal.Login(),])

        admin = Menu(menubar, tearoff=0)

        admin.add_command(label="Membresias", command= self.membresias)
        admin.add_command(label="Ventas", command= self.ventas)
        admin.add_command(label="Reportes", command= self.reportesVer)
        admin.add_separator()
        admin.add_command(label="Productos", command= self.productos)
        admin.add_command(label='Agregar Prodcutos',command=self.nuevoProducto)
        admin.add_separator()
        admin.add_command(label='Copia de seguridad', command = self.excel)
     
        menubar.add_cascade(label="Opciones", menu=opciones)
        menubar.add_cascade(label="Gestionar", menu=admin)

#### Frame agregar empleados

        self.panelFrame = LabelFrame(self.panel, text = 'Agregar un nuevo recepcionista',fg='#B60E0E', font=('Verdana',10),bg='#fff')
        self.panelFrame.pack(side=TOP, expand=YES)

        Label(self.panelFrame,text = 'Nombre : ',font=('Verdana',8),bg='#fff').grid(row=0, column =0)
        self.nombre = ttk.Entry(self.panelFrame)
        self.nombre.grid(row=0, column=1, padx=15)

        Label(self.panelFrame,text = 'Usuario : ',font=('Verdana',8),bg='#fff').grid(row=1, column =0)
        self.usuario = ttk.Entry(self.panelFrame)
        self.usuario.grid(row=1, column=1)

        Label(self.panelFrame,text = 'Contraseña : ',font=('Verdana',8),bg='#fff').grid(row=2, column =0)
        self.cont = ttk.Entry(self.panelFrame)
        self.cont.grid(row=2, column=1)
        ttk.Button(self.panelFrame,text='aleatoria', command= self.aleatoria).grid(row=2, column=2)

        Label(self.panelFrame,text = 'Direccion : ',font=('Verdana',8),bg='#fff').grid(row=3, column =0)
        self.direccion = ttk.Entry(self.panelFrame)
        self.direccion.grid(row=3, column=1)
            
        Label(self.panelFrame,text = 'Telefono : ',font=('Verdana',8),bg='#fff').grid(row=4, column =0)
        self.telefono = ttk.Entry(self.panelFrame)
        self.telefono.grid(row=4, column=1)

        Label(self.panelFrame,text = 'Imagen : ',font=('Verdana',8),bg='#fff').grid(row=5, column =0)
        self.imagen = ttk.Entry(self.panelFrame)
        self.imagen.grid(row=5, column=1)
        ttk.Button(self.panelFrame, text = 'seleccionar', command= self.seleccionar).grid(row=5, column=2,padx=10)

        # self.frameTotal = Frame(self.panel, bg='#fff')
        # self.frameTotal.pack(side=RIGHT)

### Frame lista de empleados

        self.frameUsuarios = Frame(self.panel,bg='#fff')
        self.frameUsuarios.pack(side=TOP)

        ttk.Button(self.frameUsuarios, text ='Agregar', command = self.agregar).pack(side=TOP)

        self.usuarios = Label(self.frameUsuarios, bg='#fff',font=('Verdana', 8))
        self.usuarios.pack(side=TOP, anchor=E)

        self.tabla = ttk.Treeview(self.frameUsuarios, height=4 ,columns=(1,2,3,4,5), show ='headings')
        self.tabla.pack(side=TOP)
        
        self.tabla.heading(1, text="Usuario", anchor=CENTER)
        self.tabla.heading(2, text="Nombre", anchor=CENTER)
        self.tabla.heading(3, text="Direccion", anchor=CENTER)
        self.tabla.heading(4, text="Telefono", anchor=CENTER)
        self.tabla.heading(5, text="Fecha de contratacion", anchor=CENTER)

        self.obtenerTodos()

### Frame botones inferiores

        self.botonesInferiores = Frame(self.panel,bg='#fff')
        self.botonesInferiores.pack(side=TOP)
        
        ttk.Button(self.botonesInferiores, text='Editar', command= self.actualizar).grid(row=0, column=0)
        ttk.Button(self.botonesInferiores, text='Borrar', command= self.borrar).grid(row=0, column=1)

        # self.frameTotal = Frame(self.panel, bg='#fff')
        # self.frameTotal.pack(side=TOP, anchor=E)

        # self.usuarios = Label(self.frameTotal, bg='#fff',font=('Verdana', 8))
        # self.usuarios.pack(padx=10)

        self.cantidadUsuarios()

        self.panel.mainloop()

### Funciones propias
    def aleatoria(self):
        contra = fn.contraAleatoria()

        self.cont.delete(0,END)
        self.cont.insert(0,contra)

    def aleatoria2(self):
        contra = fn.contraAleatoria()

        self.nuevaContra.delete(0,END)
        self.nuevaContraC.delete(0,END)
        self.nuevaContra.insert(0,contra)
        self.nuevaContraC.insert(0,contra)

    def actualizar(self):
        try:
            ventana = act.Actualizar(self.tabla.item(self.tabla.selection())['values'][0])
        except :
            pass

    def seleccionar(self):
        imagen = filedialog.askopenfilename(title = "Selecciona la foto del recepcionista", initialdir = 'c:/', filetypes=(("JPG", "*.jpg"),('PNG',"*.png")))
        self.imagen.insert(0,imagen)
    
    def agregar(self):
        if self.usuario.get() or self.cont.get() or self.nombre.get() or self.direccion.get() or self.telefono.get() or self.imagen.get() != '':

            fn.run_query('insert into empleados (usuario,contraseña,nombre,direccion,telefono,imagen,fecha_inicio) values (?,?,?,?,?,?,?)',
            (self.usuario.get(),
            self.cont.get(),
            self.nombre.get(),
            self.direccion.get(),
            self.telefono.get(),
            fn.crearDireccion(self.imagen.get(), self.usuario.get(), 'empleado'),
            date.today()))

            ms.showinfo('Ha agregado un nuevo empleado',f'{self.nombre.get()} agregado correctamente')
            self.limpar()
            self.obtenerTodos()
        
        else:
            ms.showerror('Error','Llena todos los campos correctamente')
    
    def limpar(self):

        self.usuario.delete(0,END)
        self.cont.delete(0,END)
        self.nombre.delete(0,END)
        self.direccion.delete(0,END)
        self.telefono.delete(0,END)
        self.imagen.delete(0,END)

    def obtenerTodos(self):
        self.limpiarTabla()
        datos = fn.run_query('select usuario,nombre,direccion,telefono,fecha_inicio from empleados')
        for (usuario,nombre,direccion, telefono,fecha) in datos:
            self.tabla.insert('',0, values = (usuario,nombre,direccion,telefono,fecha))

    def limpiarTabla(self):
        productos = self.tabla.get_children()
        for producto in productos:
            self.tabla.delete(producto)
    
    def borrar(self):
        try:
            id = self.tabla.item(self.tabla.selection())['values'][0]
            nombre = self.tabla.item(self.tabla.selection())['values'][1]
            resupuesta = ms.askquestion('Confirmar',f'Se borrara: {nombre}.')
            if resupuesta == 'yes':
                fn.run_query('delete from empleados where usuario = ?',(id,))
                self.obtenerTodos()
        except :
            pass
    
    def actualizarCont(self):
        self.contra = Toplevel()
        self.contra.iconbitmap('img/icon.ico')
        self.contra.title('Act contraseña')

        Label(self.contra, text = 'Nueva contraseña : ').grid(row=0, column=0)
        self.nuevaContra= ttk.Entry(self.contra)
        self.nuevaContra.grid(row=0,column=1)
        ttk.Button(self.contra, text='aleatoria', command= self.aleatoria2).grid(row=0, column=2)

        Label(self.contra, text = 'Confirmar contraseña : ').grid(row=1, column=0)
        self.nuevaContraC= ttk.Entry(self.contra)
        self.nuevaContraC.grid(row=1,column=1, padx=5)

        ttk.Button(self.contra, text='Guardar Cambios', command= self.actualizarContra).grid(row=2, column=1, pady=5)

    def actualizarContra(self):
        if self.nuevaContra.get() == self.nuevaContraC.get():
            fn.run_query('update administracion set contraseña = ? where usuario = ?',(self.nuevaContra.get(),'admin'))
            ms.showinfo('Actualizada','La contraseña se actualizo.')
            self.contra.destroy()
        else:
            ms.showerror('Error','Las contraseñas no coinciden.')

    def membresias(self):
        precios = fn.run_query('select precio from mensualidades order by precio desc')

        precio = precios.fetchall()
        
        self.actMem = Toplevel()
        self.actMem.title('Actualizar')
        self.actMem.iconbitmap('img/icon.ico')
        self.actMem.resizable(0,0)
        self.actMem.config(bg='#fff')

        Label(self.actMem,text = 'Mes : ', bg='#fff').grid(row=0, column=0, padx=5)
        self.mes = ttk.Entry(self.actMem)
        self.mes.grid(row=0 ,column = 1)
        self.mes.insert(0,precio[0])

        Label(self.actMem,text = '15 Dias : ', bg='#fff').grid(row=1, column=0)
        self.quincena = ttk.Entry(self.actMem)
        self.quincena.grid(row=1 ,column = 1)
        self.quincena.insert(0,precio[1])

        Label(self.actMem,text = '7 Dias : ', bg='#fff').grid(row=2, column=0)
        self.semana = ttk.Entry(self.actMem)
        self.semana.grid(row=2, column = 1)
        self.semana.insert(0,precio[2])

        Label(self.actMem,text = 'Visita : ', bg='#fff').grid(row=3, column=0)
        self.visita = ttk.Entry(self.actMem)
        self.visita.grid(row=3 ,column = 1, padx=10)
        self.visita.insert(0,precio[3])

        ttk.Button(self.actMem, text='Guardar Cambios', command= self.actualizarMembresias).grid(row=4,column=1, pady=8)

        self.actMem.mainloop()

    def actualizarMembresias(self): 
        try:
            float(self.quincena.get())
            float(self.mes.get())
            float(self.semana.get())
            float(self.visita.get())
        except:
            ms.showerror('Error', 'Ingresa precios validos')
            return

        fn.run_query('update mensualidades set precio = ? where tipo = ?',(self.mes.get(),'mes'))
        fn.run_query('update mensualidades set precio = ? where tipo = ?',(self.quincena.get(),'quincena'))
        fn.run_query('update mensualidades set precio = ? where tipo = ?',(self.semana.get(),'semana'))
        fn.run_query('update mensualidades set precio = ? where tipo = ?',(self.visita.get(),'visita'))
        
        ms.showinfo('Correcto', 'Los precios se actualizaron correctamente.')

        self.actMem.destroy()

    def ventas(self):
        ventas = rp.Reportes()

    def reportesVer(self):
        verRp = rpVer.Reportes()

    def productos(self):
        productos = Ventas.Ventas()

    def nuevoProducto(self):

        nuevo = nP.ventaProducto()

    def excel(self):
        fn.excel()
        ms.showinfo('Completado', 'Tu copia de seguridad ha sido creada correctamente guardala en un lugar seguro.')

    def cantidadUsuarios(self):
        cantidad = fn.run_query(f'select count(fecha_final) from socios where fecha_final >= "{date.today()}"')
        for total in cantidad:
            pass
        self.usuarios['text'] = f'Membresias activas: {total[0]}'


# if __name__ == '__main__':
#     PanelAdmin()