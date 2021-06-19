from tkinter import ttk, Label, messagebox as ms, Frame,Toplevel,TOP,END,RIGHT,CENTER
import source.funciones as fn
from datetime import date

class Ventas:

    def __init__(self,recepcionista='admin'):
        self.panel = Toplevel()
        self.panel.title('Productos')
        self.panel.iconbitmap('img/icon.ico')
        self.panel.config(bg='#fff')
        self.panel.resizable(0,0)

### Lista productos

        self.recepcionista = recepcionista

        self.frameLista = Frame(self.panel,bg='#fff')
        self.frameLista.pack(pady=5)

        self.tabla = ttk.Treeview(self.frameLista, height=10 ,columns=(1,2,3,4), show ='headings')
        self.tabla.grid(row=0, column=0, columnspan=6)
        
        self.tabla.heading(1, text="ID", anchor=CENTER)
        self.tabla.heading(2, text="Nombre", anchor=CENTER)
        self.tabla.heading(3, text="Disponibles", anchor=CENTER)
        self.tabla.heading(4, text="Precio", anchor=CENTER)

        self.obtenerProductos(self.recepcionista)

        self.btnActuaizar = ttk.Button(self.frameLista, text='Editar', command= self.actualizar)
        self.btnActuaizar.grid(row=1,column=2)
        self.btnBorrar= ttk.Button(self.frameLista, text='Borrar', command= self.borrar)
        self.btnBorrar.grid(row=1,column=3)
        
### Vender

        self.frameUtilidad =Frame(self.panel,bg='#fff')
        self.frameUtilidad.pack(expand = True, fill='both',side=TOP, pady=10)

        ttk.Button(self.frameUtilidad, text='Venta', command= lambda: [self.venderProducto(recepcionista)] ).pack(side=RIGHT, padx=5)
        self.cantidad = ttk.Entry(self.frameUtilidad)
        self.cantidad.pack(side=RIGHT)
        self.cantidad.insert(0,'1')

        Label(self.frameUtilidad, text='Cantidad : ',font=('Verdana',10),bg='#fff').pack(side=RIGHT, padx=5)

        self.desactivarActualizar(recepcionista)

        self.panel.mainloop()

### Actualizar Productos

    def desactivarActualizar(self, usuario):
        if usuario != 'admin':
            self.btnActuaizar.destroy()
            self.btnBorrar.destroy()
        else:
            self.frameUtilidad.destroy()

    def actualizar(self):
        try:
            nombre = self.tabla.item(self.tabla.selection())['values'][1]
            cantidad = self.tabla.item(self.tabla.selection())['values'][2]
            precio = self.tabla.item(self.tabla.selection())['values'][3]
            id = self.tabla.item(self.tabla.selection())['values'][0]

            self.ventanaActualizar = Toplevel()
            self.ventanaActualizar.title(f'Actualizar {nombre}')
            self.ventanaActualizar.iconbitmap('img/icon.ico')
            self.ventanaActualizar.config(bg='#fff')

            Label(self.ventanaActualizar, text = f'{nombre}', font=('Verdana',12), fg='#B60E0E', bg='#fff').grid(row=0, column=0, columnspan=2)

            Label(self.ventanaActualizar, text = 'Cantidad : ', bg='#fff').grid(row=1, column=0)
            self.nCantidad = ttk.Entry(self.ventanaActualizar)
            self.nCantidad.grid(row=1,column=1)
            self.nCantidad.insert(0,cantidad)

            Label(self.ventanaActualizar, text = 'Precio : ', bg='#fff').grid(row=2, column=0)
            self.nPrecio = ttk.Entry(self.ventanaActualizar)
            self.nPrecio.grid(row=2,column=1, padx=10)
            self.nPrecio.insert(0,precio)

            ttk.Button(self.ventanaActualizar, text ='Guardar Cambios', command= lambda: [self.funcionActualizar(id,nombre)]).grid(row=3, column=1, pady=5)

        except :
            pass
    
    def funcionActualizar(self,id,nombre):

        try:
            int(self.nCantidad.get())
            float(self.nPrecio.get())
        except :
            ms.showerror('Error', 'Ingresa cantidades validas')
            return

        fn.run_query('update productos set cantidad = ? , precio = ? where id = ?',
        (int(self.nCantidad.get()), float(self.nPrecio.get()), id))
        ms.showinfo('Actualizado',f'{nombre} actualizado.')
        self.obtenerProductos(self.recepcionista)
        self.ventanaActualizar.destroy()

### Funciones 
    def obtenerProductos(self, recepcionista):
        self.limpiarProductos()
        if recepcionista == 'admin':
            datos = fn.run_query('select id,nombre,cantidad,precio from productos')
        else:
            datos = fn.run_query('select id,nombre,cantidad,precio from productos where cantidad > 0')
        for (id,nombre,cantidad,precio) in datos:
            self.tabla.insert('',0, values = (id,nombre,cantidad,precio))

    def limpiarProductos(self):
        productos = self.tabla.get_children()
        for producto in productos:
            self.tabla.delete(producto)

    def borrar(self):
        try:
            nombre = self.tabla.item(self.tabla.selection())['values'][0]
            fn.run_query('delete from productos where nombre = ?',(nombre,))
            ms.showinfo('Borrado',f'Se ha borrado {nombre}')
            self.obtenerProductos()
        except:
            pass
            
    def venderProducto(self, recepcionista):
        try:
            id  = self.tabla.item(self.tabla.selection())['values'][0]
            nombre = self.tabla.item(self.tabla.selection())['values'][1]
            cantidad = self.tabla.item(self.tabla.selection())['values'][2]
            precio = self.tabla.item(self.tabla.selection())['values'][3]
            vender = int(self.cantidad.get())

            if cantidad-vender < 0:
                ms.showerror('Venta incompleta','No hay productos suficientes.')

            else:
                resupuesta = ms.askquestion(f'Venta', f'Cobrar ${float(vender)*float(precio)}, por {vender} {nombre}.')
                if resupuesta == 'yes':

                    fn.run_query('update productos set cantidad = ? where id = ?',
                    (cantidad-vender,id))
                    
                    self.obtenerProductos(recepcionista)

                    fn.run_query('insert into ventas(recepcionista,producto,cantidad,dinero,fecha) values(?,?,?,?,?)',(recepcionista, nombre,vender,float(vender)*float(precio), date.today()))
                
            
            self.cantidad.delete(0,END)
            self.cantidad.insert(0,1)
            
        except :
            ms.showerror('Venta incompleta','Seleccione un producto')