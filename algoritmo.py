# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
fileDir = os.path.dirname(os.path.abspath(__file__))
path_datos_raiting = fileDir + '/datos-prueba/raiting_25.csv'
path_datos_nombre_categoria = fileDir + '/datos-prueba/datos_valores_25.csv'

# leer archivo de ratings por usuario y pelicula
df = pd.read_csv(path_datos_raiting, sep=',', names=['user_id','id_attack','rating'])
# listar 10 primeros registros del archivo de ratings
df.head(10)
# leer archivo de titulos de peliculas con su id

items = pd.read_csv(path_datos_nombre_categoria)
# listar 10 primeros registros del archivo de titulos de peliculas
items.head(10)
#print(titulos_peliculas)

# union de los dataframes de ratings con los titulos de peliculas con su id  

df = pd.merge(df, items, on='id_attack')
df.head(20)
# los raitings agrupados por titulo y calculando 
# la media x su raiting media o promedio de cada pelicula

ratings = pd.DataFrame(df.groupby(['name','description','criticidad'])['rating'].mean())
ratings.head(10)

ratings['numero_de_rating'] = df.groupby(['name','description','criticidad'])['rating'].count()
ratings.head()

matriz_pelicula = df.pivot_table(index='user_id', columns='name', values='rating')
matriz_pelicula.head()

ratings.sort_values('numero_de_rating', ascending=False).head(10)
print("Ingrese palabra:") 
palabra = input()

print("Palabra Ingresada", palabra)

if palabra != "" :
	try:
		palabra_buscar = palabra.strip()
		user_rating = matriz_pelicula[palabra_buscar]
		user_rating.head()
		similar=matriz_pelicula.corrwith(user_rating)
		similar.head()

		corr = pd.DataFrame(similar, columns=['correlation'])
		corr.dropna(inplace=True)
		corr.head()

		corr = corr.join(ratings['numero_de_rating'],how='left', lsuffix='_left', rsuffix='_right')
		corr.head()

		items_similares = corr[corr['numero_de_rating'] > 2].sort_values(by='correlation', ascending=False).head(10)
		print(items_similares)
	except KeyError:
		print("Oops!  La palabra ingresado no se encuetra registarda.  Intenta de nuevo...")
else:
	print("Oops!  La palabra ingresado no se encuetra registarda.  Intenta de nuevo...")


