from os import execlpe
from tkinter import ttk,Label, messagebox as ms,Toplevel
import source.funciones as fn

class ventaProducto:

    def __init__(self):
        self.nuevoProducto = Toplevel()
        self.nuevoProducto.title('Agrega un nuevo producto')
        self.nuevoProducto.iconbitmap('img/icon.ico')
        self.nuevoProducto.config( bg='#fff')

        Label(self.nuevoProducto,text='Nombre : ', bg='#fff').grid(row=0, column=0)
        self.nombreProducto = ttk.Entry(self.nuevoProducto)
        self.nombreProducto.grid(row=0, column=1, pady=5, padx=5)
        self.nombreProducto.focus()

        Label(self.nuevoProducto, text='Cantidad : ', bg='#fff').grid(row=1,column=0)
        self.cantidadProducto = ttk.Entry(self.nuevoProducto)
        self.cantidadProducto.grid(row=1,column=1, padx=5)

        Label(self.nuevoProducto, text='Precio : ', bg='#fff').grid(row=2,column=0)
        self.precioProducto = ttk.Entry(self.nuevoProducto)
        self.precioProducto.grid(row=2,column=1, padx=5)

        ttk.Button(self.nuevoProducto, text='Agregar',
        command= lambda:[self.crearProducto(self.nombreProducto.get(), 
        self.cantidadProducto.get(),
        self.precioProducto.get())]).grid(row=3, column=1,pady=5)

        self.nuevoProducto.mainloop()

    def crearProducto(self, nombre, cantidad,precio):
        try:
            cantidad = int(cantidad)
            precio = float(precio)
        except:
            ms.showerror('Error', 'Ingresa cantidades validas')
            return

        fn.run_query('insert into productos(nombre,cantidad,precio) values(?,?,?)',(nombre,cantidad,precio))
        ms.showinfo('Producto agregado',f'Se han agregado {cantidad} {nombre} con el precio ${precio}')
        self.nuevoProducto.destroy()