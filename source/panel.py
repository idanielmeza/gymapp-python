from tkinter import ttk, filedialog, Label, messagebox as ms, Frame,LabelFrame, Tk,Menu,TOP,END,LEFT,RIGHT,CENTER,E,W
from datetime import date
import source.funciones as fn
import source.ventas as Ventas
import source.actualizarMem as act
import source.actualizarEmpleado as empleado
import source.reportesVer as rp
import source.perdidos as perdidos

import main as principal


class Panel:
    def __init__(self, usuario):
        # backgroud = '#0C333D'
        # color = '#F7F7F7'

        # Tk.config(bg='#0C333D', fg = '#F7F7F7')

        self.panel = Tk()
        self.panel.title('Panel FitnessGym Tepeyac')
        self.panel.iconbitmap('img/icon.ico')
        self.panel.resizable(0,0)
        self.panel.config(bg='#fff')
        # self.panel.eval('tk::PlaceWindow . center')
        self.panel.bind('<Key>', self.obtenerPanel)


        self.recepsionista = fn.datos(usuario)

        # Menubar
        menubar = Menu(self.panel)
        self.panel.config(menu=menubar)

        opciones = Menu(menubar, tearoff=0)
        productos = Menu(menubar, tearoff=0)
        reportes = Menu(menubar, tearoff=0)

        productos.add_command(label="Prodcutos", command= lambda: [self.ventas(fn.datos(usuario))] )
        # productos.add_command(label='Agregar Prodcutos',command=self.nuevoProducto)

        opciones.add_command(label="Actualizar contraseña", command=lambda: [
                             self.actualizarCont(usuario) ])

        opciones.add_command(label="Cerrar Sesion", command=lambda: [
                             self.panel.destroy(), principal.Login(), ])

        reportes.add_command(label="Generar Reporte", command= lambda: [self.generarReporte(fn.datos(usuario))] )
        reportes.add_separator()
        reportes.add_command(label="Articulos Perdidos", command= lambda: [self.perdidos(fn.datos(usuario))] )

        menubar.add_cascade(label="Opciones", menu=opciones)
        menubar.add_cascade(label='Productos', menu=productos)
        menubar.add_cascade(label='Reportes', menu=reportes)

# Frame datos empleado

        self.frameEmpleado = LabelFrame(self.panel, bg='#fff')
        self.frameEmpleado.pack(fill='both')

        img = fn.crarImage(fn.imagen(usuario))

        Label(self.frameEmpleado, image=img, bg='#fff').grid(row=0, column=0, rowspan=3)

        self.labelNombre = Label(self.frameEmpleado, text='', font=('Verdana', 12), fg='#B60E0E', bg='#fff')
        self.labelNombre.grid(row=1, column=1, padx=15)
        self.labelNombre['text'] = f'Bienvenido: {fn.datos(usuario)}'

        Label(self.frameEmpleado, text='Vendido :', font=('Verdana', 12), bg='#fff').grid(row=1,column=2)

        self.labelVentas = Label(self.frameEmpleado, text=f'Fecha : {date.today()}', font=('Verdana', 12), fg='#29A840', bg='#fff')
        self.labelVentas.grid(row=1, column=3, padx=5)

# Frame Inferior AGREGAR / BUSCAR / TEXTOS

# FRAME TEXTOS
        self.frameTextos = Frame(self.panel, bg='#fff')
        self.frameTextos.pack(fill='both')

        self.labelVentasTotales = Label(self.frameTextos, text=f'Fecha : {date.today()}', font=('Verdana', 8), fg='#000', bg='#fff')
        self.labelVentasTotales.pack(side=RIGHT)

        self.cUsuarios = Label(self.frameTextos, bg='#fff',font=('Verdana', 8))
        self.cUsuarios.pack(side=LEFT)

        self.frameInferior = Frame(self.panel, bg='#fff')
        self.frameInferior.pack(side=TOP, pady=20, expand=True, fill='both')

# FRAME BUSCAR

        self.frameBuscar = LabelFrame(self.frameInferior, text='Buscar', fg='#B60E0E', font=('Verdana', 10), bg='#fff')
        self.frameBuscar.pack(side=LEFT, padx=30, expand=True, fill='both')

        Label(self.frameBuscar, text='Nombre : ',font=('Verdana', 8), bg='#fff').grid(row=0, column=0)
        self.bnombre = ttk.Entry(self.frameBuscar)
        self.bnombre.grid(row=0, column=1, padx=10)
        self.bnombre.bind('<KeyRelease>', self.buscarNombre)

        Label(self.frameBuscar, text='ID : ', font=('Verdana', 8), bg='#fff').grid(row=1, column=0)
        self.bid = ttk.Entry(self.frameBuscar)
        self.bid.grid(row=1, column=1, pady=5)

        ttk.Button(self.frameBuscar, text='Buscar', command= self.buscar).grid(
            row=2, column=1)

# FRAME AGREGAR
        self.frameAgregar = LabelFrame(
            self.frameInferior, text='Agregar Socios', fg='#B60E0E', font=('Verdana', 10),bg='#fff')
        self.frameAgregar.pack(side=RIGHT, padx=30, expand=True, fill='both')

        Label(self.frameAgregar, text='Nombre : ',
              font=('Verdana', 8), bg='#fff').grid(row=0, column=0, padx=15)
        self.nombre = ttk.Entry(self.frameAgregar)
        self.nombre.grid(row=0, column=1)

        Label(self.frameAgregar, text='Direccion : ',
              font=('Verdana', 8), bg='#fff').grid(row=1, column=0)
        self.direccion = ttk.Entry(self.frameAgregar)
        self.direccion.grid(row=1, column=1)

        Label(self.frameAgregar, text='Telefono : ',
              font=('Verdana', 8), bg='#fff').grid(row=2, column=0)
        self.telefono = ttk.Entry(self.frameAgregar)
        self.telefono.grid(row=2, column=1)

        Label(self.frameAgregar, text='Imagen : ',
              font=('Verdana', 8), bg='#fff').grid(row=3, column=0)
        self.imagen = ttk.Entry(self.frameAgregar)
        self.imagen.grid(row=3, column=1)
        ttk.Button(self.frameAgregar, text='seleccionar',
                   command=self.seleccionar).grid(row=3, column=2, padx=10)

        ttk.Button(self.frameAgregar, text='Agregar', command= self.agregar).grid(
            row=4, column=1, pady=5)

# Frame lista socios
        self.frameUsuarios = Frame(self.panel)
        self.frameUsuarios.pack(side=TOP, fill='both')

        self.tabla = ttk.Treeview(
            self.frameUsuarios, height=10, columns=(1, 2, 3), show='headings')
        self.tabla.pack(fill='both')

        self.tabla.heading(1, text="ID", anchor=CENTER)
        self.tabla.heading(2, text="Nombre", anchor=CENTER)
        self.tabla.heading(3, text="Fecha de expiracion", anchor=CENTER)

# Frame Botones
        self.botonesInferiores = Frame(self.panel)
        self.botonesInferiores.pack(side=TOP)

        ttk.Button(self.botonesInferiores, text='Editar', command= self.actualizarBoton).grid(row=0, column=0)
        
        ttk.Button(self.botonesInferiores, text='Borrar', command= self.borrar).grid(row=0, column=1)

        ttk.Button(self.botonesInferiores, text='Visita', command= lambda: [self.visita(usuario) ]).grid(row=0,column=2)


        self.obtenerTodos()
        self.cantidadUsuarios()

# Mainloop
        self.panel.mainloop()

# Funciones propias

    def seleccionar(self):
        imagen = filedialog.askopenfilename(
            title="Selecciona la foto del socio", initialdir='c:/', filetypes=(("JPG", "*.jpg"),('PNG',"*.png")))
        self.imagen.insert(0, imagen)

    def ventas(self,usuario):
        productos = Ventas.Ventas(usuario)

    def agregar(self):

        if self.nombre.get() and self.direccion.get() and self.telefono.get() != '':
            try:
                int(self.telefono.get())
            except:
                ms.showerror('Error', 'Numero de telefono invalido')
                return
            
            fn.run_query('insert into socios (nombre,direccion,telefono,fecha_inicio,fecha_final) values (?,?,?,?,?)',
            (self.nombre.get(),self.direccion.get(),self.telefono.get(),date.today(),date.today()))
            
            datos = fn.run_query('select id from socios order by id asc')
            
            id = fn.forIn(datos)

            try:
                imagen = fn.crearDireccion(self.imagen.get(), id[0], 'socio')     
            except:
                imagen = './img/default.png'
            
            self.limpiar()

            fn.run_query('update socios set imagen = ? where id = ?',(imagen,id[0]))
            self.obtenerTodos()
            self.actualizar(id[0])
            
        else:
            ms.showinfo('Registro fallido.','Completa los campos correctamente.')

    def actualizar(self,id):
        actualizar = act.Actualizar(id,self.recepsionista)

    def actualizarBoton(self):
        try:
            id = self.tabla.item(self.tabla.selection())['values'][0]
            actualizar = act.Actualizar(id,self.recepsionista)
        except :
            pass  

    def obtenerTodos(self):
        self.ventasHoy()
        self.limpiarTabla()
        datos = fn.run_query('select id,nombre,fecha_final from socios order by fecha_final')
        for (id,nombre,fecha) in datos:
            self.tabla.insert('',0, values = (id,nombre,fecha))

    def limpiarTabla(self):
        productos = self.tabla.get_children()
        for producto in productos:
            self.tabla.delete(producto)
    
    def borrar(self):
    
        try:
            id = self.tabla.item(self.tabla.selection())['values'][0]
            nombre = self.tabla.item(self.tabla.selection())['values'][1]
            resupuesta = ms.askquestion(f'Borrar {nombre}', f'Deseas borrar al socio: {nombre}')
            if resupuesta == 'yes':
                fn.run_query('delete from socios where id = ?',(id,))
                ms.showinfo('Borrado correctamente',f'{nombre} borrado.')
            self.obtenerTodos()
        except :
            pass

    def buscar(self):    
        try:
            usuario = int(self.bid.get())
            self.limpiar()
            self.actualizar(usuario)          
        except :
             ms.showerror('Error','ID no encontrado.')
            
        else:
            ms.showerror('Error','Ingresa ID o Nombre.')
            self.obtenerTodos()
        self.limpiar()
    
    def limpiar(self):

        try:
            self.bid.delete(0,END)
            self.bnombre.delete(0,END)
            self.nombre.delete(0,END)
            self.direccion.delete(0,END)
            self.telefono.delete(0,END)
            self.imagen.delete(0,END)
        except :
            pass

    def actualizarCont(self,id):
        ventana = empleado.Actualizar(id)

    def obtenerPanel(self,e):
        # print(e)
        if e.char == '\x12':
            self.obtenerTodos()
        
        elif e.char =='\x10':
            self.ventas(self.recepsionista)
    
        
        elif e.char == '\x0c':
            self.panel.destroy() 
            principal.Login()

    def buscarNombre(self,e):
        if self.bnombre == '':
            datos = fn.run_query('select id,nombre,fecha_final from socios')
        else: 
            datos = fn.run_query('select id,nombre,fecha_final from socios where nombre like ?',('%'+self.bnombre.get()+'%',))    
        self.limpiarTabla()
        for (id, nombre, fecha) in datos:
            self.tabla.insert('',0, values = (id,nombre,fecha))
        # print(self.bnombre.get())

    def visita(self,recepcionista):
        precios = fn.run_query('select precio from mensualidades where tipo = ?',('visita',))

        for precio in precios:
            pass
        
        
        resupuesta = ms.askquestion('Visita', f'Cobrar ${precio[0]} por visita')
        if resupuesta == 'yes':
            fn.run_query('insert into ventas(recepcionista,producto,cantidad,dinero,fecha) values(?,?,?,?,?)',(fn.datos(recepcionista), 'Visita', '1', precio[0], date.today()))

        self.obtenerTodos()

    def generarReporte(self, recepcionista):
        reporte = rp.Reportes(recepcionista)

    def perdidos(self,usuario):

        perdido = perdidos.Perdidos(usuario)

    def ventasHoy(self):
        total=0
        totalUsuuario=0

        resultado1 =fn.run_query('select dinero,id_transaccion from ventas where recepcionista = ? and fecha = ?',(self.recepsionista, date.today()))
        for (dinero,id) in resultado1:
            totalUsuuario += dinero
            # print(total)

        resultado2 =fn.run_query('select dinero,id_transaccion from ventas where fecha = ?',(date.today(),))
        for (dinero,id) in resultado2:
            total += dinero
            # print(total)

        self.labelVentas['text']= f'${totalUsuuario}'
        self.labelVentasTotales['text']= f'Ventas Totales: ${total}'

    def cantidadUsuarios(self):
        cantidad = fn.run_query(f'select count(fecha_final) from socios where fecha_final >= "{date.today()}"')
        for total in cantidad:
            pass
        self.cUsuarios['text'] = f'Membresias activas: {total[0]}'