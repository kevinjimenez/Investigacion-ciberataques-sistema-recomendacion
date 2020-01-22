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
	
	style = ttk.Style()
	style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11)) # Modify the font of the body
	style.configure("mystyle.Treeview.Heading", font=('Calibri', 12,'bold')) # Modify the font of the headings
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
	treeview.column('#1', width=100, anchor='w') 
	treeview.column('#2', width=20, anchor='w') 
	treeview.heading('#0', text='Anomalia')
	treeview.heading('#1', text='rating')
	treeview.heading('#2', text='numero raitings')			

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

labelNombreAtaque = Label(raiz, text = "Sistema Recomendador de Ciberseguridad", font=('Calibri', 13,'bold'))
labelNombreAtaque.grid(pady=20,
						padx=10,
                        row=0,
                        column=0,
                        columnspan=10,
                    	sticky=S+N+E+W)	

labelNombreAtaque = Label(raiz, text = "Nombre anomalia:", font=('Calibri', 12,'bold'))
labelNombreAtaque.grid(row=1, column=0)	
inputNombreAtaque = Entry(raiz, width=60)
inputNombreAtaque.grid(row=1, column=1, sticky=E+W)
def mensaje():		
		recomendacion(inputNombreAtaque.get(), raiz)
botonRecomendacion = Button(raiz, text="Recomendar",command = mensaje,font=('Calibri', 12,'bold'))
botonRecomendacion.grid(pady=10,
						padx=10,
                        row=3,
                        column=0,
                        columnspan=3,
                    	sticky=S+N+E+W)							
raiz.mainloop()