from tkinter import *
from tkinter import ttk
import funciones as fn

root = Tk()

options = []

for id in fn.run_query('select id from socios'):
    options.append(id[0])

values = StringVar(root)
values.set('Seleccionar')


menu = OptionMenu(root,values,*options)
menu.pack()


def imprimir():
    print(f'Valor: {values.get()}')

Button(root, text='OK', command = imprimir).pack()


root.mainloop()

