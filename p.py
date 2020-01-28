#!/usr/bin/env python

from googletrans import Translator

translator = Translator()
translated = translator.translate('XSS flaws occur whenever an application includes untrusted data in a new web page without proper validation or escaping, or updates an existing web page with user-supplied data using a browser API that can create HTML or JavaScript. XSS allows attackers to execute scripts in the victim’s browser which can hijack user sessions, deface web sites, or redirect the user to malicious sites.',dest='es')

print(translated.text)

"""
from tkinter import *
 
from tkinter import scrolledtext
 
window = Tk()
 
window.title("Welcome to LikeGeeks app")
 
window.geometry('350x200')
 
txt = scrolledtext.ScrolledText(window,width=40,height=10)

txt.grid(column=0,row=0)
 
window.mainloop()
"""
"""
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkentrycomplete
import sqlite3, csv
import os
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
class Demo1:
    def __init__(self, master, anomalia):
        print(anomalia)

        self.master = master        
        self.anomalia = anomalia        
        self.botonRecomendacion = Button(self.master, text="Recomendar",command = self.new_window,font=('Verdana', 12,'bold'))
        self.botonRecomendacion.grid(pady=20,
						padx=10,
                        row=3,
                        column=0,
                        columnspan=3,
                    	sticky=S+N+E+W)							              



    def new_window(self):
            print(self.anomalia)
            self.newWindow = tk.Toplevel(self.master)
            self.app = Demo2(self.newWindow)

        self.frame = tk.Frame(self.master)
        self.button1 = tk.Button(self.frame, text = 'New Window', width = 25, command = self.new_window)
        self.button1.pack()
        self.frame.pack()

    def new_window(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = Demo2(self.newWindow)

class Demo2:
    def __init__(self, master):
        self.master = master
        
        self.frame = tk.Frame(self.master)
        self.quitButton = tk.Button(self.frame, text = 'Quit', width = 25, command = self.close_windows)
        self.quitButton.pack()
        self.frame.pack()

    def close_windows(self):
        self.master.destroy()

def main(): 
    conexionBDD = sqlite3.connect('itemsRatings.db')
    conexion = conexionBDD.cursor()
    root = tk.Tk()

    box_value = tk.StringVar()
    conexion.execute(''' SELECT anomalia FROM items ''')
    items = conexion.fetchall()
    lista_anomalias = []
    for item in items:		
	    anomalia =  ''.join(item)
	    lista_anomalias.append(anomalia)	
    root.configure(bg = 'beige')
    root.title('Sistema de recomendación')
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.rowconfigure(2, weight=1)
    labelNombreAtaque = Label(root, text = "Sistema Recomendador de Ciberseguridad", font=('Verdana', 13,'bold'))
    labelNombreAtaque.grid(pady=20,
						padx=10,
                        row=0,
                        column=0,
                        columnspan=10,
                    	sticky=S+N+E+W)	

    labelNombreAtaque = Label(root, text = "Nombre anomalia:", font=('Verdana', 12,'bold'))
    labelNombreAtaque.grid(row=1, column=0)	
    combo = tkentrycomplete.AutocompleteCombobox(textvariable=box_value,width=50)
    test_list = lista_anomalias
    combo.set_completion_list(test_list)
    combo.grid(row=1, column=1, sticky=E+W)
    print(box_value.get(),1)
    conexion.close()        
    app = Demo1(root,'adas')
    root.mainloop()

if __name__ == '__main__':
    main()
"""
