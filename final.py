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
conexionBDD = sqlite3.connect('itemsRatings.db')
conexion = conexionBDD.cursor()
fileDir = os.path.dirname(os.path.abspath(__file__))
path_datos_raiting = fileDir + '/datos-prueba/raiting_25.csv'
path_datos_ataques = fileDir + '/datos-prueba/datos_valores_25.csv'

raitings = pd.read_csv(path_datos_raiting, sep=',', names=['user_id','item_id','rating'])
lista_ratings = raitings.values.tolist()

items = pd.read_csv(path_datos_ataques)
lista_items = items.values.tolist()

class sistema_recomendacion_ciberseguridad:    
    def __init__(self, master):            
        global conexionBDD
        global conexion        
        self.style = ttk.Style()        
        self.box_value = tk.StringVar()
        conexion.execute(''' SELECT anomalia FROM items ''')
        self.items = conexion.fetchall()
        self.lista_anomalias = []
        for item in self.items:		
            self.anomalia =  ''.join(item)
            self.lista_anomalias.append(self.anomalia)	            
        self.master = master    
        self.treeview = ttk.Treeview(self.master,style="mystyle.Treeview")                
        self.labelNombreAtaque = Label(self.master, text = "Sistema Recomendador de Ciberseguridad", font=('Verdana', 13,'bold'))
        self.labelNombreAtaque.grid(pady=20,
						padx=10,
                        row=0,
                        column=0,
                        columnspan=10,
                    	sticky=S+N+E+W)	

        self.labelNombreAtaque = Label(self.master, text = "Nombre anomalia:", font=('Verdana', 12,'bold'))
        self.labelNombreAtaque.grid(row=1, column=0)	
        self.combo = tkentrycomplete.AutocompleteCombobox(textvariable=self.box_value,width=50)
        self.test_list = self.lista_anomalias
        self.combo.set_completion_list(self.test_list)
        self.combo.grid(row=1, column=1, sticky=E+W)        
        conexion.close()             
        self.botonRecomendacion = Button(self.master, text="Recomendar",command = self.recomendacion,font=('Verdana', 12,'bold'))
        self.botonRecomendacion.grid(pady=20,
						padx=10,
                        row=3,
                        column=0,
                        columnspan=3,
                    	sticky=S+N+E+W)		

    
    #def configuracion_tabla_recomendaciones(self): 


    def anomalia_seleccioanda():        
            curlItem = treeview.focus()
            receondeacion_anomaluia= treeview.item(curlItem)['values'][0]
            rating_anomalia =  treeview.item(curlItem)['values'][1]
            print(curlItem)
            print()
            print()	
            """        
                    raiz2 = Tk()				
                    raiz2.configure(bg = 'beige')
                    raiz2.title(curlItem)
                    raiz2.columnconfigure(0, weight=1)
                    raiz2.columnconfigure(1, weight=1)
                    raiz2.rowconfigure(2, weight=1)	
                    labelNombreAtaque = Label(raiz2, text = "Recoemndacion: "+receondeacion_anomaluia, font=('Verdana', 13,'bold'))
                    labelNombreAtaque.grid(pady=20,
                            padx=10,
                            row=0,
                            column=0,
                            columnspan=10,
                            sticky=S+N+E+W)				
                    labelNombreAtaque = Label(raiz2, text = "Rating: "+rating_anomalia, font=('Verdana', 13,'bold'))
                    labelNombreAtaque.grid(pady=20,
                            padx=10,
                            row=3,
                            column=0,
                            columnspan=10,
                            sticky=S+N+E+W)				

                    btn1 = Button(raiz2, text="Aceptar",font=('Verdana', 12,'bold'))
                    btn1.grid(pady=20,
                            padx=5,
                            row=6,
                            column=0,
                            columnspan=0,
                            sticky=S+N+E+W)							
                    btn2 = Button(raiz2, text="Aceptar",font=('Verdana', 12,'bold'))
                    btn2.grid(pady=20,
                            padx=5,
                            row=6,
                            column=1,
                            columnspan=3,
                            sticky=S+N+E+W)							
                            
                    #msg = messagebox.showinfo( "Recomendacion", 
                    #"Recomendacion: "+treeview.item(curlItem)['values'][0]+"\n"+"rating: "+treeview.item(curlItem)['values'][1])	
                    """
                
        
    def generar_recomendacion(self, anomalia):
        global raitings
        global items
        ataques_raitings = pd.merge(raitings, items, on='item_id')
        lista_ataques_raitings = ataques_raitings.values.tolist()
        print(ataques_raitings.head())

        media_ataques_raitings = pd.DataFrame(ataques_raitings.groupby(['anomalia','recomendacion'])['rating'].mean())
        print(media_ataques_raitings.head())


        media_ataques_raitings['numero_de_rating'] = ataques_raitings.groupby(['anomalia','recomendacion'])['rating'].count()
        print(media_ataques_raitings.head())

        matriz_usuario_ataque = ataques_raitings.pivot_table(index='user_id', columns='anomalia', values='rating')
        print(matriz_usuario_ataque.head())
        print(media_ataques_raitings.sort_values('numero_de_rating', ascending=False).head())	
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

                correlacion_recomendaciones = correlacion_recomendaciones.join(media_ataques_raitings['numero_de_rating'],how='left', lsuffix='_left', rsuffix='_right')
                correlacion_recomendaciones.head()
                #print(numero_usuarios)
                #if numero_usuarios > 0:
                    
                recomendaciones = correlacion_recomendaciones[correlacion_recomendaciones['numero_de_rating'] > 2].sort_values(by='rating', ascending=False).head()			
                print("LISTA DE RECOMENDACIONES PARA: ", anomalia )				
                for i,j in recomendaciones.iterrows():										
                        self.treeview.insert('','end',i[0],text=i[0],values=(i[1],str(j.values[0]), str(j.values[1])),tags = ('odd'))			
                self.treeview.bind('<Double-1>',anomalia_seleccioanda)               
                """
                
                def selectItem(a):
                    curlItem = treeview.focus()
                    receondeacion_anomaluia= treeview.item(curlItem)['values'][0]
                    rating_anomalia =  treeview.item(curlItem)['values'][1]
                    print(curlItem)
                    print()
                    print()	
                    
                    raiz2 = Tk()				
                    raiz2.configure(bg = 'beige')
                    raiz2.title(curlItem)
                    raiz2.columnconfigure(0, weight=1)
                    raiz2.columnconfigure(1, weight=1)
                    raiz2.rowconfigure(2, weight=1)	
                    labelNombreAtaque = Label(raiz2, text = "Recoemndacion: "+receondeacion_anomaluia, font=('Verdana', 13,'bold'))
                    labelNombreAtaque.grid(pady=20,
                            padx=10,
                            row=0,
                            column=0,
                            columnspan=10,
                            sticky=S+N+E+W)				
                    labelNombreAtaque = Label(raiz2, text = "Rating: "+rating_anomalia, font=('Verdana', 13,'bold'))
                    labelNombreAtaque.grid(pady=20,
                            padx=10,
                            row=3,
                            column=0,
                            columnspan=10,
                            sticky=S+N+E+W)				

                    btn1 = Button(raiz2, text="Aceptar",font=('Verdana', 12,'bold'))
                    btn1.grid(pady=20,
                            padx=5,
                            row=6,
                            column=0,
                            columnspan=0,
                            sticky=S+N+E+W)							
                    btn2 = Button(raiz2, text="Aceptar",font=('Verdana', 12,'bold'))
                    btn2.grid(pady=20,
                            padx=5,
                            row=6,
                            column=1,
                            columnspan=3,
                            sticky=S+N+E+W)							
                            
                    #msg = messagebox.showinfo( "Recomendacion", 
                    #"Recomendacion: "+treeview.item(curlItem)['values'][0]+"\n"+"rating: "+treeview.item(curlItem)['values'][1])	

                treeview.bind('<Double-1>',selectItem)
                #treeview.
                #else:
                #	print("Oops!  No existen usuarios .  Intenta de nuevo...")					 
                """
            except KeyError:
                print("Oops!  La palabra ingresado no se encuetra registarda.  Intenta de nuevo...")
                for i in self.treeview.get_children():
                        self.treeview.delete(i)
                msg = messagebox.showinfo( "Oops", "La palabra ingresado no se encuetra registarda.  Intenta de nuevo...")			
        else:
            print("Oops!  La palabra ingresado no se encuetra registarda.  Intenta de nuevo...")
            for i in self.treeview.get_children():
                        self.treeview.delete(i)
            msg = messagebox.showinfo( "Oops", "Debes Ingresar una palabra.  Intenta de nuevo...")		



    def recomendacion(self):                
        self.style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Verdana', 11)) # Modify the font of the body
        self.style.configure("mystyle.Treeview.Heading", font=('Verdana', 12,'bold')) # Modify the font of the headings
        self.style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders		        
        self.treeview.tag_configure('odd', background='#E8E8E8')        
        self.treeview.grid(pady=10,
                            padx=10,
                            row=6,
                            column=0,
                            columnspan=3,
                            sticky=S+N+E+W)	
            
        self.treeview["columns"]=("#1","#2","#3")
        self.treeview.column('#0', width=800, anchor='w') 
        self.treeview.column('#1', width=20, anchor='w') 
        self.treeview.column('#2', width=20, anchor='w') 
        self.treeview.column('#3', width=100, anchor='w') 
        
        self.treeview.heading('#0', text='Anomalia')
        self.treeview.heading('#1', text='recomendacion')
        self.treeview.heading('#2', text='rating')			
        self.treeview.heading('#3', text='numero raitings')
        anomalia = self.box_value.get()           
        self.ge(anomalia)
        
        """
        anomalia = self.box_value.get()   
        conn = sqlite3.connect('itemsRatings.db')
        c = conn.cursor()	
        fileDir = os.path.dirname(os.path.abspath(__file__))
        path_datos_raiting = fileDir + '/datos-prueba/raiting_25.csv'
        path_datos_ataques = fileDir + '/datos-prueba/datos_valores_25.csv'
        raitings = pd.read_csv(path_datos_raiting, sep=',', names=['user_id','item_id','rating'])
        lista_ratings = raitings.values.tolist()
        sql_inserts_data = "INSERT INTO ratings (user_id,item_id, rating) VALUES (?, ?,?);"
        sql_delete_data = "DELETE FROM ratings"
        conn.execute(sql_delete_data)
        conn.executemany(sql_inserts_data, lista_ratings)
        conn.commit()
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Verdana', 11)) # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Verdana', 12,'bold')) # Modify the font of the headings
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders		
        treeview=ttk.Treeview(self.master,style="mystyle.Treeview")
        treeview.tag_configure('odd', background='#E8E8E8')
        treeview.tag_configure('even', background='#DFDFDF')
        treeview.grid(pady=10,
                            padx=10,
                            row=6,
                            column=0,
                            columnspan=3,
                            sticky=S+N+E+W)	
            
        treeview["columns"]=("#1","#2","#3")
        treeview.column('#0', width=800, anchor='w') 
        treeview.column('#1', width=20, anchor='w') 
        treeview.column('#2', width=20, anchor='w') 
        treeview.column('#3', width=100, anchor='w') 
        treeview.heading('#0', text='Anomalia')
        treeview.heading('#1', text='recomendacion')
        treeview.heading('#2', text='rating')			
        treeview.heading('#3', text='numero raitings')

        print(raitings.head())

        items = pd.read_csv(path_datos_ataques)
        lista_items = items.values.tolist()
        sql_inserts_data = "INSERT INTO items (item_id, anomalia, descripcion, criticidad, recomendacion) VALUES (?, ?,?,?,?);"
        sql_delete_data = "DELETE FROM items"
        conn.execute(sql_delete_data)
        conn.executemany(sql_inserts_data, lista_items)
        conn.commit()

        print(items.head())
        

        ataques_raitings = pd.merge(raitings, items, on='item_id)
        lista_ataques_raitings = ataques_raitings.values.tolist()
        #print(lista_ataques_raitings)
        #sql_inserts_data = "INSERT INTO items_ratings (item_id, anomalia, descripcion, criticidad, recomendacion) VALUES (?, ?,?,?,?);"
        #sql_delete_data = "DELETE FROM items"
        #conn.execute(sql_delete_data)
        #conn.executemany(sql_inserts_data, lista_items)
        #conn.commit()
        
        print(ataques_raitings.head())

        media_ataques_raitings = pd.DataFrame(ataques_raitings.groupby(['anomalia','recomendacion'])['rating'].mean())
        print(media_ataques_raitings.head())


        media_ataques_raitings['numero_de_rating'] = ataques_raitings.groupby(['anomalia','recomendacion'])['rating'].count()
        print(media_ataques_raitings.head())

        matriz_usuario_ataque = ataques_raitings.pivot_table(index='user_id', columns='anomalia', values='rating')
        print(matriz_usuario_ataque.head())
        print(media_ataques_raitings.sort_values('numero_de_rating', ascending=False).head())	

        
        
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

                correlacion_recomendaciones = correlacion_recomendaciones.join(media_ataques_raitings['numero_de_rating'],how='left', lsuffix='_left', rsuffix='_right')
                correlacion_recomendaciones.head()
                #print(numero_usuarios)
                #if numero_usuarios > 0:
                    
                recomendaciones = correlacion_recomendaciones[correlacion_recomendaciones['numero_de_rating'] > 2].sort_values(by='rating', ascending=False).head()			
                print("LISTA DE RECOMENDACIONES PARA: ", anomalia )				
                for i,j in recomendaciones.iterrows():										
                        treeview.insert('','end',i[0],text=i[0],values=(i[1],str(j.values[0]), str(j.values[1])),tags = ('odd'))			

                def selectItem(a):
                    curlItem = treeview.focus()
                    receondeacion_anomaluia= treeview.item(curlItem)['values'][0]
                    rating_anomalia =  treeview.item(curlItem)['values'][1]
                    print(curlItem)
                    print()
                    print()	
                    
                    raiz2 = Tk()				
                    raiz2.configure(bg = 'beige')
                    raiz2.title(curlItem)
                    raiz2.columnconfigure(0, weight=1)
                    raiz2.columnconfigure(1, weight=1)
                    raiz2.rowconfigure(2, weight=1)	
                    labelNombreAtaque = Label(raiz2, text = "Recoemndacion: "+receondeacion_anomaluia, font=('Verdana', 13,'bold'))
                    labelNombreAtaque.grid(pady=20,
                            padx=10,
                            row=0,
                            column=0,
                            columnspan=10,
                            sticky=S+N+E+W)				
                    labelNombreAtaque = Label(raiz2, text = "Rating: "+rating_anomalia, font=('Verdana', 13,'bold'))
                    labelNombreAtaque.grid(pady=20,
                            padx=10,
                            row=3,
                            column=0,
                            columnspan=10,
                            sticky=S+N+E+W)				

                    btn1 = Button(raiz2, text="Aceptar",font=('Verdana', 12,'bold'))
                    btn1.grid(pady=20,
                            padx=5,
                            row=6,
                            column=0,
                            columnspan=0,
                            sticky=S+N+E+W)							
                    btn2 = Button(raiz2, text="Aceptar",font=('Verdana', 12,'bold'))
                    btn2.grid(pady=20,
                            padx=5,
                            row=6,
                            column=1,
                            columnspan=3,
                            sticky=S+N+E+W)							
                            
                    #msg = messagebox.showinfo( "Recomendacion", 
                    #"Recomendacion: "+treeview.item(curlItem)['values'][0]+"\n"+"rating: "+treeview.item(curlItem)['values'][1])	

                treeview.bind('<Double-1>',selectItem)
                #treeview.
                #else:
                #	print("Oops!  No existen usuarios .  Intenta de nuevo...")					 
            except KeyError:
                print("Oops!  La palabra ingresado no se encuetra registarda.  Intenta de nuevo...")
                for i in treeview.get_children():
                        treeview.delete(i)
                msg = messagebox.showinfo( "Oops", "La palabra ingresado no se encuetra registarda.  Intenta de nuevo...")			
        else:
            print("Oops!  La palabra ingresado no se encuetra registarda.  Intenta de nuevo...")
            for i in treeview.get_children():
                        treeview.delete(i)
            msg = messagebox.showinfo( "Oops", "Debes Ingresar una palabra.  Intenta de nuevo...")		

        conn.close()
        """


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
        conexion.execute('''CREATE TABLE ratings
                (user_id text, item_id text, rating text)''')
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
        conexion.execute('''CREATE TABLE items
                (item_id text, anomalia text, descripcion text, criticidad text, recomendacion text)''')        
        sql_insert = "INSERT INTO items (item_id, anomalia, descripcion, criticidad, recomendacion) VALUES (?, ?,?,?,?);"
        #sql_delete = "DELETE FROM ratings"
        #conn.execute(sql_delete_data)
        conexionBDD.executemany(sql_insert, lista_items)
        conexionBDD.commit()
        #conexionBDD.close()

"""
def agregar_informacion_items_ratings():    
        global conexionBDD
        global conexion
        global lista_ratings
        conexion.execute('''CREATE TABLE items_ratings
                (anomalia text, rating text, numero_de_rating text)''')
        sql_insert = "INSERT INTO ratings (user_id,item_id, rating) VALUES (?, ?,?);"
        sql_delete = "DELETE FROM ratings"
        #conn.execute(sql_delete_data)
        conexion.executemany(sql_inserts_data, lista_ratings)
        conexion.commit()
        conexion.close()
"""

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

