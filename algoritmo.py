from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3, csv
import os
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
conn = sqlite3.connect('itemsRatings.db')
c = conn.cursor()
def recomendacion(anomalia,raiz):
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
	treeview=ttk.Treeview(raiz,style="mystyle.Treeview")
	treeview.tag_configure('odd', background='#E8E8E8')
	treeview.tag_configure('even', background='#DFDFDF')
	treeview.grid(pady=10,
						padx=10,
                        row=6,
                        column=0,
                        columnspan=3,
                    	sticky=S+N+E+W)	
		
	treeview["columns"]=("#1","#2")
	treeview.column('#0', width=800, anchor='w') 
	treeview.column('#1', width=20, anchor='w') 
	treeview.column('#2', width=100, anchor='w') 
	treeview.heading('#0', text='Anomalia')
	treeview.heading('#1', text='rating')
	treeview.heading('#2', text='numero raitings')			

	print(raitings.head())

	items = pd.read_csv(path_datos_ataques)
	lista_items = items.values.tolist()
	sql_inserts_data = "INSERT INTO items (item_id, anomalia, descripcion, criticidad, recomendacion) VALUES (?, ?,?,?,?);"
	sql_delete_data = "DELETE FROM items"
	conn.execute(sql_delete_data)
	conn.executemany(sql_inserts_data, lista_items)
	conn.commit()
	conn.close()

	print(items.head())


	ataques_raitings = pd.merge(raitings, items, on='item_id')
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
					print(type(j.values[0]))
					treeview.insert('','end',i,text=i,values=(str(j.values[0]), str(j.values[1])),tags = ('odd'))			
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



"""
try:
    #ratingDb = open("rating.db")
	 itemsDb = open("items.db")
	#itemsRatingsDb = open("itemsRatings.db")
    # Do something with the file
except IOError:
    print("File not accessible")
finally:
    #ratingDb.close()
	itemsDb.close()
	#itemsRatingsDb.close()
"""


#c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='items_ratings' ''')
c.execute(''' SELECT name FROM sqlite_master WHERE type='table' ''')
rows = c.fetchall() 
if len(rows) > 0:
	print('Existen tablas.')
else:
	c.execute('''CREATE TABLE items_ratings
             (anomalia text, rating text, numero_de_rating text)''')
	c.execute('''CREATE TABLE ratings
             (user_id text, item_id text, rating text)''')
	c.execute('''CREATE TABLE items
             (item_id text, anomalia text, descripcion text, criticidad text, recomendacion text)''')
	print('Base de datos sin tablas.')

# Insert a row of data
#c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
conn.commit()
conn.close()
# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
raiz = Tk()
windowWidth = raiz.winfo_reqwidth()
windowHeight = raiz.winfo_reqheight()
positionRight = int(raiz.winfo_screenwidth()/2 - windowWidth/2)
positionDown = int(raiz.winfo_screenheight()/2 - windowHeight/2)
raiz.geometry("+{}+{}".format(positionRight, positionDown))
#raiz.geometry('1400x400') # anchura x altura
raiz.configure(bg = 'beige')
raiz.title('Sistema de recomendación')
raiz.columnconfigure(0, weight=1)
raiz.columnconfigure(1, weight=1)
raiz.rowconfigure(2, weight=1)

labelNombreAtaque = Label(raiz, text = "Sistema Recomendador de Ciberseguridad", font=('Verdana', 13,'bold'))
labelNombreAtaque.grid(pady=20,
						padx=10,
                        row=0,
                        column=0,
                        columnspan=10,
                    	sticky=S+N+E+W)	

labelNombreAtaque = Label(raiz, text = "Nombre anomalia:", font=('Verdana', 12,'bold'))
labelNombreAtaque.grid(row=1, column=0)	
inputNombreAtaque = Entry(raiz, width=60)
inputNombreAtaque.grid(row=1, column=1, sticky=E+W)
def realizarRecomendacion():		
		recomendacion(inputNombreAtaque.get(), raiz)
botonRecomendacion = Button(raiz, text="Recomendar",command = realizarRecomendacion,font=('Verdana', 12,'bold'))
botonRecomendacion.grid(pady=20,
						padx=10,
                        row=3,
                        column=0,
                        columnspan=3,
                    	sticky=S+N+E+W)							
raiz.mainloop()
