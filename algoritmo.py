from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
def recomendacion(anomalia,raiz):
	
	fileDir = os.path.dirname(os.path.abspath(__file__))
	path_datos_raiting = fileDir + '/datos-prueba/raiting_25.csv'
	path_datos_ataques = fileDir + '/datos-prueba/datos_valores_25.csv'
	raitings = pd.read_csv(path_datos_raiting, sep=',', names=['user_id','item_id','rating'])
	"""
	Lb1 = Listbox(raiz)
	Lb1.grid(pady=10,
						padx=10,
                        row=6,
                        column=0,
                        columnspan=3,
                    	sticky=S+N+E+W)	
	headers = ["ANOMALÌA", "RATING", "NUMERO RATINGS"]
	row_format ="{:<8}  {:>8}  {:8}" 
	"""

	print(raitings.head())

	items = pd.read_csv(path_datos_ataques)
	print(items.head())


	ataques_raitings = pd.merge(raitings, items, on='item_id')
	print(ataques_raitings.head())

	media_ataques_raitings = pd.DataFrame(ataques_raitings.groupby(['name'])['rating'].mean())
	print(media_ataques_raitings.head())


	media_ataques_raitings['numero_de_rating'] = ataques_raitings.groupby(['name'])['rating'].count()
	print(media_ataques_raitings.head())

	matriz_usuario_ataque = ataques_raitings.pivot_table(index='user_id', columns='name', values='rating')
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
			treeview=ttk.Treeview(raiz)
			treeview.grid(pady=10,
						padx=10,
                        row=6,
                        column=0,
                        columnspan=3,
                    	sticky=S+N+E+W)	
			treeview["columns"]=("#1","#2")
			treeview.heading('#0', text='Anomalia')
			treeview.heading('#1', text='rating')
			treeview.heading('#2', text='numero raitings')			
			for i,j in recomendaciones.iterrows():					
					treeview.insert('','end',i,text=i,values=(str(j.values[0]), str(j.values[1])))			
			#else:
			#	print("Oops!  No existen usuarios .  Intenta de nuevo...")					 
		except KeyError:
			print("Oops!  La palabra ingresado no se encuetra registarda.  Intenta de nuevo...")
			msg = messagebox.showinfo( "Oops", "La palabra ingresado no se encuetra registarda.  Intenta de nuevo...")			
	else:
		print("Oops!  La palabra ingresado no se encuetra registarda.  Intenta de nuevo...")
		msg = messagebox.showinfo( "Oops", "Debes Ingresar una palabra.  Intenta de nuevo...")		
	

raiz = Tk()
#raiz.geometry('800x600') # anchura x altura
raiz.configure(bg = 'beige')
raiz.title('Sistema de recomendación')
raiz.columnconfigure(0, weight=1)
raiz.columnconfigure(1, weight=1)
raiz.rowconfigure(2, weight=1)

labelNombreAtaque = Label(raiz, text = "Sistema de Recomendador de Ciberseguridad", font=("Arial Bold", 15))
labelNombreAtaque.grid(pady=20,
						padx=10,
                        row=0,
                        column=0,
                        columnspan=10,
                    	sticky=S+N+E+W)	

labelNombreAtaque = Label(raiz, text = "Nombre anomalia:", font=("Arial Bold", 10))
labelNombreAtaque.grid(row=1, column=0)	
inputNombreAtaque = Entry(raiz, width=50)
inputNombreAtaque.grid(row=1, column=1, sticky=E+W)
def mensaje():		
		recomendacion(inputNombreAtaque.get(), raiz)
botonRecomendacion = Button(raiz, text="Recomendar",command = mensaje)
botonRecomendacion.grid(pady=10,
						padx=10,
                        row=3,
                        column=0,
                        columnspan=3,
                    	sticky=S+N+E+W)							
raiz.mainloop()