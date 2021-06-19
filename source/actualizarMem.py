from tkinter import ttk, filedialog, Label, messagebox as ms, Frame,LabelFrame,Toplevel,TOP,LEFT,DISABLED
import source.funciones as fn

from datetime import *

class Actualizar:
    
    def __init__(self,id,recepcionista):
        
        self.recepcionista = recepcionista

        query = fn.run_query('select * from socios where id = ?',(id,))

        datos = fn.forIn(query)

        self.ventanaActualizar = Toplevel()
        self.ventanaActualizar.title(f'{datos[1]}')
        self.ventanaActualizar.iconbitmap('img/icon.ico')
        self.ventanaActualizar.resizable(0,0)
        self.ventanaActualizar.config(bg='#fff')

        self.imagenLabel = LabelFrame(self.ventanaActualizar,bg='#fff')
        self.imagenLabel.pack(side=TOP)

        img= fn.crarImage2(datos[4])

        Label(self.imagenLabel, image=img,bg='#fff').grid(row = 0, column = 0, columnspan= 3)

        self.ventanaActualizarArriba = Frame(self.ventanaActualizar,bg='#fff')
        self.ventanaActualizarArriba.pack(side=TOP)
        
        self.expiracion = Label(self.ventanaActualizarArriba, text =f'Fecha de expiracion : {datos[6]}',font=('Verdana',11), fg='#B60E0E',bg='#fff', justify='center')
        self.expiracion.grid(row=0, column=0, columnspan=3, pady=15)


        Label(self.ventanaActualizarArriba, text = 'ID : ',bg='#fff').grid(row=2, column=0)
        self.id = ttk.Entry(self.ventanaActualizarArriba)
        self.id.grid(row=2,column=1)
        self.id.insert(0,str(datos[0]))
        self.id.config(state=DISABLED)

        Label(self.ventanaActualizarArriba, text = 'Nombre : ',bg='#fff').grid(row=3, column=0)
        self.nombre = ttk.Entry(self.ventanaActualizarArriba)
        self.nombre.grid(row=3,column=1)
        self.nombre.insert(0,datos[1])

        Label(self.ventanaActualizarArriba, text = 'Direccion : ',bg='#fff').grid(row=4, column=0)
        self.direccion = ttk.Entry(self.ventanaActualizarArriba)
        self.direccion.grid(row=4,column=1)
        self.direccion.insert(0,datos[2])

        Label(self.ventanaActualizarArriba, text = 'Telefono : ',bg='#fff').grid(row=5, column=0)
        self.telefono = ttk.Entry(self.ventanaActualizarArriba)
        self.telefono.grid(row=5,column=1)
        self.telefono.insert(0,datos[3])

        self.imagenLabel = Label(self.ventanaActualizarArriba, text='Imagen : ',bg='#fff')
        self.imagenLabel.grid(row=6,column=0)
        self.imagenEntry = ttk.Entry(self.ventanaActualizarArriba)
        self.imagenEntry.grid(row=6,column=1)
        self.imagenBtn = ttk.Button(self.ventanaActualizarArriba, text='Seleccionar', command=self.seleccionar)
        self.imagenBtn.grid(row=6, column=2)

        Label(self.ventanaActualizarArriba, text = 'Socio desde : ',bg='#fff').grid(row=7, column=0)
        self.desde = ttk.Entry(self.ventanaActualizarArriba)
        self.desde.grid(row=7,column=1, padx=8)
        self.desde.insert(0,datos[5])
        self.desde.config(state=DISABLED)


        ttk.Button(self.ventanaActualizarArriba, text='Guardar Cambios', command= lambda:[self.actualizar(id)]).grid(row=8, column=1, pady=5)

        self.meses = ttk.Entry(self.ventanaActualizarArriba)
        self.meses.grid(row=9, column=1)
        self.meses.insert(0,1)
        ttk.Button(self.ventanaActualizarArriba, text='Meses', command= lambda:[self.membresia(datos[0],
        f'"+{int(self.meses.get())} months"',
        datos[6])]).grid(row=9, column=2)  

        self.ventanaActualizarAbajo = Frame(self.ventanaActualizar,bg='#fff')
        self.ventanaActualizarAbajo.pack(side=TOP)

        ttk.Button(self.ventanaActualizarAbajo, text='Semana',command= lambda:[self.membresia(datos[0],
        '"+7 day"',
        datos[6])]).pack(side=LEFT) 

        ttk.Button(self.ventanaActualizarAbajo, text='15 dias', command= lambda:[self.membresia(datos[0],
        '"+15 day"',
        datos[6])]).pack(side=LEFT, pady=5)

        self.expirado(datos[6])
        self.check = 1

        if(datos[4] != './img/default.png'):
            self.noImagen()
            self.check = 0


        self.ventanaActualizar.mainloop()

    def actualizar(self,id):
        if(self.check != 0):
            try:
                imagen = fn.crearDireccion(self.imagenEntry.get(), id, 'socio')     
            except:
                imagen = './img/default.png'
            
            fn.run_query('update socios set nombre = ?, direccion = ?, telefono = ?, imagen = ? where id = ?',
            (self.nombre.get(),self.direccion.get(),self.telefono.get(), imagen ,id))

        else:
            fn.run_query('update socios set nombre = ?, direccion = ?, telefono = ? where id = ?',
            (self.nombre.get(),self.direccion.get(),self.telefono.get(),id))
            
        ms.showinfo('Usuario Actualizado',f'{self.nombre.get()} actualizado.')
        self.ventanaActualizar.destroy()

    def expirado(self,fecha):
        if fecha < str(date.today()):
            self.expiracion.config(text='Membresia Expirada')
    
    def membresia(self,id,texto,fecha):
        precios = fn.run_query('select precio from mensualidades order by precio desc')

        precio = precios.fetchall()

        if fecha < str(date.today()):
            fn.run_query('update socios set fecha_final = ? where id = ?',
            (date.today(),id))
        
        fn.run_query(f'update socios set fecha_final = date(fecha_final, {texto}) where id =?',
        (id,))

        if(texto == '"+15 day"'):
            resupuesta = ms.askquestion('Actualizacion de membresia',f'La membresia de {self.nombre.get()} ha sera actualizada, cobrar ${sum(precio[1])} por 15 dias.')
            if resupuesta == 'yes':
                fn.run_query('insert into ventas(recepcionista,producto,cantidad,dinero,fecha) values(?,?,?,?,?)',
                (self.recepcionista,'Quincena','1',sum(precio[1]),date.today()))
                self.ventanaActualizar.destroy()

        elif(texto == '"+7 day"'):
            resupuesta = ms.askquestion('Actualizacion de membresia',f'La membresia de {self.nombre.get()} ha sera actualizada, cobrar ${sum(precio[1])} por 7 dias.')
            if resupuesta == 'yes':
                fn.run_query('insert into ventas(recepcionista,producto,cantidad,dinero,fecha) values(?,?,?,?,?)',
                (self.recepcionista,'Semana','1',sum(precio[2]),date.today()))
                self.ventanaActualizar.destroy()

        else:
            if self.meses.get() =='1':
                resupuesta = ms.askquestion('Actualizacion de membresia',f'La membresia de {self.nombre.get()} sera actualizada, cobrar ${sum(precio[0])} por 1 mes.')
            else:
                resupuesta = ms.askquestion('Actualizacion de membresia',f'La membresia de {self.nombre.get()} sera actualizada, cobrar ${sum(precio[0]) * int(self.meses.get())} por {self.meses.get()} meses.')
            
            if resupuesta == 'yes':
                fn.run_query('insert into ventas(recepcionista,producto,cantidad,dinero,fecha) values(?,?,?,?,?)',
                (self.recepcionista,'Mensualidad',self.meses.get(),
                sum(precio[0]) * int(self.meses.get())
                ,date.today()))
                self.ventanaActualizar.destroy()

    def noImagen(self):
        self.imagenBtn.destroy()
        self.imagenLabel.destroy()
        self.imagenEntry.destroy()

    def seleccionar(self):
        imagen = filedialog.askopenfilename(
            title="Selecciona la foto del socio", initialdir='c:/', filetypes=(("JPG", "*.jpg"),('PNG',"*.png")))
        self.imagenEntry.insert(0, imagen)