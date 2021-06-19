from tkinter import ttk, Label, Frame,Toplevel,TOP,END,RIGHT,CENTER,DISABLED,NORMAL
import source.funciones as fn
from tkcalendar import DateEntry
from datetime import *
from openpyxl import Workbook
from os import startfile,remove
from shutil import move

class Reportes:

    def __init__(self):
        self.reportes = Toplevel()
        # self.reporte = Tk()
        self.reportes.title('Generar Reporte de Ventas')
        self.reportes.iconbitmap('img/icon.ico')
        self.reportes.config(bg='#fff')

        ##Seleccionar Fechas
        self.frameSuperior = Frame(self.reportes,bg='#fff')
        self.frameSuperior.pack(side=TOP, pady=10)

        Label(self.frameSuperior, text = 'Fecha Inicial',font=('Verdana',10),bg='#fff').grid(row=0,column=0, padx=10)
        self.fechaInicio = DateEntry(self.frameSuperior,width=12,
                    foreground='white', locale='es_MX', selectmode='day', date_pattern = 'y/mm/dd', maxdate = date.today())
        self.fechaInicio.grid(row=1,column=0,pady=5)        
        
        Label(self.frameSuperior, text = 'Fecha Final',font=('Verdana',10),bg='#fff').grid(row=0,column=3, padx=10)
        self.fechaFinal = DateEntry(self.frameSuperior,width=12,
                    foreground='white', locale='es_MX', selectmode='day', date_pattern = 'y/mm/dd', maxdate = date.today())
        self.fechaFinal.grid(row=1,column=3)

        ttk.Button(self.frameSuperior, text='Ver', command= self.verReporte).grid(row=2, column=1, pady=10)
        ttk.Button(self.frameSuperior, text='Excel', command= self.generarReporte).grid(row=2, column=2, pady=10)

        ##TreeView Reportes
        self.frameUsuarios = Frame(self.reportes,bg='#fff')
        self.frameUsuarios.pack(side=TOP, pady=5)

        self.tabla = ttk.Treeview(self.frameUsuarios, height=4 ,columns=(1,2,3,4,5,6), show ='headings')
        self.tabla.pack(side=TOP)
        
        self.tabla.heading(1, text="ID", anchor=CENTER)
        self.tabla.heading(2, text="Vendedor", anchor=CENTER)
        self.tabla.heading(3, text="Tipo", anchor=CENTER)
        self.tabla.heading(4, text="Cantidad", anchor=CENTER)
        self.tabla.heading(5, text="Precio", anchor=CENTER)
        self.tabla.heading(6, text="Fecha", anchor=CENTER)
        
        ## Total de ventas
        self.frameTotal = Frame(self.reportes,bg='#fff')
        self.frameTotal.pack(side=RIGHT)

        self.total = ttk.Entry(self.frameTotal, state= DISABLED)
        self.total.pack(side=RIGHT,pady=5,padx=8)
        Label(self.frameTotal, text='Total de ventas :',bg='#fff').pack(side=RIGHT)
        
        self.reportes.mainloop()

    def verReporte(self):
        self.limpiarTabla()
        fechaInicio = self.fechaInicio.get_date()
        fechaFinal = self.fechaFinal.get_date()

        self.reporte = fn.run_query('select * from ventas where fecha between ? and ? order by id_transaccion asc',(fechaInicio, fechaFinal))
        for (id,vendedor, tipo, cantidad, precio, fecha) in self.reporte:
            self.tabla.insert('',0, values = (id,vendedor,tipo,cantidad,precio,fecha))

        total = fn.run_query('select sum(dinero) from ventas where fecha between ? and ?', (fechaInicio,fechaFinal))

        self.totalVentas = fn.forIn(total)

        self.total.config(state= NORMAL)
        self.total.delete(0,END)
        self.total.insert(0,('$' + str(self.totalVentas[0])))
        self.total.config(state='readonly')
            
    def limpiarTabla(self):
        productos = self.tabla.get_children()
        for producto in productos:
            self.tabla.delete(producto)

    def generarReporte(self):
        self.verReporte()
        wb = Workbook()
        reporte = wb.active
        reporte.title = f'Generado {date.today()}'

        reporte.append(('', f'Reporte {self.fechaInicio.get_date()} - {self.fechaFinal.get_date()}'))

        reporte.append(('', ''))

        reporte.append(('#Venta','Vendedor', 'Tipo', 'Cantidad', 'Dinero', 'Fecha'))

        datos = fn.run_query('select * from ventas where fecha between ? and ?',(self.fechaInicio.get_date(),self.fechaFinal.get_date()))

        for dato in datos:
            reporte.append(dato)

        reporte.append(('', ''))
        reporte.append(('', '','' ,'Total Vendido',f'{str(self.totalVentas[0])}'))

        path = f'Reporte - {self.fechaInicio.get_date()} - {self.fechaFinal.get_date()}.xlsx'

        try:
            wb.save(path)
            ubicacion = move(path, 'reportes')
        except:
            remove(path)
            ubicacion = 'reportes\\'+path

        startfile(ubicacion)
        
# if __name__ == '__main__':
#     app = Reportes()