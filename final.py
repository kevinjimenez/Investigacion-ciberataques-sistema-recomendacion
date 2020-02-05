import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox
#from googletrans import Translator
import tkentrycomplete
import sqlite3, csv
import os
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
#translator = Translator()
conexionBDD = sqlite3.connect('itemsRatings.db')
conexion = conexionBDD.cursor()
fileDir = os.path.dirname(os.path.abspath(__file__))
### DATOS PRUEBA

path_datos_rating_prueba = fileDir + '/datos-prueba/raiting_25.csv'
path_datos_ataques_prueba = fileDir + '/datos-prueba/datos_valores_25.csv'

###


path_datos_rating = fileDir + '/datos-sistema-recomendacion/rating_anomalias.csv'
path_datos_ataques = fileDir + '/datos-sistema-recomendacion/anomalias.csv'

ratings = pd.read_csv(path_datos_rating, sep=',', names=['user_id','item_id','rating'])
lista_ratings = ratings.values.tolist()

items = pd.read_csv(path_datos_ataques)
lista_items = items.values.tolist()

class sistema_recomendacion_ciberseguridad:    
    def __init__(self, master):            
        global conexionBDD
        global conexion        
        self.style = ttk.Style()        
        self.box_value = tk.StringVar()
        conexion.execute('SELECT anomalia FROM items')
        self.items = conexion.fetchall()
        self.lista_anomalias = []
        for item in self.items:		
            self.anomalia =  ''.join(item)
            self.lista_anomalias.append(self.anomalia)	            
        self.master = master    
        self.treeview = ttk.Treeview(self.master,style="mystyle.Treeview")                
        self.labelNombreAtaque = Label(self.master, text = "Sistema Recomendación de Ciberseguridad", font=('Helvetica', 18,'bold','italic'))
        self.labelNombreAtaque.grid(pady=20,
                                padx=10,
                                row=0,
                                column=0,
                                columnspan=10,
                                sticky=S+N+E+W)	

        self.labelNombreAtaque = Label(self.master, text = "Nombre anomalía:", font=('Helvetica', 16,'bold','italic'))
        self.labelNombreAtaque.grid(row=1, column=0)	
        self.combo = tkentrycomplete.AutocompleteCombobox(textvariable=self.box_value,width=50)
        self.test_list = self.lista_anomalias
        self.combo.set_completion_list(self.test_list)
        self.combo.grid(row=1, column=1, sticky=E+W)        
        conexion.close()             
        self.botonRecomendacion = Button(self.master, text="Generar recomendación",command = self.recomendacion,font=('Helvetica', 16,'bold','italic'))
        self.botonRecomendacion.grid(pady=20,
                                padx=10,
                                row=3,
                                column=0,
                                columnspan=3,
                                sticky=S+N+E+W)		

    
    def generar_recomendacion(self, anomalia):
        global ratings
        global items
        self.vaciar_lista()
        descripcion = ""
        ataques_ratings = pd.merge(ratings, items, on='item_id')
        lista_ataques_ratings = ataques_ratings.values.tolist()
        print(ataques_ratings.head())

        media_ataques_ratings = pd.DataFrame(ataques_ratings.groupby(['anomalia','recomendacion','descripcion'])['rating'].mean())
        print(media_ataques_ratings.head())


        media_ataques_ratings['numero_de_rating'] = ataques_ratings.groupby(['anomalia','recomendacion','descripcion'])['rating'].count()
        print(media_ataques_ratings.head())

        matriz_usuario_ataque = ataques_ratings.pivot_table(index='user_id', columns='anomalia', values='rating')
        print(matriz_usuario_ataque.head())
        print(media_ataques_ratings.sort_values('numero_de_rating', ascending=False).head())	
        if anomalia != "" :
            try:
                #numero_usuarios = 0
                palabra_buscar = anomalia.strip()
                user_rating = matriz_usuario_ataque[palabra_buscar]
                user_rating.head()
                recomendacion_similar=matriz_usuario_ataque.corrwith(user_rating)
                recomendacion_similar.head()

                correlacion_recomendaciones = pd.DataFrame(recomendacion_similar, columns=['rating'])
                correlacion_recomendaciones.dropna(inplace=True)
                correlacion_recomendaciones.head()

                correlacion_recomendaciones = correlacion_recomendaciones.join(media_ataques_ratings['numero_de_rating'],how='left', lsuffix='_left', rsuffix='_right')
                correlacion_recomendaciones.head()
                #print(numero_usuarios)
                #if numero_usuarios > 0:
                    
                recomendaciones = correlacion_recomendaciones[correlacion_recomendaciones['numero_de_rating'] > 2].sort_values(by='rating', ascending=False).head()			
                print("LISTA DE RECOMENDACIONES PARA: ", anomalia )				
                for i,j in recomendaciones.iterrows():		                        
                        nombre_anomalia = i[0]
                        recomendacion_anomalia = i[2]
                        descripcion_anomalia = i[1]
                        valor_rating = str(j.values[0]) # round(j.values[0],6)
                        numero_rating = str(round(j.values[0],2))                                                
                        self.treeview.insert('','end',nombre_anomalia,text=nombre_anomalia,values=(valor_rating, numero_rating,descripcion_anomalia,recomendacion_anomalia),tags = ('odd'))			
		
                def anomalia_seleccionada(anomalia):
                        item = self.treeview.focus()                        
                        valores_item = self.treeview.item(item)['values']                                                
                        self.cuadro_recomendacion(item,valores_item)

                self.treeview.bind('<Double-1>',anomalia_seleccionada)                               
                #else:
                #	print("Oops!  No existen usuarios .  Intenta de nuevo...")					                 
            except KeyError:
                print("Oops!  La anomalía ingresada no se encuentra registrada.  Intenta de nuevo...")
                self.vaciar_lista()
                msg = messagebox.showinfo( "Oops", "La ananomalía ingresada no se encuentra registrada.  Intenta de nuevo...")			
        else:
            print("Oops!  La anomalía ingresada no se encuentra registrada.  Intenta de nuevo...")
            self.vaciar_lista()
            msg = messagebox.showinfo( "Oops", "Debes Ingresar una anomalía.  Intenta de nuevo...")		

    def vaciar_lista(self):
            for i in self.treeview.get_children():
                self.treeview.delete(i) 


    def recomendacion(self):                
        self.style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Verdana', 11))
        self.style.configure("mystyle.Treeview.Heading", font=('Helvetica', 16,'bold','italic'))
        self.style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])
        self.treeview.tag_configure('odd', background='#E8E8E8')        
        self.treeview.grid(pady=10,
                            padx=10,
                            row=6,
                            column=0,
                            columnspan=3,
                            sticky=S+N+E+W)	
            
        self.treeview["columns"]=("#1","#2")
        self.treeview.column('#0', width=725, anchor='w')         
        self.treeview.column('#1', width=80, anchor='w') 
        self.treeview.column('#2', width=150, anchor='w') 
        
        self.treeview.heading('#0', text='Anomalías Similares')        
        self.treeview.heading('#1', text='Rating')			
        self.treeview.heading('#2', text='Número ratings')
        anomalia = self.box_value.get()           
        self.generar_recomendacion(anomalia)

    def cuadro_recomendacion(self,item,valores_item):   
                global translator             
                #traduccion_descripcion = translator.translate(valores_item[3],dest='es')
                #traduccion_recomendacion = translator.translate(valores_item[2],dest='es')
                recoemndacion_cuadro = tk.Tk()                
                recoemndacion_cuadro.configure(bg = 'beige')  
                recoemndacion_cuadro.title(item)      
                recoemndacion_cuadro.columnconfigure(0, weight=1)
                recoemndacion_cuadro.columnconfigure(1, weight=1)
                recoemndacion_cuadro.rowconfigure(2, weight=1)     
                rating = Label(recoemndacion_cuadro,justify=tk.CENTER, text = "Rating: "+valores_item[0], font=('Helvetica', 25,'bold','italic'))
                rating.grid(pady=20,
                            padx=10,
                            row=0, 
                            column=3,
                            sticky=S+N+E+W)	
                label_descripcion = Label(recoemndacion_cuadro, text = "Descripción: ", font=('Helvetica', 20,'bold','italic'))
                label_descripcion.grid(pady=10,
                                padx=10,
                                row=1, 
                                column=0)	

                txt_descripcion = scrolledtext.ScrolledText(recoemndacion_cuadro,width=30,height=7,font=('Helvetica', 16,'bold','italic'))
                txt_descripcion.insert(INSERT,valores_item[3])
                #txt_descripcion.config(state=DISABLED)
                txt_descripcion.grid(pady=20,
                        padx=10,
                        row=2, 
                        column=0,
                        columnspan=3,
                        sticky=S+N+E+W)           # Helvetica 16 bold italic
                label_recomendacion = Label(recoemndacion_cuadro, text = "Recomendación: ", font=('Helvetica', 20,'bold','italic'))
                label_recomendacion.grid(pady=10,
                                padx=10,
                                row=1, 
                                column=3)	

                txt_recomendacion = scrolledtext.ScrolledText(recoemndacion_cuadro,width=60,height=15,font=('Helvetica', 16,'bold','italic'))
                txt_recomendacion.insert(INSERT,valores_item[2])
                #txt_recomendacion.config(state=DISABLED)
                txt_recomendacion.grid(pady=20,
                        padx=10,
                        row=2, 
                        column=3,
                        columnspan=3,
                        sticky=S+N+E+W)                
                boton_aceptar = Button(recoemndacion_cuadro, text="Aceptar", width = 25 , command = recoemndacion_cuadro.destroy,font=('Verdana', 12,'bold'))
                boton_aceptar.grid(pady=20,
                                padx=20,
                                row=6,
                                column=3,
                                columnspan=3,
                                sticky=E+W)                

def main():    
    inicio()

def inicio():
    global conexionBDD
    global conexion
    conexion.execute(''' SELECT name FROM sqlite_master WHERE type='table' ''')
    tablas = conexion.fetchall() 
    if len(tablas) > 0:        
        print('Existen tablas.')
        diseno_interfaz()
    else:                
        print('Base de datos creada.') 
        agregar_informacion_ratings()
        agregar_informacion_items()
        diseno_interfaz()

def agregar_informacion_ratings():
        global conexionBDD
        global conexion
        global lista_ratings        
        conexion.execute('CREATE TABLE ratings (user_id text, item_id text, rating text)')
        sql_insert = "INSERT INTO ratings (user_id,item_id, rating) VALUES (?, ?,?);"
        sql_delete = "DELETE FROM ratings"
        #conn.execute(sql_delete_data)
        conexionBDD.executemany(sql_insert, lista_ratings)
        conexionBDD.commit()
        #conexionBDD.close()

def agregar_informacion_items():    
        global conexionBDD
        global conexion
        global lista_items
        conexion.execute('CREATE TABLE items (item_id text, anomalia text, descripcion text, criticidad text, recomendacion text)')
        sql_insert = "INSERT INTO items (item_id, anomalia, descripcion, criticidad, recomendacion) VALUES (?, ?,?,?,?);"
        #sql_delete = "DELETE FROM ratings"
        #conn.execute(sql_delete_data)
        conexionBDD.executemany(sql_insert, lista_items)
        conexionBDD.commit()
        #conexionBDD.close()

def diseno_interfaz():
        root = tk.Tk()
        root.configure(bg = 'beige')  
        root.title('Sistema de recomendación')      
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)
        root.rowconfigure(2, weight=1)
        app = sistema_recomendacion_ciberseguridad(root)
        root.mainloop()    


if __name__ == '__main__':
    main()

